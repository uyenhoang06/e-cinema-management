# Generated by Django 5.0.1 on 2024-01-13 19:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_booking_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
