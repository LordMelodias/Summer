from django.contrib import admin
from .models import employee
# Register your models here.

class Adminemployee(admin.ModelAdmin):
    list_display = ['username', 'email']

admin.site.register(employee, Adminemployee)