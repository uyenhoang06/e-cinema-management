import datetime

from django.contrib.auth.models import User as TemplateUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group


class User(TemplateUser):
    phone = models.CharField(max_length=12, unique=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=5, choices={'m': "Male", 'f': 'Female'})
    is_verified = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="images/", blank=True, null=True)
    membership = models.CharField(max_length=50, choices={
        'standard' :'standard',
        'premium' : 'premium',
        'VIP' : 'VIP'
        }, default='standard')
    score = models.IntegerField(default=0)



class Staff(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE)
    joining_date = models.DateField(auto_now_add=True)
    position = models.CharField(max_length=50, choices={
        'schedule_staff' : 'schedule_staff',
        'ticket_staff' : 'ticket_staff',
        })











