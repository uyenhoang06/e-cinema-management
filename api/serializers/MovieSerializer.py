
from rest_framework import serializers

from movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='genre'
    )

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'trailer', 'poster', 'banner', 'age',
                  'status', 'released_date', 'director', 'actor', 'language', 'country', 'duration', 'genre']

