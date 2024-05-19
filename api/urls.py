
from django.contrib import admin
from django.urls import path, include

from api.views.MovieView import MovieView
from api.views.RegisterView import register
from api.views.ShowtimeView import ShowtimeView
from api.views.BookingView import BookingView
from api.views.TicketView import TicketView
from api.views.LoginView import login
from api.views.ChangePasswordView import ChangePassword
from api.views.UpdateProfileView import UpdateProfileView

urlpatterns = [
    path('api/film/', MovieView.as_view()),
    path('api/film/<int:id>', MovieView.as_view()),

    path('api/register/', register),
    path('api/login/', login),
    path('api/change_password/', ChangePassword.as_view()),
    path('api/update_profile/<int:id>', UpdateProfileView.as_view()),

    path('api/showtime/', ShowtimeView.as_view()),
    path('api/showtime/<int:id>', ShowtimeView.as_view()),

    path('api/booking/', BookingView.as_view()),
    path('api/booking/<int:id>', BookingView.as_view()),

    path('api/ticket/', TicketView.as_view()),
    path('api/ticket/<int:id>', TicketView.as_view()),

]
