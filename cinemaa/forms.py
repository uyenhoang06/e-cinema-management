import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import *
from movie.models import *


class ShowTimeForm(forms.ModelForm):
    class Meta:
        model = ShowTime
        fields = ('movie', 'hall', 'date', 'start_time', 'end_time', 'slot_status', 'subtitle')
        widgets = {
            "date": forms.DateInput(attrs={
                'type': 'date',
            }),
        }

    '''
    # ham save() 
    # - tao instance cua showtime
    # - tao seat cho showtime 
    '''
    def save(self, commit=True):
        showtime = ShowTime.objects.create(**self.cleaned_data)
        list_seats = Seat.objects.filter(hall=self.cleaned_data['hall'])
        for seat in list_seats:
            ShowtimeSeat.objects.create(seat=seat, showtime=showtime, status='available')

    def clean_hall(self):
        hall = self.cleaned_data['hall']
        if hall.status == 'available':
            return hall
        raise ValidationError('cut')

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        hall = self.cleaned_data['hall']
        date = self.cleaned_data['date']
        all_showtimes = ShowTime.objects.filter(hall=hall, date=date)
        # print(all_showtimes)
        for showtime in all_showtimes:
            if showtime.start_time <= start_time <= showtime.end_time:
                raise forms.ValidationError('loi')

        return start_time

    def clean_end_time(self):
        # movie = Movie.objects.get(title=self.cleaned_data['movie'])
        # start_time = self.cleaned_data['start_time']
        # print(type(e_time))

        end_time = self.cleaned_data['end_time']
        hall = self.cleaned_data['hall']
        date = self.cleaned_data['date']
        all_showtimes = ShowTime.objects.filter(hall=hall, date=date)
        # print(all_showtimes)
        for showtime in all_showtimes:
            if showtime.start_time <= end_time <= showtime.end_time:
                raise ValidationError('loi')

        return end_time

