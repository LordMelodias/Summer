from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def destination(request):
    return render(request, 'destination.html')

def video(request):
    return render(request, 'video.html')