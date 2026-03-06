from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('remove-photo/', views.remove_photo, name='remove_photo'),
]
