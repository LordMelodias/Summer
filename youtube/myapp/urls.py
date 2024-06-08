from django.urls import path, include
from myapp import views

urlpatterns = [
    path("", views.home, name='home'),
    path("channel_video", views.channel_video, name='channel_video'),
    path("about", views.about, name='about'),
    path("community", views.community, name='community'),
    path("video", views.video, name='video'),
    path("login", views.login, name="login"),
    path("register", views.register, name='register'),
    path("login_view", views.login_view, name='login_view'),
    path("save_register", views.save_register, name='save_register'),
    path('otp/<str:email>/', views.otp, name='otp'),
    path('create_channel/<str:email>/', views.create_channel, name='create_channel'),
    path('channel/<str:email>/', views.create_chan, name="create_chan"),
]