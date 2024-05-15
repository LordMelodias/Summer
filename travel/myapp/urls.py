from django.urls import path
from myapp import views


urlpatterns = [
    path(" ", views.index, name='home'),
    path("destination", views.destination, name='destination'),
    path("video", views.video, name='video'),
    path("booking", views.booking, name='booking'),
    path("login", views.login, name='login'),
    path("login_view", views.login_view, name='login_view'),
    path("register", views.register, name='register'),
    path("save_register", views.save_register, name='save_register'),
    path('otp/<str:email>/', views.otp, name='otp'),
    path("contact", views.contact, name='contact'),
]