from django.urls import path
from . import views

urlpatterns = [
    # This matches the list of past/active orders
    path('', views.order_list, name='order_list'),
    
    # This matches the page where the user selects COD or Online
    path('checkout/', views.checkout_page, name='checkout'),
    
    # This matches the AJAX logic that sends the "Congratulations" message
    path('place-order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]