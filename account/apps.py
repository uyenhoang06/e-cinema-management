from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        post_migrate.connect(create, sender=self)


def create(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    # from movie.models import Movie
    from .models import User

    roles = ['admin', 'schedule_staff', 'ticket_staff', 'customer']
    for role in roles:
        if not Group.objects.filter(name=role).exists():
            Group.objects.create(name=role)

    schedule_staff_group = Group.objects.get(name='schedule_staff')
    perms1 = [
        Permission.objects.get(codename='change_movie', content_type__app_label='movie'),
        Permission.objects.get(codename='add_movie', content_type__app_label='movie'),
        Permission.objects.get(codename='delete_movie', content_type__app_label='movie'),

        Permission.objects.get(codename='view_booking', content_type__app_label='booking'),
        Permission.objects.get(codename='add_showtime', content_type__app_label='cinemaa'),
        Permission.objects.get(codename='change_showtime', content_type__app_label='cinemaa'),
        Permission.objects.get(codename='delete_showtime', content_type__app_label='cinemaa'),
    ]
    for p in perms1:
        schedule_staff_group.permissions.add(p)
    schedule_staff_group.save()

    # schedule_staff, _ = User.objects.get_or_create(username='thanhhai1')
    # schedule_staff.groups.add(schedule_staff_group)

    ticket_staff_group = Group.objects.get(name='ticket_staff')
    perms2 = [
        Permission.objects.get(codename='view_booking', content_type__app_label='booking'),
    ]
    for p in perms2:
        ticket_staff_group.permissions.add(p)
    ticket_staff_group.save()


    customer_group = Group.objects.get(name='customer')
    perms3 = [
        Permission.objects.get(codename='add_booking', content_type__app_label='booking'),
        Permission.objects.get(codename='delete_booking', content_type__app_label='booking'),
        Permission.objects.get(codename='change_booking', content_type__app_label='booking'),
    ]
    for p in perms3:
        customer_group.permissions.add(p)
    customer_group.save()



