from collections import defaultdict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta, date

from .forms import *
from booking.models import *
from .serializer import MovieSerializer
#
from movie.models import *
from booking.models import Ticket, Booking


# Create your views here.


class HomeView(View):
    template_name = "home.html"
    Model = Movie

    def list_movie(self):
        items = []
        for i, movie in enumerate(Movie.objects.all()):
            item = {
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'trailer': movie.trailer,
                'poster': movie.poster,
                'banner': movie.banner,
                'age': movie.age,
                'rating': movie.rating,
                'status': movie.status,
                'released_date': movie.released_date,
                'director': movie.director,
                'actor': movie.actor,
                'language': movie.language,
                'country': movie.country,
                'duration': movie.duration,
                'genre': movie.genre
            }
            # print(item)
            items.append(item)
        return items

    def get(self, request):

        context = {
            'movies' : self.list_movie(),
            'current_tab' : 'home'
        }

        return TemplateResponse(request, self.template_name, context)


class ShowtimeView(View):
    template = 'schedule.html'
    def get_showtime(self, date):
        # print(today)
        showtimes = []
        # for i, showtime in enumerate(ShowTime.objects.filter(date__gte=today, date__lte=today+timedelta(days=7))):
        for i, showtime in enumerate(ShowTime.objects.filter(date=date, date__lte=date+timedelta(days=5))):
            item = {
                'id' : showtime.id,
                'movie': showtime.movie,
                'hall': showtime.hall,
                'date': showtime.date,
                'start_time': showtime.start_time,
                'end_time': showtime.end_time,
                'slot_status': showtime.slot_status,
                'subtitle': showtime.subtitle
            }
            # print(item)
            showtimes.append(item)
        return showtimes

    def get_list_time(self, movie, date):
        result = []
        for i, showtime in enumerate(ShowTime.objects.filter(date=date, movie=movie)):
            item = {
                'id' : showtime.id,
                'movie': showtime.movie,
                'hall': showtime.hall,
                'date': showtime.date,
                'start_time': showtime.start_time,
                'end_time': showtime.end_time,
                'slot_status': showtime.slot_status,
                'subtitle': showtime.subtitle
            }
            # print(item)
            result.append(item)
        return result

    def final(self, date):
        result = []

        showtime_today = self.get_showtime(date)
        # print(showtime_today)
        movies_today = []
        for s in showtime_today:
            if s['movie'] not in movies_today:
                movies_today.append(s['movie'])

        for movie in movies_today:
            item = {
                'movie' : movie,
                'showtime' : ShowTime.objects.filter(date=date, movie=movie)
            }
            result.append(item)
        return result

    def get(self, request):
        today = datetime.date.today()
        today_date = date.today()

        list_showtime_today = self.final(today_date)


        context = {
            'today' : today_date,
            'showtime_today' : list_showtime_today,
            # 'list_time': list_showtime_today,

            'next1' : today_date+timedelta(days=1),
            'showtime_next1': self.final(today + timedelta(days=1)),


            'next2': today_date + timedelta(days=2),
            'showtime_next2': self.final(today + timedelta(days=2)),

            'next3': today_date + timedelta(days=3),
            'showtime_next3': self.final(today + timedelta(days=3)),

            'next4': today_date + timedelta(days=4),
            'showtime_next4': self.final(today + timedelta(days=4)),

            'next5': today_date + timedelta(days=5),
            'showtime_next5': self.final(today + timedelta(days=5)),
            'current_tab' : 'schedule'
        }

        return TemplateResponse(request, self.template, context)


@method_decorator([
    login_required(login_url='/login'),
    permission_required('cinemaa.add_showtime', raise_exception=True),
], name='dispatch')
class AddShowtimeView(View):
    template = 'add_schedule.html'

    def get(self, request):
        context = {
            'form': ShowTimeForm(),
        }
        return TemplateResponse(request, self.template, context)

    def post(self, request):
        form = ShowTimeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['add_showtime'] = 'add showtime successfully'
            messages.success(request, 'Add showtime successfully!')
            
        else:
            print(form.errors)
            request.session['add_showtime'] = 'add showtime fail'
            messages.error(request, 'Add showtime unsuccessfully!')
            
        return HttpResponseRedirect("/schedule")


@login_required(login_url='/login')
@permission_required('cinemaa.change_showtime', raise_exception=True)
def update_showtime(request, id):
    showtime = ShowTime.objects.get(id=id)
    form = ShowTimeForm(instance=showtime)

    if request.method == "POST":
        form = ShowTimeForm(request.POST, request.FILES, instance=showtime)
        if form.is_valid():
            showtime.movie = form.cleaned_data['movie']
            showtime.hall = form.cleaned_data['hall']
            showtime.date = form.cleaned_data['date']
            showtime.start_time = form.cleaned_data['start_time']
            showtime.end_time = form.cleaned_data['end_time']
            showtime.slot_status = form.cleaned_data['slot_status']
            showtime.subtitle = form.cleaned_data['subtitle']
            showtime.save()
            # form.save()
            request.session['update_showtime'] = 'update showtime successfully'
        else :
            request.session['update_showtime'] = 'update showtime fail'

        return HttpResponseRedirect('/schedule')

    return render(request, "update_schedule.html", {"form": form})


@login_required(login_url='/login')
@permission_required('cinemaa.delete_showtime', raise_exception=True)
def delete_showtime(request, id):
    show = ShowTime.objects.get(id=id)
    show.delete()
    request.session['delete_showtime'] = 'Delete showtime successfully'
    return HttpResponseRedirect('/schedule')



from booking.models import *
from account.models import *
@method_decorator([
    login_required(login_url='/login'),
], name='dispatch')
class TicketView(View):
    template_name = "ticket.html"

    def list_booking(self, user):
        list_booking = []
        # for i, showtime in enumerate(ShowTime.objects.filter(date__gte=today, date__lte=today+timedelta(days=7))):
        for i, booking in enumerate(Booking.objects.filter(customer=user)):
                item = {
                    "id" : booking.id,
                    "created_at" : booking.created_at,
                    "score" : booking.score,
                    'status' : booking.booking_status
                    # "price" : ticket.ticket_price,
                    # "showtime" : ticket.showtime,
                    # "seat" : ticket.seat,
                }
                list_booking.append(item)
        return list_booking

    def get(self, request):
        today = datetime.date.today()

        user = User.objects.get(username=request.user)
        list_booking = self.list_booking(user)
        ongoing_booking = []
        success_booking = []
        for booking in list_booking:
            if booking['status'] == 'on-going':
                ongoing_booking.append(booking)
            elif booking['status'] == 'successful':
                success_booking.append(booking)

        success_booking = sorted(success_booking, key= lambda x: x['created_at'], reverse=True)

        context = {
            'current_tab': 'ticket',
            'booking' : list_booking,
            'ongoing_booking' : ongoing_booking,
            'success_booking' : success_booking,
            'user' : user,
        }
        return TemplateResponse(request, self.template_name, context)


@login_required(login_url='/login')
def delete_ticket(request, id):
    booking = Booking.objects.get(id=id)
    booking.delete()
    request.session['delete_ticket'] = 'delete ticket successfully'
    return HttpResponseRedirect('/ticket')

@login_required(login_url='/login')
def payment_detail(request, id):
    booking = Booking.objects.get(id=id)
    ticket = Ticket.objects.filter(booking=booking)
    return render(request, 'payment_detail.html', {
        'booking' : booking,
        'ticket' : ticket
    })


def ticket_detail(request, id):
    ticket = Ticket.objects.get(id=id)
    return render(request, 'ticket_detail.html', {
        'ticket' : ticket,
    })







from django.db.models import Count, F, Sum, Avg
months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]
colorPalette = ["#55efc4", "#81ecec", "#a29bfe", "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8"]
colorPrimary, colorSuccess, colorDanger = "#79aec8", colorPalette[0], colorPalette[5]

def get_year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict

def filter_option(request):
    group_purchase = Booking.objects.annotate(year=ExtractYear("created_at")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in group_purchase]
    # print(group_purchase)

    return JsonResponse({
        "options" : options,
    })

def booking_price(booking):
    ticket = Ticket.objects.filter(booking=booking)
    price = 0
    for t in ticket:
        price += t.ticket_price
    return price

def get_sale_chart(request, year):
    booking = Booking.objects.filter(created_at__year=year)
    sale_dict = get_year_dict()

    for b in booking:
        price = booking_price(b)
        # print(price)
        month = b.created_at.strftime("%m")
        if month == '01':
            sale_dict["January"] += price
        elif month == '02':
            sale_dict["February"] += price
        elif month == '03':
            sale_dict["March"] += price
        elif month == '04':
            sale_dict["April"] += price
        elif month == '05':
            sale_dict["May"] += price
        elif month == '06':
            sale_dict["June"] += price
        elif month == '07':
            sale_dict["July"] += price
        elif month == '08':
            sale_dict["August"] += price
        elif month == '09':
            sale_dict["September"] += price
        elif month == '10':
            sale_dict["October"] += price
        elif month == '11':
            sale_dict["November"] += price
        elif month == '12':
            sale_dict["December"] += price

    return JsonResponse({
        "title": f"Sales in {year}",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(sale_dict.values()),
            }]
        },
    })


def get_sale_today():
    today = datetime.date.today()
    result = 0
    booking = Booking.objects.all()
    for b in booking:
        time = b.created_at.strftime("%Y-%m-%d")
        if time == str(today):
            result += booking_price(b)
    return result


def get_sale_month():
    month = datetime.date.today().strftime("%m")
    year = datetime.date.today().strftime("%Y")
    result = 0
    booking = Booking.objects.all()
    for b in booking:
        b_time = b.created_at.strftime("%m")
        b_year = b.created_at.strftime("%Y")
        if b_time == str(month) and b_year == str(year):
            result += booking_price(b)
    return result


def sale_film(movie):
    tickets = Ticket.objects.all()
    result = 0
    for t in tickets:
        if t.showtime.movie.title == movie:
            # print(t.showtime.movie)
            result += t.ticket_price
    return result


def get_film_dict():
    film_dict = dict()
    movies = Movie.objects.all().values_list('title', flat=True)
    for m in movies:
        film_dict[m] = 0

    return film_dict


def statistic_view(request):
    sale_film_dict = get_film_dict()
    # print(sale_film_dict)
    movies = Movie.objects.all().values_list('title', flat=True)
    for m in movies:
        # print(sale_film(m))
        sale_film_dict[m] += float(sale_film(m))
    sale_film_dict = dict(sorted(sale_film_dict.items(), key=lambda x:x[1], reverse=True))
    # print(sale_film_dict)

    sale_month = get_sale_month()
    sale_today = get_sale_today()
    # print(sale_today)
    # print(sale_month)

    cus_group = Group.objects.get(name='customer')
    customers = cus_group.user_set.all()
    print(len(customers))
    ticket_group = Group.objects.get(name='ticket_staff')
    tickets_staff = ticket_group.user_set.all()
    print(len(tickets_staff))
    schedule_group = Group.objects.get(name='schedule_staff')
    schedule_staff = schedule_group.user_set.all()
    print(len(schedule_staff))
    return render(request, "chart/sale_chart.html", {
        'sale_film' : sale_film_dict,
        'sale_today' : sale_today,
        'sale_month' : sale_month,
        'num_customer' : len(customers),
        'num_ticket_staff' : len(tickets_staff),
        'num_schedule_staff' : len(schedule_staff),
    })










































@api_view(['GET'])
def api_get_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def api_post_movie(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'Create movie successfully' : serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def api_update_movie(request, id):
    movie = Movie.objects.get(id = id)
    serializer = MovieSerializer(instance=movie, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'update movie' : serializer.data})
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def api_delete_movie(request, id):
    movie = Movie.objects.get(id = id)
    movie.delete()

    return Response(f"Successful delete movie")

