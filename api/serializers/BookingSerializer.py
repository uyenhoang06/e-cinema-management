from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from booking.models import Booking


class BookingSerializer(serializers.Serializer):
    customer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='customer'
    )

    class Meta:
        model = Booking
        fields = ['id', 'created_at', 'score', 'booking_status', 'code', 'customer']

    def create(self, validated_data):
        booking = Booking.objects.create(**self.validated_data)
        booking.save()
        return booking

