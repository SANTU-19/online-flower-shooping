from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.
 
@login_required(login_url='/accounts/login/')

def flowers(request):
    products=Product.objects.all()
    return render(request,'flowers.html',{'products':products})

