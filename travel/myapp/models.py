from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

# for register
class User(models.Model):
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    otp = models.IntegerField()
    verified = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        # Only hash the password if it's not already hashed
        if not self.password.startswith('pbkdf2_sha256$'):  # Ensure hashing only if not already hashed
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, password):
	    return check_password(password, self.password)
 
class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()

class Host(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    otp = models.IntegerField()
    verified = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        # Only hash the password if it's not already hashed
        if not self.password.startswith('pbkdf2_sha256$'):  # Ensure hashing only if not already hashed
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, password):
	    return check_password(password, self.password)