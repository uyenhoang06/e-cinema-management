from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cinemaa.models import ShowTime
from ..serializers.ShowtimeSerializer import ShowtimeSerializer


class ShowtimeView(APIView):
    def get(self, request):
        showtime = ShowTime.objects.all()
        serializer = ShowtimeSerializer(showtime, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShowtimeSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response({'Create showtime successfully': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        showtime = ShowTime.objects.get(id=id)
        serializer = ShowtimeSerializer(instance=showtime, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'update showtime': serializer.data})
        return Response({'message' : 'Showtime does not exist'})

    def delete(self, request, id):
        showtime = ShowTime.objects.get(id=id)
        showtime.delete()
        return Response(f"Successful delete showtime {showtime}")