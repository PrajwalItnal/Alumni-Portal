from email.mime import message
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render,redirect
from user.models import Event, User, Achievement
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from .models import Donation


# Create your views here.
def home(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        user = User.objects.get(register_id=register_id)
        if user.role == "Admin":
            return render(request, "user/admin_home.html", {"user": user})
        elif user.role == "Alumni":
            return render(request, "user/alumni_home.html", {"user": user})
        else:
            return render(request, "user/user_home.html", {"user": user})

def logout(request):
    request.session.flush()
    return redirect('home')

def vi_event(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        user = User.objects.get(register_id=register_id)
        today = datetime.datetime.now()
        events = Event.objects.filter(date__gte = today).order_by("-created_at")
        return render(request, "user/vi_event.html", {"user": user, "events": events})
    
def create_event(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        user = User.objects.get(register_id=register_id)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            event_type = request.POST.get("event_type")
            date = request.POST.get("date")
            time = request.POST.get("event_time")
            location = request.POST.get("location")
            image = request.FILES.get("image")
            date = request.POST.get("date")
            Event.objects.create(title=title, 
                                description=description, 
                                event_type=event_type, 
                                date=date, 
                                event_time=time, 
                                location=location, 
                                image=image,
                                organized_by=user)
            messages.success(request, "Event created successfully!")
            return redirect("user:vi_event")
        return render(request, "user/create_event.html", {"user": user})

def view_achievements(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        user = User.objects.filter(register_id = register_id).first()
        achievements = Achievement.objects.all().order_by('created_at')
        return render(request,"user/view_achievement.html", {"user" : user, "achievements" : achievements})

def create_achievements(request):
    if request.method == 'POST':
        register_id = request.session.get("register_id")
        if not register_id:
            return redirect("login")
        else:
            user = User.objects.filter(register_id = register_id).first()
            title = request.POST.get('title')
            description = request.POST.get('description')
            certificate = request.FILES.get('certificate')
            Achievement.objects.create(
                achieved_by = user,
                title = title,
                description = description,
                certificate = certificate
            )
            messages.success(request, "Achievement add successfully")
            return redirect('user:achievements_view')
    return render(request, "user/create_achievement.html")



def create_donation(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")

    user = User.objects.filter(register_id=register_id).first()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        description = request.POST.get('description')

        if not amount or not payment_method:
            messages.error(request, "❌ Amount and Payment Method are required.")
            return redirect('user:create_donation')

        Donation.objects.create(
            donated_by=user,
            amount=amount,
            payment_method=payment_method,
            description=description,
        )
        messages.success(request, "✅ Donation recorded successfully!")
        return redirect('user:donation_list')
    return render(request, 'user/add_donation.html', {"user": user})

def donation_list(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        user = User.objects.filter(register_id=register_id).first()
        donations = Donation.objects.all().order_by('-donated_at')
        return render(request, "user/vi_donation.html", {"user": user, "donations": donations})


