from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('upload_video', views.upload_video, name='upload_video'),
    path('play_video/<str:name>/', views.play_video, name='play_video'),
    path('subscribe_channel', views.subscribe_channel, name='subscribe_channel'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)