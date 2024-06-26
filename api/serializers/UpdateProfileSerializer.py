
from rest_framework import serializers

from account.models import User


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'address', 'gender', 'birthday', "avatar")
