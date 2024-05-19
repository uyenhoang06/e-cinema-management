from django.contrib import admin
from .models import *


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre')
    class Meta:
        model = Genres


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'age','rating', 'status', 'released_date', 'duration')

    class Meta:
        model = Movie

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'review', 'rating')
    class Meta:
        model = CustomerRating


# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genres, GenreAdmin )
admin.site.register(CustomerRating, RatingAdmin)
