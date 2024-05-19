from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from account.models import User
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create(**self.validated_data)
        user.set_password(self.validated_data['password'])
        user.save()
        return user


