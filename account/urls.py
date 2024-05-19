from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('update_profile/<int:id>', update_profile, name = "update_profile"),
    path('change_password', change_password, name = 'change_password')

    # path('token_send', token_send, name='token_send'),
    # path('emailActivate/<uidb64>/<token>', activate, name='emailActivate')
]