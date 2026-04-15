from io import BytesIO

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
import user
from user.models import Event, User, Achievement, Job, Student
from django.contrib import messages
from datetime import date, datetime, timedelta
from .models import Alumni, Department, Donation
from .models import Internship
import pandas as pd
import random
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage, get_connection, send_mail
import openpyxl
from django.core.validators import URLValidator

def get_session_user(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return None
    return User.objects.filter(register_id=register_id).first()

def is_valid_text(text):
    if not text:
        return False
    text = str(text)
    clean_text = text.replace(" ", "").replace("\r", "").replace("\n", "").replace(".", "").replace(",", "").replace("'", "").replace("\"", "").replace(":", "").replace(";", "").replace("-", "").replace("_", "").replace("+", "").replace("=", "").replace("*", "").replace("/", "").replace("%", "").replace("^", "").replace("&", "").replace("#", "").replace("@", "").replace("$", "").replace("!", "").replace("?", "").replace("<", "").replace(">", "").replace("|", "").replace("\\", "").replace("~", "").replace("`", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("|", "").replace("\\", "").replace("~", "").replace("`", "")
    return clean_text.isalpha()

def home(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    if user.role == "Admin":
        return render(request, "user/admin_home.html", {"user": user})
    elif user.role == "Alumni":
        return render(request, "user/alumni_home.html", {"user": user})
    else:
        return render(request, "user/user_home.html", {"user": user})

def vi_event(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    today = datetime.now().date()
    events = Event.objects.filter(date__gte=today).order_by("-created_at")
    return render(request, "user/vi_event.html", {"user": user, "events": events})
    
def create_event(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")

    if user.role != "Alumni" and user.role != "Admin":
        messages.error(request, "You do not have permission to edit this event.")
        return redirect("user:vi_event")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        event_type = request.POST.get("event_type")
        date = request.POST.get("date")
        time = request.POST.get("event_time")
        location = request.POST.get("location")
        image = request.FILES.get("image")

        try:
            event_date = datetime.strptime(date, "%Y-%m-%d").date()
            today = datetime.now().date()
            max_limit = today + timedelta(days=60)

            if event_date <= today or event_date > max_limit:
                messages.error(request, f"Select a date between tomorrow and {max_limit}.")
                return render(request, "user/create_event.html", {"user": user, "data": request.POST})
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid date.")
            return render(request, "user/create_event.html", {"user": user, "data": request.POST})

        if image:
            if image.size > 2 * 1024 * 1024:
                messages.error(request, "Image size should not exceed 2MB.")
                return render(request, "user/create_event.html", {"user": user, "data": request.POST})
        
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                messages.error(request, "Invalid image format: Only JPG, JPEG, and PNG files are allowed.")
                return render(request, "user/create_event.html", {"user": user, "data": request.POST})
        
        if not is_valid_text(title) or not is_valid_text(description) or not is_valid_text(location):
            messages.error(request, "Title, Description, and Location must contain only alphabets and spaces.")
            return render(request, "user/create_event.html", {"user": user, "data": request.POST})

        Event.objects.create(
            title=title, 
            description=description, 
            event_type=event_type, 
            date=date, 
            event_time=time, 
            location=location, 
            image=image,
            organized_by=user
        )
        messages.success(request, "Event created successfully!")
        return redirect("user:vi_event")
    return render(request, "user/create_event.html", {"user": user})
    
def delete_event(request, event_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    event = get_object_or_404(Event, id=event_id)

    if event.organized_by == user or user.role == "Admin":
        event.delete()
        messages.success(request, "Event deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this event.")
    
    return redirect("user:vi_event")

def edit_event(request, event_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    event = get_object_or_404(Event, id=event_id)

    if event.organized_by != user and user.role != "Admin":
        messages.error(request, "You do not have permission to edit this event.")
        return redirect("user:vi_event")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        event_type = request.POST.get("event_type")
        location = request.POST.get("location")
        date = request.POST.get("date")
        time = request.POST.get("event_time")

        try:
            event_date = datetime.strptime(date, "%Y-%m-%d").date()
            today = datetime.now().date()
            max_limit = today + timedelta(days=60)
            if event_date <= today or event_date > max_limit:
                messages.error(request, f"Select a date between tomorrow and {max_limit}.")
                return render(request, "user/create_event.html", {"user": user, "data": request.POST})
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid date.")
            return render(request, "user/create_event.html", {"user": user, "data": request.POST})
        
        new_image = request.FILES.get("image")
        if new_image:
            event.image = new_image

        if not is_valid_text(title) or not is_valid_text(description) or not is_valid_text(location):
            messages.error(request, "Title, Description, and Location must contain only alphabets and spaces.")
            return render(request, "user/create_event.html", {"user": user, "data": request.POST})
        
        event.title = title
        event.description = description
        event.event_type = event_type
        event.location = location
        event.date = date
        event.event_time = time
        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect("user:vi_event")

    return render(request, "user/create_event.html", {"user": user, "data": event})

def view_achievements(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    achievements = Achievement.objects.all().order_by('created_at')
    return render(request, "user/view_achievement.html", {"user": user, "achievements": achievements})

def create_achievements(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")

    if user.role != "Alumni" and user.role != "Admin":
        messages.error(request, "You do not have permission to add achievements.")
        return redirect("user:achievements_view")

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        certificate = request.FILES.get('certificate')

        if not is_valid_text(title) or not is_valid_text(description):
            messages.error(request, "Title and Description should only contain letters and spaces.")
            return render(request, "user/create_achievement.html", {"user": user, "data": request.POST})
        
        if not title or not description:
            messages.error(request, "Title and Description cannot be empty.")
            return render(request, "user/create_achievement.html", {"user": user, "data": request.POST})
        
        if len(description.split()) < 5:
            messages.error(request, "Description must be at least 5 words.")
            return render(request, "user/create_achievement.html", {"user": user, "data": request.POST})

        if certificate:
            if certificate.size > 5 * 1024 * 1024:
                messages.error(request, "Certificate file size should not exceed 5MB.")
                return render(request, "user/create_achievement.html", {"user": user, "data": request.POST})
            
            valid_extensions = ('.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx')
            if not certificate.name.lower().endswith(valid_extensions):
                messages.error(request, "Invalid format: Only PDF, JPG, JPEG, PNG, DOC, and DOCX are allowed.")
                return render(request, "user/create_achievement.html", {"user": user, "data": request.POST})

        Achievement.objects.create(
            achieved_by = user,
            title = title,
            description = description,
            certificate = certificate
        )
        messages.success(request, "Achievement added successfully")
        return redirect('user:achievements_view')
    
    return render(request, "user/create_achievement.html", {"user": user})

def edit_achievement(request, achievement_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    achievement = get_object_or_404(Achievement, id=achievement_id)

    if achievement.achieved_by != user and user.role != "Admin":
        messages.error(request, "You do not have permission to edit this achievement.")
        return redirect("user:achievements_view")

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        certificate = request.FILES.get('certificate')

        if not is_valid_text(title) or not is_valid_text(description):
            messages.error(request, "Title and Description should only contain letters and spaces.")
            return render(request, "user/create_achievement.html", {"data": achievement, "user": user})

        if certificate:
            if certificate.size > 5 * 1024 * 1024:
                messages.error(request, "Certificate file size should not exceed 5MB.")
                return render(request, "user/create_achievement.html", {"data": achievement, "user": user})
            
            valid_extensions = ('.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx')
            if not certificate.name.lower().endswith(valid_extensions):
                messages.error(request, "Invalid format: Only PDF, JPG, JPEG, PNG, DOC, and DOCX are allowed.")
                return render(request, "user/create_achievement.html", {"data": achievement, "user": user})
            
            achievement.certificate = certificate

        if not title or not description:
            messages.error(request, "Title and Description cannot be empty.")
            return render(request, "user/create_achievement.html", {"data": achievement, "user": user})
            
        if len(description.split()) < 5:
            messages.error(request, "Description must be at least 5 words.")
            return render(request, "user/create_achievement.html", {"data": achievement, "user": user})

        achievement.title = title
        achievement.description = description
        achievement.save()
        
        messages.success(request, "Achievement updated successfully!")
        return redirect('user:achievements_view')

    return render(request, "user/create_achievement.html", {"data": achievement, "user": user})

def delete_achievement(request, achievement_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    achievement = get_object_or_404(Achievement, id=achievement_id)

    if achievement.achieved_by == user or user.role == "Admin":
        achievement.delete()
        messages.success(request, "Achievement deleted successfully.")
    else:
        messages.error(request, "Unauthorized action.")
        
    return redirect("user:achievements_view")

def create_donation(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")

    if user.role != "Alumni" and user.role != "Admin":
        messages.error(request, "You do not have permission to add donations.")
        return redirect("user:donation_list")

    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        description = request.POST.get('description')

        try:
            if int(amount) < 1000:
                messages.error(request, "Amount must be at least 1000.")
                return render(request, 'user/add_donation.html', {"user": user, 'data': request.POST})
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid amount.")
            return render(request, 'user/add_donation.html', {"user": user, 'data': request.POST})
        
        if not is_valid_text(description):
            messages.error(request, "Description should only contain alphabets and spaces.")
            return render(request, 'user/add_donation.html', {"user": user, 'data': request.POST})

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
    user = get_session_user(request)
    if not user:
        return redirect("login")
    donations = Donation.objects.all().order_by('-donated_at')
    return render(request, "user/vi_donation.html", {"user": user, "donations": donations})

def edit_donation(request, donation_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    donation = get_object_or_404(Donation, id=donation_id)

    if donation.donated_by != user and user.role != "Admin":
        messages.error(request, "You do not have permission to edit this donation.")
        return redirect("user:donation_list")

    if request.method == "POST":
        amount_raw = request.POST.get("amount")

        try:
            amount = int(float(amount_raw))
            if amount < 1000 or amount > 100000:
                messages.error(request, "Amount must be between 1000 and 100000.")
                return render(request, 'user/add_donation.html', {"user": user, "data": donation})
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid numeric amount.")
            return render(request, 'user/add_donation.html', {"user": user, "data": donation})
        
        description = request.POST.get("description")
        if not is_valid_text(description):
            messages.error(request, "Description should only contain alphabets and spaces.")
            return render(request, 'user/add_donation.html', {"user": user, 'data': request.POST})

        donation.amount = amount
        donation.payment_method = request.POST.get("payment_method")
        donation.description = description
        donation.save()
        
        messages.success(request, "Donation updated successfully!")
        return redirect("user:donation_list")

    return render(request, "user/add_donation.html", {"user": user, "data": donation})

def delete_donation(request, donation_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    donation = get_object_or_404(Donation, id=donation_id)

    if donation.donated_by == user or user.role == "Admin":
        donation.delete()
        messages.success(request, "Donation record deleted.")
    else:
        messages.error(request, "Unauthorized action.")
        
    return redirect("user:donation_list")

def view_job(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    jobs = list(Job.objects.all().order_by('-posted_at'))
    
    if user.role == "Student":
        user_skills = [s.strip().lower() for s in user.student_profile.skills.split(",")] if user.student_profile.skills else []
        for job in jobs:
            job_skills = [j.strip().lower() for j in job.required_skills.split(",")] if job.required_skills else []
            job.matched_skills = len(set(user_skills) & set(job_skills))

        jobs.sort(key=lambda x: x.matched_skills, reverse=True)

    return render(request, "user/view_job.html", {"user": user, "jobs": jobs})
    
def add_job(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    if user.role != "Alumni" and user.role != "Admin":
        messages.error(request, "You do not have permission to post jobs.")
        return redirect("user:view_job")

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        company_name = request.POST.get('c_name', '').strip()
        description = request.POST.get('description', '').strip()
        location = request.POST.get('location', '').strip()
        salary = request.POST.get('salary', '').strip()
        last_date = request.POST.get('last_date', '').strip()
        required_skills = request.POST.get('required_skills', '').strip()
        apply_link = request.POST.get('apply_link', '').strip()

        if not is_valid_text(company_name) or not is_valid_text(location) or not is_valid_text(title):
            messages.error(request, "Title, Company, and Location should contain only alphabets and spaces.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})
        
        if not all([title, company_name, description, location, last_date, required_skills]):
            messages.error(request, "Please fill all required fields.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        try:
            last_date_obj = datetime.strptime(last_date, "%Y-%m-%d").date()
            today = datetime.today().date()
            if last_date_obj < today:
                messages.error(request, "Last date cannot be in the past.")
                return render(request, "user/add_job.html", {"user": user, "data": request.POST})
            if last_date_obj > today + timedelta(days=60):
                messages.error(request, "Last date must be within 2 months from today.")
                return render(request, "user/add_job.html", {"user": user, "data": request.POST})
        except ValueError:
            messages.error(request, "Invalid date format.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        if salary and (not salary.isdigit() or int(salary) <= 0):
            messages.error(request, "Salary must be a valid number greater than 0.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        if len(description.split()) < 5:
            messages.error(request, "Description must be at least 5 words.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})
        
        validate = URLValidator()
        try:
            validate(apply_link)
        except ValidationError:
            messages.error(request, "Please enter a valid URL for the Apply Link (e.g., https://...)")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        Job.objects.create(
            posted_by=user,
            company_name=company_name,
            title=title,
            description=description,
            location=location,
            salary=salary,
            last_date=last_date,
            required_skills=required_skills,
            application_link=apply_link
        )
        messages.success(request, "Job posted successfully!")
        return redirect('user:view_job')

    return render(request, "user/add_job.html", {"user": user})

def filter_job(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")

    jobs = Job.objects.all()
    title_query = request.GET.get("title", "").strip()
    location_query = request.GET.get("loc", "").strip() 

    if title_query:
        jobs = jobs.filter(title__icontains=title_query)
    if location_query:
        jobs = jobs.filter(location__icontains=location_query)

    jobs = jobs.order_by('-posted_at')
    return render(request, "user/view_job.html", {"user": user, "jobs": jobs})

def edit_job(request, job_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    job = get_object_or_404(Job, id=job_id)

    if job.posted_by != user and user.role != "Admin":
        messages.error(request, "You do not have permission to edit this job.")
        return redirect("user:view_job")

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        company_name = request.POST.get('c_name', '').strip()
        description = request.POST.get('description', '').strip()
        location = request.POST.get('location', '').strip()
        salary = request.POST.get('salary', '').strip()
        last_date = request.POST.get('last_date', '').strip()
        required_skills = request.POST.get('required_skills', '').strip()
        apply_link = request.POST.get('apply_link', '').strip()

        if not is_valid_text(title) or not is_valid_text(company_name) or not is_valid_text(location) or not is_valid_text(description):
            messages.error(request, "All text fields must contain only alphabets and spaces.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        if not all([title, company_name, description, location, last_date, required_skills, apply_link]):
            messages.error(request, "Please fill all required fields.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        try:
            last_date_obj = datetime.strptime(last_date, "%Y-%m-%d").date()
            today = datetime.today().date()
            if last_date_obj < today:
                messages.error(request, "Last date cannot be in the past.")
                return render(request, "user/add_job.html", {"user": user, "data": request.POST})
            if last_date_obj > today + timedelta(days=60):
                messages.error(request, "Last date must be within 2 months from today.")
                return render(request, "user/add_job.html", {"user": user, "data": request.POST})
        except ValueError:
            messages.error(request, "Invalid date format.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        if salary and (not salary.isdigit() or int(salary) <= 0):
            messages.error(request, "Salary must be a valid number greater than 0.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        if len(description.split()) < 5:
            messages.error(request, "Description must be at least 5 words.")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        validate = URLValidator()
        try:
            validate(apply_link)
        except ValidationError:
            messages.error(request, "A valid Apply Link is compulsory (e.g., https://...).")
            return render(request, "user/add_job.html", {"user": user, "data": request.POST})

        job.title = title
        job.company_name = company_name
        job.description = description
        job.location = location
        job.salary = salary
        job.last_date = last_date
        job.required_skills = required_skills
        job.application_link = apply_link
        job.save()
        
        messages.success(request, "Job updated successfully!")
        return redirect('user:view_job')

    return render(request, "user/add_job.html", {"data": job, "user": user})

def delete_job(request, job_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    job = get_object_or_404(Job, id=job_id)

    if job.posted_by == user or user.role == "Admin":
        job.delete()
        messages.success(request, "Job listing deleted.")
    else:
        messages.error(request, "Unauthorized action.")
        
    return redirect("user:view_job")

def logout(request):
    request.session.flush()
    return redirect('home')

def internship_list(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    internships = Internship.objects.all().order_by('-posted_at')
    return render(request, 'user/view_internship.html', {'internships': internships, 'user': user})

def internship_create(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")

    if user.role not in ["Admin", "Alumni"]:
        messages.error(request, "You are not authorized to post internships.")
        return redirect("user:internship_list")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        company_name = request.POST.get("company_name", "").strip()
        description = request.POST.get("description", "").strip()
        location = request.POST.get("location", "").strip()
        stipend = request.POST.get("stipend")
        duration = request.POST.get("duration")
        last_date_raw = request.POST.get("last_date")
        required_skills = request.POST.get("required_skills")

        if not is_valid_text(title) or not is_valid_text(company_name) or not is_valid_text(location) or not is_valid_text(description):
            messages.error(request, "Title, Company, Location, and Description must contain only alphabets and spaces.")
            return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})

        try:
            last_date = datetime.strptime(last_date_raw, "%Y-%m-%d").date()
            today = datetime.now().date()
            if last_date <= today:
                messages.error(request, "The application deadline must be a future date.")
                return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
            if last_date > today + timedelta(days=60):
                messages.error(request, "The application deadline must be within 2 months from today.")
                return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format. Please use the date picker.")
            return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
            
        if stipend:
            try:
                if float(stipend) < 0:
                    messages.error(request, "Stipend cannot be negative.")
                    return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
            except ValueError:
                messages.error(request, "Stipend must be a valid number.")
                return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
        
        if len(description.split()) < 5:
            messages.error(request, "Description must be at least 5 words.")
            return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})

        Internship.objects.create(
            posted_by=user,
            title=title,
            company_name=company_name,
            description=description,
            location=location,
            stipend=stipend or None,
            duration=duration or None,
            last_date=last_date,
            required_skills=required_skills,
        )
        messages.success(request, "Internship posted successfully!")
        return redirect("user:internship_list")

    return render(request, "user/create_internship.html", {'user': user})

def internship_edit(request, internship_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    internship = get_object_or_404(Internship, id=internship_id)

    if internship.posted_by != user and user.role != "Admin":
        messages.error(request, "You are not authorized to edit this internship.")
        return redirect("user:internship_list")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        company_name = request.POST.get("company_name", "").strip()
        description = request.POST.get("description", "").strip()
        location = request.POST.get("location", "").strip()
        stipend = request.POST.get("stipend", "").strip()
        duration = request.POST.get("duration", "").strip()
        last_date_raw = request.POST.get("last_date")
        required_skills = request.POST.get("required_skills", "").strip()

        if not is_valid_text(title) or not is_valid_text(company_name) or not is_valid_text(location) or not is_valid_text(description):
            messages.error(request, "Title, Company, Location, and Description must contain only alphabets and spaces.")
            return render(request, "user/create_internship.html", {'user': user, 'data': internship})

        try:
            last_date_obj = datetime.strptime(last_date_raw, "%Y-%m-%d").date()
            today = datetime.now().date()
            if last_date_obj <= today:
                messages.error(request, "The application deadline must be a future date.")
                return render(request, "user/create_internship.html", {'user': user, 'data': internship})
            if last_date_obj > today + timedelta(days=60):
                messages.error(request, "The application deadline must be within 2 months from today.")
                return render(request, "user/create_internship.html", {'user': user, 'data': internship})
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format.")
            return render(request, "user/create_internship.html", {'user': user, 'data': internship})

        if stipend:
            try:
                if float(stipend) < 0:
                    messages.error(request, "Stipend cannot be negative.")
                    return render(request, "user/create_internship.html", {'user': user, 'data': internship})
            except ValueError:
                messages.error(request, "Stipend must be a valid number.")
                return render(request, "user/create_internship.html", {'user': user, 'data': internship})

        if len(description.split()) < 5:
            messages.error(request, "Description must be at least 5 words.")
            return render(request, "user/create_internship.html", {'user': user, 'data': internship})

        internship.title = title
        internship.company_name = company_name
        internship.description = description
        internship.location = location
        internship.stipend = stipend or None
        internship.duration = duration or None
        internship.last_date = last_date_obj
        internship.required_skills = required_skills
        internship.save()
        
        messages.success(request, "Internship updated successfully!")
        return redirect("user:internship_list")

    return render(request, "user/create_internship.html", {'user': user, 'data': internship})

def internship_delete(request, internship_id):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    internship = get_object_or_404(Internship, id=internship_id)

    if internship.posted_by == user or user.role == "Admin":
        internship.delete()
        messages.success(request, "Internship deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
        
    return redirect("user:internship_list")

def filter_internship(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")

    title = request.GET.get('title', '')
    loc = request.GET.get('loc', '')

    internships = Internship.objects.all().order_by('-posted_at')
    message = ''

    if title:
        internships = internships.filter(title__icontains=title)
    if loc:
        internships = internships.filter(location__icontains=loc)

    if not internships.exists():
        if title and loc:
            title_exists = Internship.objects.filter(title__icontains=title).exists()
            location_exists = Internship.objects.filter(location__icontains=loc).exists()
            if title_exists and not location_exists:
                message = f'"{title}" is available but not found in "{loc}" location.'
            elif location_exists and not title_exists:
                message = f'internship in "{loc}" are available but no title matching "{title}".'
            elif not title_exists and not location_exists:
                message = f'No internships found for "{title}" in "{loc}".'

    return render(request, 'user/view_internship.html', {
        'internships': internships,
        'user': user,
        'searched': True,
        'title': title,
        'loc': loc,
        'message': message
    })
    
def student_register(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")

    if user.role != "Admin":
        messages.error(request, "You do not have permission to access this page.")
        return redirect("user:admin_home")

    departments = Department.objects.all()
    if request.method == "POST":
        registration_type = request.POST.get("registration_type")
        
        if registration_type == "single":
            register_id = request.POST.get("register_id", "").strip()
            name = request.POST.get("name", "").strip()
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()
            gender = request.POST.get("gender", "").lower()
            course_duration = int(request.POST.get("duration"))
            department = request.POST.get("department")

            if not register_id:
                messages.error(request, "Register ID is required.")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})

            if not is_valid_text(register_id):
                messages.error(request, "Invalid Register ID: numbers are not allowed.")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})

            if len(register_id) > 14:
                messages.error(request, "Register ID is too long (max 14 characters).")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})

            if not is_valid_text(name):
                messages.error(request, "Invalid name: only letters and spaces allowed (numbers not allowed).")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})
            
            if len(name) < 3:
                messages.error(request, "Name is too short (min 3 characters).")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})

            if User.objects.filter(register_id=register_id).exists():
                messages.error(request, "Register ID already exists.")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})

            if not email.endswith("@gmail.com"):
                messages.error(request, "Invalid email domain (must be @gmail.com).")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})

            if not phone.isdigit() or len(phone) != 10:
                messages.error(request, "Invalid phone number: must be 10 digits.")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})

            password = random.randint(1000000000, 9999999999)
            try:
                user = User.objects.create(
                    register_id=register_id,
                    username=name.title(),
                    email=email,
                    role="Student",
                    password=make_password(str(password))
                )
                Student.objects.create(
                    user=user,
                    department=department,
                    admission_year=datetime.now().year,
                    graduation_year=datetime.now().year + course_duration,
                    phone=phone,
                    gender=gender
                )
                
                send_mail(
                    "Welcome to Alumni Portal",
                    f"Your account has been created successfully! Your login credentials are:\n\nRegister ID: {register_id}\nPassword: {password}\n\nPlease change your password after logging in.",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f"Student {name} registered successfully! Credentials sent to {email}.")
                return redirect("user:student_register")
            except Exception as e:
                messages.error(request, f"Error creating student: {str(e)}")
                return render(request, "user/student_registration.html", {"departments": departments, "data": request.POST})

        # Bulk Registration Logic
        file = request.FILES.get("file")
        course_duration = int(request.POST.get("duration"))
        department = request.POST.get("department")
        email_messages = []

        try:

            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file, engine='openpyxl')
        except Exception as e:
            messages.error(request, "Error reading file: " + str(e))
            return redirect("user:student_register")

        if course_duration >= 5:
            messages.error(request, "Course duration must be less than 5 years.")
            return redirect("user:student_register")
        
        required_columns = ['register id', "name", "email", "phone", "gender"]

        df.columns = df.columns.str.lower().str.strip()

        for column in required_columns:
            if column not in df.columns:
                messages.error(request, f"Columns are not present in the file. Required columns: {', '.join(required_columns)}")
                return redirect("user:student_register")
        
        failed_rows = []
        success_count = 0
        for index, row in df.iterrows():
            register_id = row['register id']
            name = row['name']
            email = row['email']
            phone = str(row['phone'])
            gender = row['gender']

            error_reason = None
            
            if not is_valid_text(register_id):
                error_reason = "Invalid Register ID: numbers are not allowed"
            elif User.objects.filter(register_id=register_id).exists():
                error_reason = "Register ID already exists"
            elif User.objects.filter(email=email).exists():
                error_reason = "Email already exists"
            elif not email.endswith("@gmail.com"):
                error_reason = "Invalid email domain (must be @gmail.com)"
            elif gender not in ['male', 'female']:
                error_reason = f"Invalid gender: {gender}"
            elif not phone.isdigit() or len(phone) != 10:
                error_reason = f"Invalid phone number: {phone}"
            elif not is_valid_text(name):
                error_reason = "Invalid username: only letters and spaces allowed (numbers not allowed)"
            elif len(name.strip()) < 3:
                error_reason = "Username too short (min 3 characters)"

            
            if error_reason:
                error_data = df.iloc[index].to_dict()
                error_data['error_reason'] = error_reason
                failed_rows.append(error_data)
                continue  

            password = random.randint(1000000000,9999999999)
            
            try:
                user = User.objects.create(
                    register_id=register_id,
                    username = name.strip().title(),
                    email = email,
                    role = "Student",
                    password = make_password(str(password))
                )
                
                student = Student.objects.create(
                    user = user,
                    department = department,
                    admission_year = datetime.now().year,
                    graduation_year = datetime.now().year + course_duration,
                    phone = phone,
                    gender = gender.lower().strip()
                )
                user.save()
                student.save()

                email_messages.append(EmailMessage(
                    "Welcome to Alumni Portal",
                    f"Your account has been created successfully! Your login credentials are:\n\nRegister ID: {register_id}\nPassword: {password}\n\nPlease change your password after logging in.",
                    settings.EMAIL_HOST_USER,
                    [email]
                ))
                success_count += 1
            except Exception as e:
                error_reason = str(e)
            
            if error_reason:
                error_data = df.iloc[index].to_dict()
                error_data['error_reason'] = error_reason
                failed_rows.append(error_data)
                continue
        if failed_rows:
            error_df = pd.DataFrame(failed_rows)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                error_df.to_excel(writer, index=False, sheet_name='Errors')
            
            output.seek(0)
            
            response = HttpResponse(
                output.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="registration_errors_{datetime.now()}.xlsx"'
            
            _send_registration_emails(email_messages)
            
            messages.warning(request, f"{success_count} students registered. Downloaded errors for {len(failed_rows)} rows.")
            return response
        _send_registration_emails(email_messages)
        messages.success(request, "Students registered successfully! Login credentials have been sent to their email addresses.")
        return redirect("user:student_register")

    return render(request, "user/student_registration.html", {"departments": departments})

def send_email(title, message, recipient_list):
    try:
        send_mail(
                title,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
            )
        return True
    except Exception as e:
        print(e)


def _send_registration_emails(email_messages):
    if not email_messages:
        return
    with get_connection() as connection:
        connection.send_messages(email_messages)


def change_user_email(request):
    user = get_session_user(request)
    if not user or user.role != 'Admin':
        messages.error(request, 'You do not have permission to change user details.')
        return redirect('user:home')

    if request.method == 'POST':
        target_register_id = request.POST.get('register_id', '').strip()
        new_email = request.POST.get('new_email', '').strip()
        new_password = request.POST.get('new_password', '').strip()

        if not target_register_id:
            messages.error(request, 'Register ID is required.')
            return render(request, 'user/change_user_email.html', {'user': user})

        try:
            target_user = User.objects.get(register_id=target_register_id)
        except User.DoesNotExist:
            messages.error(request, 'User with this register ID does not exist.')
            return render(request, 'user/change_user_email.html', {'user': user})

        if new_email:
            if User.objects.filter(email=new_email).exclude(register_id=target_register_id).exists():
                messages.error(request, 'This email is already in use by another user.')
                return render(request, 'user/change_user_email.html', {'user': user})

            from django.core.validators import validate_email
            try:
                validate_email(new_email)
                target_user.email = new_email
            except:
                messages.error(request, 'Please enter a valid email address.')
                return render(request, 'user/change_user_email.html', {'user': user})

        if new_password:
            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, 'user/change_user_email.html', {'user': user})
            target_user.password = make_password(new_password)

        if not new_email and not new_password:
            messages.error(request, 'Please provide either a new email or a new password to update.')
            return render(request, 'user/change_user_email.html', {'user': user})

        target_user.save()
        messages.success(request, f'Details for user {target_register_id} have been updated successfully.')
        return redirect('user:change_user_email')

    return render(request, 'user/change_user_email.html', {'user': user})


def convert_alumni(request):
    user = get_session_user(request)
    if not user or user.role != 'Admin':
        messages.error(request, 'You do not have permission to use this page.')
        return redirect('user:home')

    students = Student.objects.filter(graduation_year=datetime.now().year)
    current_graduators = students.filter(user__role="Student")
    if current_graduators.exists():
        return render(request, "user/convert_alumni.html", {'convert': True, 'year': datetime.now().year, 'current_graduators': current_graduators})
    else:
        return render(request, "user/convert_alumni.html", {'convert': False, 'year': datetime.now().year})

def convert_to_alumni(request):
    user = get_session_user(request)
    if not user or user.role != 'Admin':
        messages.error(request, 'You do not have permission to use this action.')
        return redirect('user:home')

    users = User.objects.filter(
        role = "Student",
        student_profile__graduation_year = datetime.now().year
    )
    count = users.count()
    for user in users:
        user.role = "Alumni"
        user.save()
        Alumni.objects.get_or_create(
            user = user
        )

        subject = "Welcome to Alumni Network 🎓"

        message = f"""
Dear {user.username},

Congratulations! 🎉

You have successfully graduated and are now part of our Alumni Network.

We are excited to keep you connected with our institution and fellow graduates.
You can now explore alumni features such as networking, job opportunities, and events.

We wish you all the best for your future career!

Best Regards,  
Alumni Portal Team
"""

        send_email(
            subject,
            message,
            [user.email]
        )

    messages.success(request, f"Students converted to alumni successfully! Total converted: {count}")
    return redirect("user:admin_home")

def change_password(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect("user:change_password")

        if len(new_password) < 8:
            messages.error(request, "New password must be at least 8 characters long.")
            return redirect("user:change_password")

        user.password = make_password(new_password)
        user.save(update_fields=["password"])

        messages.success(request, "Password changed successfully! Please log in again.")
        return redirect("login")

    return render(request, "user/change_password.html", {"user": user})

def update_profile_std(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    student = Student.objects.get(user=user) 

    if request.method == "POST":
        student.bio = request.POST.get("bio")
        student.phone = request.POST.get("phone")
        student.gender = request.POST.get("gender")
        student.github_url = request.POST.get("github_url")
        student.linkedin_url = request.POST.get("linkedin_url")
        student.city = request.POST.get("city")
        student.permanent_address = request.POST.get("permanent_address")
        if request.POST.get("dob"):
            student.dob = request.POST.get("dob")
        student.skills = request.POST.get("skills")

        if request.FILES.get("photo"):
            photo_ext = request.FILES.get("photo").name.split(".")[-1].lower()
            if photo_ext not in ["jpg", "jpeg", "png"]:
                messages.error(request, "Photo must be a JPG, JPEG, or PNG file.")
                return redirect("user:update_profile_std")
            student.photo = request.FILES.get("photo")

        if request.FILES.get("resume"):
            resume_ext = request.FILES.get("resume").name.split(".")[-1].lower()
            if resume_ext not in ["pdf", "doc", "docx"]:
                messages.error(request, "Resume must be a PDF or Word document.")
                return redirect("user:update_profile_std")
            student.resume = request.FILES.get("resume")
                       
        student.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("user:profile_view")
    return render(request, "user/update_profile.html", {"user": user, "student": student})


def profile_view(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    student = Student.objects.get(user=user)
    alumni = Alumni.objects.filter(user=user).first() if user.role == "Alumni" else None
    return render(request, "user/profile_view.html", {
        "user": user, 
        "student": student, 
        "alumni": alumni, 
        "skills_list": student.skills.split(",") if student.skills else []
    })

def alumni_update(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    
    alumni = get_object_or_404(Alumni, user=user)

    if request.method == "POST":
        alumni.employment_status = request.POST.get("employment_status")
        alumni.company_name = request.POST.get("company_name")
        alumni.job_title = request.POST.get("job_title")
        exp_year = request.POST.get("experience_year")
        alumni.experience_year = int(exp_year) if exp_year else None
        alumni.pursuing_degree = request.POST.get("pursuing_degree")
        alumni.university = request.POST.get("university")
        alumni.available_for_referral = bool(request.POST.get("available_for_referral"))
        alumni.save()
        messages.success(request, "The Alumni Data Updated Successfully")
        return redirect("user:profile_view")
    return render(request, "user/alumni_track.html", {"alumni": alumni, "user": user})


def alumni_directory(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    alumni_data = Alumni.objects.select_related('user', 'user__student_profile').all()
    return render(request, "user/alumni_directory.html", { "user": user, "alumni_data": alumni_data})

def student_directory(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    if user.role not in ["Admin", "Alumni"]:
        messages.error(request, "You are not authorized to view this page.")
        return redirect("user:home")
    students = Student.objects.select_related('user').filter(user__role="Student")
    return render(request, "user/student_directory.html", {"user": user, "students": students})

def alumni_career_track(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    if 'query' in request.session:
        del request.session['query']
    alumni = Alumni.objects.all().order_by('user__student_profile__graduation_year')
    return render(request, "user/alumni_career_track.html", {'user': user, 'alumni': alumni})

def search_career_track(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    query = request.POST.get('q',"").strip()
    request.session['query'] = query
    print(query)
    alumni = Alumni.objects.all().order_by('user__student_profile__graduation_year')
    alumni = alumni.filter(user__username__icontains = query) | alumni.filter(
        company_name__icontains = query
        ) | alumni.filter(
            job_title__icontains = query
            ) | alumni.filter(
                user__student_profile__graduation_year__icontains = query
                ) | alumni.filter(
                    pursuing_degree__icontains = query
                    )
    return render(request, "user/alumni_career_track.html", {'alumni' : alumni,'query' : query})

def download_career_track(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    query = ""
    if 'query' in request.session:
        query = request.session['query']
    print(query)
    alumni = Alumni.objects.all().order_by('user__student_profile__graduation_year')
    if query:
        alumni = alumni.filter(user__username__icontains = query) | alumni.filter(
            company_name__icontains = query
            ) | alumni.filter(
                job_title__icontains = query
                ) | alumni.filter(
                    user__student_profile__graduation_year__icontains = query
                    ) | alumni.filter(
                        pursuing_degree__icontains = query
                        )
    data = []
    for a in alumni:
        data.append({
            'RegNo' : a.user.register_id,
            'Name': a.user.username,
            'Company': a.company_name or "-",
            'Job Role': a.job_title or "-",
            'Experience': a.experience_year or 0,
            'Higher Studies': a.pursuing_degree or "-",
            'University': a.university or "-",
            'Referral': "Available" if a.available_for_referral else "Not Available"
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumni_report.csv"'

    df.to_csv(path_or_buf=response, index=False)

    return response

def alumni_directory_search(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    query = request.GET.get('q', '').strip()


    if query:
        alumni = Alumni.objects.select_related('user').filter(user__role = "Alumni")
        alumni_data = alumni.filter(
            Q(user__username__icontains=query) |
            Q(user__student_profile__department__icontains=query) |
            Q(user__student_profile__admission_year__icontains=query) |
            Q(user__student_profile__graduation_year__icontains=query) |
            Q(pursuing_degree__icontains=query) |
            Q(university__icontains=query) |
            Q(company_name__icontains=query) |
            Q(job_title__icontains=query)
        ).distinct()
    else:
        alumni_data = Alumni.objects.select_related('user').filter(user__role = "Alumni").all()

    context = {
        "user": user, 
        "alumni_data": alumni_data,
        "query": query  
    }
    return render(request, "user/alumni_directory.html", context)

def student_directory_search(request):
    user = get_session_user(request)
    if not user:
        return redirect("login")
    query = request.GET.get('q', '').strip()

    students = Student.objects.select_related('user').filter(user__role="Student")

    if query:
        students = students.filter(
            user__username__icontains=query  
        ) | students.filter(
            user__register_id__icontains=query  
        ) | students.filter(
            department__icontains=query  
        ) | students.filter(
            admission_year__icontains=query  
        ) | students.filter(
            graduation_year__icontains=query  
        )
        
        students = students.distinct()

    context = {
        "user": user,
        "students": students,
        "query": query
    }
    return render(request, "user/student_directory.html", context)

def department_list(request):
    user = get_session_user(request)
    if not user or user.role != 'Admin':
        messages.error(request, 'You do not have permission to view departments.')
        return redirect('user:home')

    departments = Department.objects.all()
    return render(request, 'user/department_list.html', {'departments': departments})

def add_department(request):
    user = get_session_user(request)
    if not user or user.role != 'Admin':
        messages.error(request, 'You do not have permission to add departments.')
        return redirect('user:home')

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, "Department name cannot be empty.")
            return redirect('user:department_list')

        if Department.objects.filter(name__iexact=name).exists():
            messages.error(request, f"Department '{name}' already exists.")
            return redirect('user:department_list')

        Department.objects.create(name=name)
        messages.success(request, f"Department '{name}' added successfully!")
    return redirect('user:department_list')

def edit_department(request, dept_id):
    user = get_session_user(request)
    if not user or user.role != 'Admin':
        messages.error(request, 'You do not have permission to edit departments.')
        return redirect('user:home')

    dept = get_object_or_404(Department, dept_id=dept_id)
    students = Student.objects.filter(department=dept.name)

    if request.method == "POST":
        new_name = request.POST.get('name', '').strip()

        if not new_name:
            messages.error(request, "Department name cannot be empty.")
            return redirect('user:department_list')

        if Department.objects.filter(name__iexact=new_name).exclude(dept_id=dept_id).exists():
            messages.error(request, "A department with this name already exists.")
            return redirect('user:department_list')

        dept.name = new_name
        dept.save()

        if students.exists():
            students.update(department=new_name)

        messages.success(request, "Department updated successfully.")
    return redirect('user:department_list')

def delete_department(request, dept_id):
    user = get_session_user(request)
    if not user or user.role != 'Admin':
        messages.error(request, 'You do not have permission to delete departments.')
        return redirect('user:home')

    dept = get_object_or_404(Department, dept_id=dept_id)

    if request.method == "POST":
        Student.objects.filter(department=dept.name).update(department="")
        dept.delete()
        messages.success(request, "Department deleted successfully.")
    return redirect('user:department_list')
