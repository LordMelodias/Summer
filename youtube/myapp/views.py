from django.shortcuts import render

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