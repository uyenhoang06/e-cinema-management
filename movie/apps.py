from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MovieConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie'


