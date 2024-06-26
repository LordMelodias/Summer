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
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    video_file = video_file = models.FileField(upload_to='rework/appname/static/videos')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='rework/appname/static/thumbnails')
    number_of_views = models.IntegerField(blank=True, default=0)

class Comment(models.Model):
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Channel(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    subscribers = models.IntegerField(default=0, blank=False, null=False)
    email = models.EmailField(unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rework/appname/static/channel')  # Directory to store images
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

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
    email = models.EmailField()