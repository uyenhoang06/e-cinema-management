from django.db import models

from movie.models import Movie


class Cinema(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_contact = models.CharField(max_length=12, null=True, blank=True)
    email_contact = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    is_activate = models.BooleanField(default=True)
    image = models.ImageField(blank=True, upload_to="images/", null=True)

    def __str__(self):
        return self.name


class HallType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to="images/", null=True)
    price_surcharge = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Hall(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    number_of_row = models.IntegerField(blank=True, null=True)
    number_of_column = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, choices={
        'available': 'available',
        'unavailable': 'unavailable',
        'under_maintenance': 'under_maintenance'
    })

    cinema = models.ForeignKey(Cinema, null=True, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(HallType, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name


class ShowType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class ShowTime(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_status = models.CharField(max_length=50, choices={
        'available': 'available',
        'full': 'full',
        'cancelled': 'cancelled'
    })
    subtitle = models.CharField(max_length=50, choices={
        'subtitle': 'subtitle',
        'voice-over': 'voice-over'
    })

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    type = models.ForeignKey(ShowType, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.movie.title


class SeatType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to="images/", null=True)
    price_surcharge = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Seat(models.Model):
    id = models.AutoField(primary_key=True)
    row = models.IntegerField()
    col = models.IntegerField()

    hall = models.ForeignKey(Hall, null=True, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(SeatType, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'[{self.type}] {self.row}, {self.col}'


class ShowtimeSeat(models.Model):
    id = models.AutoField(primary_key=True)

    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    status = models.CharField(max_length=50, choices={
        'available' : 'available',
        'unavailable' : 'unavailable'
    })


