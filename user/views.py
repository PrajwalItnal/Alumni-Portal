from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request, register_id):
    
    return HttpResponse(f"Welcome to the Alumni Portal User Page, {register_id}!")

