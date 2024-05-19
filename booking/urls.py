
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('book_showtime/<int:id>', BookingView.as_view(), name='booking'),
    path('payment/<int:id>', PaymentView.as_view(), name='payment'),
    path('list_booking', ListBooking.as_view(), name='list_booking'),

    path('search_result/', ListBooking.as_view(), name='search_result'),
    path('check_out/<int:id>', check_out, name='check-out'),

    # path('search_result/ticket/payment_detail/<int:id>', ListBooking.as_view())
]

