from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from django.core import serializers

from ..serializers.BookingSerializer import BookingSerializer
from booking.models import Booking


class BookingView(APIView):

    def get(self, request):
        booking_list = Booking.objects.all().values()
        return JsonResponse({'List bookings': list(booking_list)})

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Create booking successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        booking = Booking.objects.get(id=id)
        booking.delete()
        return Response(f"Successful delete booking {id}")

        # def get(self, request):
    #     bookings = Booking.objects.all()
    #     result = []
    #
    #     for booking in bookings:
    #         item = {
    #             'id' : booking.id,
    #             'created_at' : booking.created_at,
    #             'score' : booking.score,
    #             'booking_status' : booking.booking_status,
    #             'code' : booking.code,
    #             'customer' : booking.customer.values()
    #         }
    #         result.append(item)
    #
    #     return Response(result)