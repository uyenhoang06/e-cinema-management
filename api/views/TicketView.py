from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.models import Ticket

from ..serializers.TicketSerializer import TicketSerializer


class TicketView(APIView):
    def get(self, request):
        ticket = Ticket.objects.all()
        serializer = TicketSerializer(ticket, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response({'Create ticket successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ticket = Ticket.objects.get(id=id)
        ticket.delete()
        return Response(f"Successful delete ticket {id}")