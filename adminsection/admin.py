from django.contrib import admin

# Register your models here.
from adminsection.models import (Customer,
                                 Invoice,
                                 Service)

admin.site.register(Customer)
admin.site.register(Invoice)


class MyModelAdmin(admin.ModelAdmin):
    readonly_fields = ['TimeStamp']


admin.site.register(Service, MyModelAdmin)
