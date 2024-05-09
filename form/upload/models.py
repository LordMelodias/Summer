from django.db import models

# Create your models here.
class employee(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    file = models.FileField()
    class Meta:
        db_table = 'employee'
    