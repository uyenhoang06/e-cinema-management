
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie.models import *
from .serializer import *


@api_view(['GET'])
def api_get_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def api_post_movie(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'Create movie successfully' : serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def api_update_movie(request, id):
    movie = Movie.objects.get(id = id)
    serializer = MovieSerializer(instance=movie, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'update movie' : serializer.data})
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def api_delete_movie(request, id):
    movie = Movie.objects.get(id = id)
    movie.delete()

    return Response(f"Successful delete movie")


