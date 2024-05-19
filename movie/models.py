from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from account.models import User


class Genres(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, null=True, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    trailer = models.FileField(upload_to='video/', blank=True, null=True)
    poster = models.ImageField(blank=True, upload_to="images/", null=True)
    banner = models.ImageField(blank=True, upload_to="images/", null=True)
    age = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, default=0)
    status = models.CharField(max_length=10, choices={'now': 'now', 'soon': 'soon'})
    released_date = models.DateField()
    director = models.CharField(max_length=255, blank=True, null=True)
    actor = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)

    genre = models.ManyToManyField(Genres)

    def __str__(self):
        return self.title




class CustomerRating(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    movie = models.ForeignKey(Movie, null=True, on_delete=models.SET_NULL)

    review = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    create_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.review





