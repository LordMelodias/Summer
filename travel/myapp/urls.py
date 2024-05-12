from django.urls import path
from myapp import views


urlpatterns = [
    path(" ", views.index, name='home'),
    path("destination", views.destination, name='destination')
]