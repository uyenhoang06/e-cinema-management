import base64
import datetime
import decimal
import io
import random
import string
from io import BytesIO
from django.utils.crypto import get_random_string

import qrcode
from PIL import Image, ImageDraw
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View
from cinemaa.models import *
from .form import *
from qrcode import *
# Create your views here.


@method_decorator([
    login_required(login_url='/login'),
], name='dispatch')
class BookingView(View):
    def list_seat(self, id):
        show = ShowTime.objects.get(id=id)
        hall = show.hall
        list_seats = []
        for i, s in enumerate(ShowtimeSeat.objects.filter(showtime=show)):
            item = {
                'id' : s.id,
                'row' : s.seat.row,
                'col' : s.seat.col,
                'status' : s.status,
                'type' : s.seat.type,
            }
            # print(item['type'], item['status'])
            # print(item)
            list_seats.append(item)
        return list_seats

    def get(self, request, id):
        show = ShowTime.objects.get(id=id)
        hall = show.hall

        list_seats = self.list_seat(id)
        num_row = hall.number_of_row
        num_col = hall.number_of_column

        form = TicketForm(show)
        list_form = {
            r:{
                c : {} for c in range(1, num_col+1)
            } for r in range(1, num_row+1)
        }
        for s in list_seats:
            list_form[s['row']] [s['col']] = {
                **s
            }

        return render(request, 'booking.html', context={
            'seats': list_seats,
            'show' : show,
            'form' : form,
            'rows' : range(1, num_row+1, 1),
            'cols' : range(1, num_col+1, 1),
            'list_form' : list_form
        })

    def post(self, request, id):
        seats = request.POST.getlist('seat') if 'seat' in request.POST else []
        user = User.objects.get(username=request.user)
        showtime = ShowTime.objects.get(id=id)
        seat_reserved = []
        price = 0
        booking, _ = Booking.objects.get_or_create(customer=user, booking_status='on-going')

        for s in seats:
            seat = ShowtimeSeat.objects.get(id=int(s))
            if seat not in seat_reserved:
                seat_reserved.append(seat)

            # if request.user.groups.filter(name='customer').exists():
            # else:
                # form = TicketScheduleForm
                # booking, _ = Booking.objects.get_or_create(staff=user, booking_status='on-going')
            booking.score += 10

            seat_price = seat.seat.type.price_surcharge
            price+=seat_price

            hall = showtime.hall
            price += hall.type.price_surcharge
            ticket = TicketForm(data={'seat': seat, 'booking': booking, 'showtime': showtime, 'ticket_price': price}, showtime=showtime)
            if ticket.is_valid():
                ticket.save()
                booking.save()
            else:
                print('loi', ticket.errors.as_data())
        return HttpResponseRedirect(f'/payment/{booking.id}')


@method_decorator([
    login_required(login_url='/login'),
], name='dispatch')
class PaymentView(View):
    def booking_price(self, id):
        booking = Booking.objects.get(id=id)
        booking_discount = BookingDiscount.objects.filter(booking=booking)
        ticket = Ticket.objects.filter(booking=booking)
        price = 0
        list_seat = []
        for t in ticket:
            if t.seat.seat not in list_seat:
                list_seat.append(t.seat.seat)
                price += t.ticket_price

        normal_price = price
        for bd in booking_discount:
            discount = bd.discount
            score = bd.score
            if discount is not None:
                price -= price*(discount.percentage/100)
            if score is not None:
                price = round(price - decimal.Decimal(score / 100), 2)

        return normal_price, price

    def get(self, request, id):
        print(request)
        booking = Booking.objects.get(id=id)
        ticket = Ticket.objects.filter(booking=booking)
        # print(len(ticket))
        if len(ticket) ==0:
            request.session['booking'] = 'this seat is unavailable'
            return HttpResponseRedirect(f'http://127.0.0.1:8000/schedule')

        showtime = ticket[0].showtime
        print(ticket[0].seat.showtime)

        list_seat = []
        for t in ticket:
            if t.seat.seat not in list_seat:
                list_seat.append(t.seat.seat)
        # print(list_seats)

        return render(request, 'payment.html',{
            "discount" : DiscountForm(),
            "showtime" : showtime,
            "seats" : list_seat,
            "user" : booking.customer,
            "booking" : booking,
            'normal_price' : self.booking_price(id)[0],
        })

    def post(self, request, id):

        # print(request.POST)
        if 'apply_discount' in request.POST:
            return self.apply_discount(request, id)
        elif 'dat_ve' in request.POST:
            return self.dat_ve(request, id)
        elif 'use_score' in request.POST:
            return self.use_score(request, id)
        elif 'delete_score' in request.POST:
            return self.delete_score(request, id)
        elif 'delete_discount' in request.POST:
            return self.delete_discount(request, id)
        else:
            print("loi")

    def dat_ve(self, request, id):
        booking = Booking.objects.get(id=id)
        booking_discount = BookingDiscount.objects.filter(booking=booking)
        allowed_chars = ''.join((string.ascii_letters, string.digits))
        code = ''.join(random.choice(allowed_chars) for _ in range(6))
        booking.code=code
        booking.booking_status = 'successful'

        user = User.objects.get(username=request.user)
        user.score += 10

        ticket = Ticket.objects.filter(booking=booking)
        for t in ticket:
            t.seat.status = 'unavailable'
            t.seat.save()

        for bd in booking_discount:
            if bd.score is not None:
                user.score -= bd.score
            if bd.discount_id is not None:
                discount = Discount.objects.get(id=bd.discount_id)
                discount.delete()
                booking_discount.delete()
                print('da delete')

        user.save()
        booking.save()
        # booking_discount.save()


        return render(request, 'payment_success.html', {
            'booking': booking,
            'message' : 'Dat ve thanh cong'
        })


    def apply_discount(self, request, id):
        form = DiscountForm(request.POST)
        # print(form.data)
        booking = Booking.objects.get(id=id)
        ticket = Ticket.objects.filter(booking=booking)
        # print(ticket)
        showtime = ticket[0].showtime
        list_seat = []
        for t in ticket:
            if t.seat.seat not in list_seat:
                list_seat.append(t.seat.seat)
        if form.is_valid():
            discount = form.save(booking=booking)
            if discount:
                BookingDiscount.objects.create(booking=booking, discount=discount)

            normal_price, price = self.booking_price(id)

            return render(
                request, 'payment.html', {
                    "discount": DiscountForm(),
                    "showtime": showtime,
                    "seats": list_seat,
                    "user": booking.customer,
                    "booking": booking,
                    'price': price,
                    'normal_price': normal_price,
                    'message' : 'Apply discount successfully',
                    'applied_discount' : [bd.discount.code for bd in BookingDiscount.objects.filter(booking=booking) if bd.discount is not None]
                }
            )
        else:
            print(form.errors)

    def use_score(self, request, id):
        booking = Booking.objects.get(id=id)
        user = User.objects.get(username=request.user)
        ticket = Ticket.objects.filter(booking=booking)
        # print(ticket)
        showtime = ticket[0].showtime
        list_seat = []
        for t in ticket:
            if t.seat.seat not in list_seat:
                list_seat.append(t.seat.seat)

        score = 0
        booking_discount = BookingDiscount.objects.filter(booking=booking)
        for bd in booking_discount:
            score += bd.score if bd.score is not None else 0
        if score == 0:
            BookingDiscount.objects.create(booking=booking, score=user.score)
        normal_price, price = self.booking_price(id)

        return render(
            request, 'payment.html', {
                "discount": DiscountForm(),
                "showtime": showtime,
                "seats": list_seat,
                "user": booking.customer,
                "booking": booking,
                'normal_price' : normal_price,
                'price': price,
                'score': score,
                'message': 'Use score successfully',
                'applied_discount': [bd.discount.code for bd in BookingDiscount.objects.filter(booking=booking) if
                                     bd.discount is not None]
            }
        )

    def delete_score(self, request, id):
        booking = Booking.objects.get(id=id)
        ticket = Ticket.objects.filter(booking=booking)
        showtime = ticket[0].showtime
        list_seat = []
        for t in ticket:
            if t.seat.seat not in list_seat:
                list_seat.append(t.seat.seat)
        booking_discount = BookingDiscount.objects.filter(booking=booking)
        for bd in booking_discount:
            if bd.score is not None :
                bd.delete()


        normal_price, price = self.booking_price(id)

        return render(
            request, 'payment.html', {
                "discount": DiscountForm(),
                "showtime": showtime,
                "seats": list_seat,
                "user": booking.customer,
                "booking": booking,
                'normal_price' : normal_price,
                'price': price,
                'message': 'do not use score',

                'applied_discount': [bd.discount.code for bd in BookingDiscount.objects.filter(booking=booking) if
                                     bd.discount is not None]
            }
        )

    def delete_discount(self, request, id):
        booking = Booking.objects.get(id=id)
        ticket = Ticket.objects.filter(booking=booking)
        showtime = ticket[0].showtime
        list_seat = []
        for t in ticket:
            if t.seat.seat not in list_seat:
                list_seat.append(t.seat.seat)
        booking_discount = BookingDiscount.objects.filter(booking=booking)
        for bd in booking_discount:
            if bd.discount is not None :
                bd.delete()

        normal_price, price = self.booking_price(id)

        return render(
            request, 'payment.html', {
                "discount": DiscountForm(),
                "showtime": showtime,
                "seats": list_seat,
                "user": booking.customer,
                "booking": booking,
                'normal_price' : normal_price,
                'price': price,
                'message': 'do not use discount',

                'applied_discount': [bd.discount.code for bd in BookingDiscount.objects.filter(booking=booking) if
                                     bd.discount is not None]
            }
        )


@method_decorator([
    login_required(login_url='/login'),
    permission_required('booking.view_booking', raise_exception=True),
], name='dispatch')
class ListBooking(View):
    def count_today(self):
        today = datetime.date.today()
        # print(today)
        count=0
        booking = Booking.objects.filter(booking_status='successful') | Booking.objects.filter(booking_status='check-out')
        for b in booking:
            time =  b.created_at.strftime("%Y-%m-%d")
            # print(time)
            if time == str(today):
                count+=1
        return count

    def count_month(self):
        today = datetime.date.today().strftime("%m")
        year = datetime.date.today().strftime("%Y")
        print(year)
        # print(today)
        # print(today)
        count=0
        booking = Booking.objects.filter(booking_status='successful') | Booking.objects.filter(booking_status='check-out' )
        for b in booking:
            b_time =  b.created_at.strftime("%m")
            b_year = b.created_at.strftime("%Y")
            print(b_year)
            if b_time == str(today) and b_year==str(year):
                count+=1
        return count

    def get(self, request):
        booking = Booking.objects.filter(booking_status='successful').order_by('-created_at')
        check_out = Booking.objects.filter(booking_status='check-out')
        count_today = self.count_today()
        count_month = self.count_month()
        # print(count_month)
        # print(booking)
        return render(request, "list_booking.html", {
            'booking' : booking,
            'check_out' : check_out,
            'search' : SearchForm(),
            'count_today' : count_today,
            'count_month' : count_month,
        } )

    def post(self, request):
        data = request.POST
        code = data.get('code')
        # print(code)
        booking = Booking.objects.filter(code=code)
        # print(booking)
        return render(request, 'search_result.html', {
            'booking' : booking
        })



def check_out(request, id):
    booking = Booking.objects.get(id=id)
    booking.booking_status = 'check-out'
    booking.save()
    request.session['check-out'] = 'Check-out successfully'
    return HttpResponseRedirect('/list_booking')


