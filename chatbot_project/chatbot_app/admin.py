# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import OTP, History

admin.site.register(OTP)
admin.site.register(History)
