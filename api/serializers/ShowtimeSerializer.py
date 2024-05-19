
from rest_framework import serializers

from cinemaa.models import ShowTime
from rest_framework.relations import StringRelatedField


class ShowtimeSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    hall = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )


    class Meta:
        model = ShowTime
        fields = ['id', 'movie', 'hall', 'date', 'start_time', 'end_time', 'slot_status', 'subtitle']



