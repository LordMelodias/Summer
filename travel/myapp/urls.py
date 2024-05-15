from django.urls import path
from myapp import views


urlpatterns = [
    path(" ", views.index, name='home'),
    path("destination", views.destination, name='destination'),
    path("video", views.video, name='video'),
    path("booking", views.booking, name='booking'),
    path("login", views.login, name='login'),
]