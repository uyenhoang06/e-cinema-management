from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.MovieSerializer import MovieSerializer
from movie.models import Movie


class MovieView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Create movie successfully': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        movie = Movie.objects.get(id=id)
        serializer = MovieSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'update movie': serializer.data})
        return Response({'message' : 'Movie does not exist'})

    def delete(self, request, id):
        movie = Movie.objects.get(id=id)
        movie.delete()
        return Response(f"Successful delete movie {id}")