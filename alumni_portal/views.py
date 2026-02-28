from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from user.models import User

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render

def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = "New Contact Message – Alumni Portal"

        body = f"""
            Dear Admin,

            You have received a new contact message from the Alumni Portal website.

            Name: {name}
            Email: {email}

            Message:
            {message}

            Thank you,
            Alumni Portal System
        """

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            ['junedfattekhan00@gmail.com'],  # Replace with your admin email
            fail_silently=False,
        )

        user_subject = "Thank You for Contacting Us – Alumni Portal"
        user_body = f"""
            Dear {name},

            Thank you for contacting the Alumni Portal.

            We have received your message and our team will get back to you as soon as possible.

            Here is a copy of your message:

            {message}

            Best Regards,
            Alumni Portal Team
        """

        send_mail(
            user_subject,
            user_body,
            settings.EMAIL_HOST_USER,
            [email],  # Send to user
            fail_silently=False,
        )

        return render(request, "contact.html", {"success": True})

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