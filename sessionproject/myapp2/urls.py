from django.urls import path, include
from myapp2 import views

urlpatterns = [
    path("gcookie", views.getcookie),
    path("scookie", views.setcookie)
]