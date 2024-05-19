
# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.

class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff', 'joining_date', 'phone', 'birthday', 'address', 'position')

    def phone(self, user):
        return user.staff.phone

    def birthday(self, user):
        return user.staff.birthday

    def address(self, user):
        return user.staff.address


# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'phone', 'address', 'membership', 'score')
#
#     def phone(self, user):
#         return user.customer.phone
#
#     def birthday(self, user):
#         return user.customer.birthday
#
#     def address(self, user):
#         return user.customer.address


admin.site.register(User)
admin.site.register(Staff, StaffAdmin)
# admin.site.register(Customer, CustomerAdmin)
