from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from user.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
import random
from django.contrib.auth.hashers import check_password, make_password

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
        
        Name  : {name}
        Email : {email}
       

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
            ['junedfattekhan00@gmail.com'],  
            fail_silently=False,
        )

        user_subject = "Thank You for Contacting Alumni Portal"
        user_body = f"""
        Dear {name},

        Thank you for contacting the Alumni Portal.

        We have successfully received your message and appreciate you reaching out to us. 
        Our team will review your inquiry and respond as soon as possible.

        For your reference, here is a copy of your message:

        {message}
      

        If you have any additional information to share, feel free to reply to this email.

        Warm Regards,  
        Alumni Portal Team
        """

        send_mail(
            user_subject,
            user_body,
            settings.EMAIL_HOST_USER,
            [email],  
            fail_silently=False,
        )
        messages.success(request, "Your message has been sent successfully! We will get back to you soon.")
        return redirect('contact')

    return render(request, "contact.html")


def login(request):
    if request.method == "POST":
        register_id = request.POST.get("register_id")
        password = request.POST.get("password")
        user = User.objects.filter(register_id=register_id).first()
        print(user)
        print(password)
        print(check_password(password, user.password))
        if user is None:
            messages.error(request, "Invalid register ID or password.")
            return redirect('login')
        if check_password(password, user.password):
            request.session["register_id"] = user.register_id
            return redirect('user:home')
        else:
            messages.error(request, "Invalid register ID or password.")
            return redirect('login')
    return render(request, "login.html")

def reset_password(request):
    if request.method == "POST":
        user_otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        session_otp = request.session.get("otp")
        register_id = request.session.get("register_id")

        if str(user_otp) == str(session_otp):

            if new_password == confirm_password:

                User.objects.filter(register_id=register_id).update(password=make_password(str(new_password)))

                messages.success(request, "Password reset successfully")
                return redirect("login")

            else:
                messages.error(request, "Passwords do not match")
                return redirect("reset_password")

        else:
            messages.error(request, "Invalid OTP")
            return redirect("reset_password")
    return render(request, 'forgetpassword.html')
        

def send_otp(request):
    register_id = request.POST.get("register_id")
    try:
        user = User.objects.get(register_id = register_id)
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['register_id'] = register_id
        send_mail(
            "Forget Password",
            "Forget password in alumni portal the OTP is " + str(otp),
            settings.EMAIL_HOST_USER,
            [user.email], 
            fail_silently=False,
        )
        messages.success(request, "OTP sent successfully to your register email")
        return redirect('reset_password')
    except User.DoesNotExist:
        messages.error(request, "Enter the correct register id")
        return redirect('reset_password')
