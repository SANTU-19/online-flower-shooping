from django.urls import path
from . import views

urlpatterns = [
  path('flowers/',views.flowers,name='flowers'),
]