from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def item(request):
    return render(request, 'flower.html')

def contact(request):
    return render(request, 'contact.html')



from django.contrib import messages
from django.shortcuts import redirect

def signup(request):
    if request.method == "POST":
        messages.success(request, "Signup successful 🎉")
        return redirect('login')
