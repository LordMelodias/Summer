from django.db import models

# Create your models here.
class register(models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    age = models.IntegerField()
    password = models.CharField(max_length=20)