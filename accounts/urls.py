from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),  # <-- ADD THIS
    path('forgot-password/',views.forgot_password_view, name='forgot_password'),
    path('reset-otp/', views.reset_verify_otp_view, name='reset_verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('verify-otp-signup/', views.verify_otp_signup_view, name='verify_otp_signup'),


]
