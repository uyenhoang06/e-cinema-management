from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from booking.models import Ticket


class TicketSerializer(serializers.Serializer):
    booking = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )
    seat = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )
    showtime = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Ticket
        fields = ['id', 'seat', 'booking', 'showtime', 'ticket_price']

    def create(self, validated_data):
        ticket = Ticket.objects.create(**self.validated_data)
        ticket.save()
        return ticket



