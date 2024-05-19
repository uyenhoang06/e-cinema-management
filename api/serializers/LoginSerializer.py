from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from account.models import User



class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'password']