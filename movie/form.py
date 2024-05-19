
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.utils.dateparse import parse_duration

from .models import *


class DurationInput(TextInput):
    def _format_value(self, value):
        duration = parse_duration(value)

        seconds = duration.seconds

        minutes = seconds // 60
        seconds = seconds % 60

        minutes = minutes % 60

        return '{:02d}:{:02d}'.format(minutes, seconds)

class MovieForm(ModelForm):
    class Meta:
        model = Movie
        autocomplete_fields = ['genre']
        fields = ('title', 'description', 'trailer', 'poster', 'banner', 'age',
                  'released_date', 'director', 'actor', 'language', 'country', 'duration', 'genre')
        widgets = {
            # "id": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "title": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "description": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "trailer": forms.FileInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "poster": forms.FileInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "banner": forms.FileInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "age": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "released_date": forms.DateInput(attrs={'type': 'date'}),
            "director": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "actor": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "language": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "country": forms.TextInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "duration": DurationInput(),
            "genre": forms.CheckboxSelectMultiple()
        }


class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}))

    class Meta:
        model = CustomerRating
        fields = ['review', 'rating']

