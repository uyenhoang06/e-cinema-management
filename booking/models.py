from django.db import models
import django.utils.timezone as timezone # Create your models here.
from cinemaa.models import *
from account.models import *
from cinemaa.models import *


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)
    booking_status = models.CharField(max_length=50, choices={
        'successful' : 'successful',
        'on-going' : 'on-going',
        'check-out' : 'check-out',
    }, default='on-going')
    code = models.CharField(max_length=10, null=True, blank=True, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    seat = models.ForeignKey(ShowtimeSeat, on_delete=models.DO_NOTHING)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)


class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    maximum_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)


class BookingDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    score = models.IntegerField(null=True, blank=True)

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)


    