from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
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
 
 
class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    path = models.CharField(max_length=60)
    datetime = models.DateTimeField(blank=False, null=False) #todo: auto_now=True
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    number_of_views = models.IntegerField(blank=True, default=0)

class Comment(models.Model):
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Channel(models.Model):
    channel_name = models.CharField(max_length=50, blank=False, null=False)
    subscribers = models.IntegerField(default=0, blank=False, null=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    email = models.EmailField(primary_key=True)
    image = models.ImageField(upload_to='youtube_clone/myapp/static/channel')  # Directory to store images

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Dislike(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Video_View(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)

class Channel_Subscription(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
