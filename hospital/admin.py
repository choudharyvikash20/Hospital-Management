from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Patient)
admin.site.register(appointment)
admin.site.register(Doctor)
admin.site.register(Receptionist)