from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from user.models import User

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def login(request):
    if request.method == "POST":
        register_id = request.POST.get("register_id")
        password = request.POST.get("password")
        user = None
        try:
            user = User.objects.get(register_id=register_id, password=password)
            return redirect('user:home', register_id=user.register_id)
        except User.DoesNotExist:
            messages.error(request, "Invalid register ID or password.")
            return redirect('login')
    return render(request, "login.html")