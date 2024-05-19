
import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import *
from cinemaa.models import *


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('seat', 'booking', 'showtime', 'ticket_price')
        widgets = {
            "seat": forms.CheckboxSelectMultiple(attrs={
            }),
        }

    def __init__(self, showtime, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['seat'].queryset = ShowtimeSeat.objects.filter(showtime=showtime)

    def clean_seat(self):
        seat = self.cleaned_data['seat']
        if seat.status == 'available':
            return seat
        raise ValidationError('loi')



class TicketScheduleForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('customer',)


class DiscountForm(forms.Form):
    code = forms.CharField(max_length=50, required=False )

    def save(self, booking, commit=True,):
        # print(self.cleaned_data['code'])
        discount = Discount.objects.filter(code=self.cleaned_data['code'])
        if discount.exists():
            if BookingDiscount.objects.filter(booking=booking, discount=discount[0]).exists():
                return None
            return discount[0]
        return None


class DeleteForm(forms.Form):
    # id = forms.IntegerField(widget=forms.HiddenInput)
    id = forms.IntegerField()

    # def save(self, commit=True):
    #     print(self.cleaned_data['id'])
    #     instance = Ticket.objects.get(id=self.cleaned_data['id'])
    #     instance.delete()



class SearchForm(forms.Form):
    code = forms.CharField(max_length=50, required=False )

    def save(self, commit=True,):
        # print(self.cleaned_data['code'])
        booking = Booking.objects.filter(code=self.cleaned_data['code'])
        if booking.exists():
            print(booking)
            return booking[0]
        else:
            print('nothing')
        return None
