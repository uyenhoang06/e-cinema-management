from django.contrib import admin
from .models import *
# Register your models here.

class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'type', 'cinema')
    class Meta:
        model = Hall


class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'date', 'start_time', 'end_time', 'slot_status', 'subtitle')


class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'row', 'col', 'type', 'hall')

class ShowtimeSeatAdmin(admin.ModelAdmin):
    list_display = ('showtime', 'seat', 'status')


admin.site.register(Cinema)
admin.site.register(Hall, HallAdmin)
admin.site.register(HallType)
admin.site.register(ShowTime, ShowtimeAdmin)
admin.site.register(ShowType)
admin.site.register(SeatType)
admin.site.register(Seat, SeatAdmin)
admin.site.register(ShowtimeSeat, ShowtimeSeatAdmin)


