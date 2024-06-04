from django.shortcuts import render
from .models import Video, Comment, Channel, Like, Dislike, Video_View, Channel_Subscription
# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'your_video/about.html')


def channel_video(request):
    return render(request, 'your_video/index.html')

def community(request):
    return render(request, 'your_video/community.html')

def video(request):
    return render(request, 'your_video/video.html')