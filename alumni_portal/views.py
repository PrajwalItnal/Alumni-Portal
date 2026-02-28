from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from user.models import User
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = "New Contact Form Submission | Alumni Portal"
        body = f"""
        Dear Administrator,

        A new message has been submitted through the Alumni Portal Contact Form.

        Contact Details:
        ----------------------------------------
        Name  : {name}
        Email : {email}
        ----------------------------------------

        Message:
        {message}

        Please review this inquiry and respond as appropriate.

        Best Regards,
        Alumni Portal System
        """

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            ['junedfattekhan00@gmail.com'],  # Replace with your admin email
            fail_silently=False,
        )

        user_subject = "Thank You for Contacting Alumni Portal"
        user_body = f"""
        Dear {name},

        Thank you for contacting the Alumni Portal.

        We have successfully received your message and appreciate you reaching out to us. 
        Our team will review your inquiry and respond as soon as possible.

        For your reference, here is a copy of your message:

        ----------------------------------------
        {message}
        ----------------------------------------

        If you have any additional information to share, feel free to reply to this email.

        Warm Regards,  
        Alumni Portal Team
        """

        send_mail(
            user_subject,
            user_body,
            settings.EMAIL_HOST_USER,
            [email],  # Send to user
            fail_silently=False,
        )
        messages.success(request, "Your message has been sent successfully! We will get back to you soon.")
        return redirect('contact')

    return render(request, "contact.html")


def login(request):
    if request.method == "POST":
        register_id = request.POST.get("register_id")
        password = request.POST.get("password")
        user = None
        try:
            user = User.objects.get(register_id=register_id, password=password)
            request.session["register_id"] = user.register_id
            return redirect('user:home')
        except User.DoesNotExist:
            messages.error(request, "Invalid register ID or password.")
            return redirect('login')
    return render(request, "login.html")