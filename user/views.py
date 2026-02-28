from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        return HttpResponse(f"Welcome to your dashboard, {register_id}!")