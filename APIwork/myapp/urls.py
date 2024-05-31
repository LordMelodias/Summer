from django.urls import path
from . import views
urlpatterns = [
    path('', views.getdata),
    path('item', views.manage_item),
    path('item/<int:pk>/', views.manage_item),
]