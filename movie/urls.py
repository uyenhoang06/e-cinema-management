
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('film', views.MovieView.as_view(), name = 'film'),
    path('add_film', views.AddMovieView.as_view(), name = 'add_film'),
    path('film/<int:id>', views.detail_movie, name = "detail_movie"),
    path('film/<int:id>/review_rating', views.review_rating, name="review_rating"),
    path('update_film/<int:id>', views.update_film),
    path('delete_film/<int:id>', views.delete_film)
]