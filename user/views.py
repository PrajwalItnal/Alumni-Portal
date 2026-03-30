from io import BytesIO

from django.conf import settings
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
import user
from user.models import Event, User, Achievement, Job, Student
from django.contrib import messages
from datetime import datetime, timedelta
from .models import Alumni, Department, Donation
from .models import Internship
import pandas as pd
import random
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import openpyxl
from django.core.validators import URLValidator


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

def vi_event(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        user = User.objects.get(register_id=register_id)
        today = datetime.now()
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
            
                if image and not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    messages.error(request, "Invalid image format: Only JPG, JPEG, and PNG files are allowed.")
                    return render(request, "user/create_event.html", {"user": user, "data": request.POST})
            
                check_fields = [title, description, event_type, location]
                if not all(x.replace(" ", "").isalpha() for x in check_fields):
                    messages.error(request, "Please use only alphabets and spaces for text fields.")
                    return render(request, "user/create_event.html", {"user": user, "data": request.POST})
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
    
def delete_event(request, event_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = get_object_or_404(User, register_id=register_id)
    event = get_object_or_404(Event, id=event_id)

    if event.organized_by == user or user.role == "Admin":
        event.delete()
        messages.success(request, "Event deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this event.")
    
    return redirect("user:vi_event")

def edit_event(request, event_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.get(register_id=register_id)
    event = get_object_or_404(Event, id=event_id)

    # Security: Only owner or Admin can edit
    if event.organized_by != user and user.role != "Admin":
        messages.error(request, "You do not have permission to edit this event.")
        return redirect("user:vi_event")

    if request.method == "POST":
        # Get data from form
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.event_type = request.POST.get("event_type")
        event.location = request.POST.get("location")
        event.date = request.POST.get("date")
        event.event_time = request.POST.get("event_time")
        
        # Check if a new image was uploaded
        new_image = request.FILES.get("image")
        if new_image:
            event.image = new_image
        
        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect("user:vi_event")

    # For GET request, we send the event object as 'data' to fill the form
    return render(request, "user/create_event.html", {"user": user, "data": event})

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

            if not all(x.replace(" ", "").isalpha() for x in [title, description]):
                messages.error(request, "Title and Description should only contain letters.")
                return render(request, "user/create_achievement.html", {"data": request.POST})
            
            if certificate:
                if certificate.size > 5 * 1024 * 1024:
                    messages.error(request, "Certificate file size should not exceed 5MB.")
                    return render(request, "user/create_achievement.html", {"data": request.POST})
                
                valid_extensions = ('.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx')
                if not certificate.name.lower().endswith(valid_extensions):
                    messages.error(request, "Invalid format: Only PDF, JPG, JPEG, PNG, DOC, and DOCX are allowed.")
                    return render(request, "user/create_achievement.html", {"data": request.POST})
            Achievement.objects.create(
                achieved_by = user,
                title = title,
                description = description,
                certificate = certificate
            )
            messages.success(request, "Achievement add successfully")
            return redirect('user:achievements_view')
    return render(request, "user/create_achievement.html")

def edit_achievement(request, achievement_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.filter(register_id=register_id).first()
    achievement = get_object_or_404(Achievement, id=achievement_id)

    # Permission Check: Only the person who achieved it or Admin can edit
    if achievement.achieved_by != user and user.role != "Admin":
        messages.error(request, "You do not have permission to edit this achievement.")
        return redirect("user:achievements_view")

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        certificate = request.FILES.get('certificate')

        # Validation logic (same as create)
        if not all(x.replace(" ", "").isalpha() for x in [title, description]):
            messages.error(request, "Title and Description should only contain letters.")
            return render(request, "user/create_achievement.html", {"data": achievement})

        achievement.title = title
        achievement.description = description
        
        if certificate:
            achievement.certificate = certificate
        
        achievement.save()
        messages.success(request, "Achievement updated successfully!")
        return redirect('user:achievements_view')

    # Pass existing achievement as 'data' to pre-fill the form
    return render(request, "user/create_achievement.html", {"data": achievement})

def delete_achievement(request, achievement_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.filter(register_id=register_id).first()
    achievement = get_object_or_404(Achievement, id=achievement_id)

    if achievement.achieved_by == user or user.role == "Admin":
        achievement.delete()
        messages.success(request, "Achievement deleted successfully.")
    else:
        messages.error(request, "Unauthorized action.")
        
    return redirect("user:achievements_view")

def create_donation(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")

    user = User.objects.filter(register_id=register_id).first()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        description = request.POST.get('description')

        if int(amount) < 0 or int(amount) < 1000:
            messages.error(request, "Amount must be a positive number and greater than 1000.")
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
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        user = User.objects.filter(register_id=register_id).first()
        donations = Donation.objects.all().order_by('-donated_at')
        return render(request, "user/vi_donation.html", {"user": user, "donations": donations})

def edit_donation(request, donation_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.filter(register_id=register_id).first()
    donation = get_object_or_404(Donation, id=donation_id)

    # Permission Check: Only owner or Admin
    if donation.donated_by != user and user.role != "Admin":
        messages.error(request, "You do not have permission to edit this donation.")
        return redirect("user:donation_list")

    if request.method == "POST":
        amount = request.POST.get("amount")
        
        # Validation
        if int(amount) < 1000:
            messages.error(request, "Amount must be at least 1000.")
            return render(request, 'user/add_donation.html', {"user": user, "data": donation})

        donation.amount = amount
        donation.payment_method = request.POST.get("payment_method")
        donation.description = request.POST.get("description")
        donation.save()
        
        messages.success(request, "Donation updated successfully!")
        return redirect("user:donation_list")

    # Send the existing donation as 'data' to pre-fill the form
    return render(request, "user/add_donation.html", {"user": user, "data": donation})

def delete_donation(request, donation_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.filter(register_id=register_id).first()
    donation = get_object_or_404(Donation, id=donation_id)

    if donation.donated_by == user or user.role == "Admin":
        donation.delete()
        messages.success(request, "Donation record deleted.")
    else:
        messages.error(request, "Unauthorized action.")
        
    return redirect("user:donation_list")

def view_job(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        user = User.objects.filter(register_id=register_id).first()
        jobs = Job.objects.all().order_by('-posted_at')
        return render(request, "user/view_job.html", {"user": user, "jobs": jobs})
    
def add_job(request):
    if request.method == 'POST':
        register_id = request.session.get("register_id")
        if not register_id:
            return redirect("login")
        
        user = User.objects.filter(register_id=register_id).first()

        title = request.POST.get('title', '').strip()
        company_name = request.POST.get('c_name', '').strip()
        if not company_name.isalpha():
            messages.error(request, "Please don't fill the except alphabets.")
            return redirect('user:add_job')

        description = request.POST.get('description', '').strip()
        location = request.POST.get('location', '').strip()
        if not location.isalpha():
            messages.error(request, "Please don't fill the except alphabets.")
            return redirect('user:add_job')
        salary = request.POST.get('salary', '').strip()
        last_date = request.POST.get('last_date', '').strip()
        required_skills = request.POST.get('required_skills', '').strip()
        apply_link = request.POST.get('apply_link', '').strip()

        
        if not all([title, company_name, description, location, last_date, required_skills]):
            messages.error(request, "Please fill all required fields.")
            return redirect('user:add_job')

       
        if len(title) < 3:
            messages.error(request, "Job title must be at least 3 characters.")
            return redirect('user:add_job')

        try:
            last_date_obj = datetime.strptime(last_date, "%Y-%m-%d").date()
            if last_date_obj < datetime.today().date():
                messages.error(request, "Last date cannot be in the past.")
                return redirect('user:add_job')
            if last_date_obj > datetime.today().date() + timedelta(days=60):
                messages.error(request, "Last date must be within 2 months from today.")
                return redirect('user:add_job')
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('user:add_job')

        if salary and (not salary.isdigit() or int(salary) <= 0):
            messages.error(request, "Salary must be a valid number greater than 0.")
            return redirect('user:add_job')

        if len(description.split()) < 5:
            messages.error(request, "Description must be at least 5 words.")
            return redirect('user:add_job')
        
        validate = URLValidator()
        try:
            validate(apply_link)
        except ValidationError:
            messages.error(request, "Please enter a valid URL for the Apply Link (e.g., https://...)")
            return render(request, "user/add_job.html", {"data": request.POST})

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

    return render(request, "user/add_job.html")

def filter_job(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")

    jobs = Job.objects.all()

    title_query = request.GET.get("title", "").strip()
    location_query = request.GET.get("loc", "").strip() 

    if title_query:
        jobs = jobs.filter(title__icontains=title_query)
        print(f"Filtering by title: {title_query}")

    if location_query:
        jobs = jobs.filter(location__icontains=location_query)
        print(f"Filtering by location: {location_query}")

    jobs = jobs.order_by('-posted_at')
    
    print(f"Jobs found: {jobs.count()}")

    user = User.objects.filter(register_id=register_id).first()
    return render(request, "user/view_job.html", {"user": user, "jobs": jobs})

def edit_job(request, job_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.filter(register_id=register_id).first()
    job = get_object_or_404(Job, id=job_id)

    # Permission Check
    if job.posted_by != user and user.role != "Admin":
        messages.error(request, "You do not have permission to edit this job.")
        return redirect("user:view_job")

    if request.method == 'POST':
        # Get data
        title = request.POST.get('title', '').strip()
        company_name = request.POST.get('c_name', '').strip()
        location = request.POST.get('location', '').strip()
        salary = request.POST.get('salary', '').strip()
        last_date = request.POST.get('last_date', '').strip()
        apply_link = request.POST.get('apply_link', '').strip()
        
        # Basic Validation (Alphabet check)
        if not (company_name.replace(" ","").isalpha() and location.replace(" ","").isalpha()):
            messages.error(request, "Company name and Location should only contain alphabets.")
            return render(request, "user/add_job.html", {"data": job})

        validate = URLValidator()
        try:
            if not apply_link: raise ValidationError("Required")
            validate(apply_link)
        except ValidationError:
            messages.error(request, "A valid Apply Link is compulsory.")
            return render(request, "user/add_job.html", {"data": job})

        # Update fields
        job.title = title
        job.company_name = company_name
        job.description = request.POST.get('description', '').strip()
        job.location = location
        job.salary = salary
        job.last_date = last_date
        job.required_skills = request.POST.get('required_skills', '').strip(),
        job.application_link = apply_link

        
        job.save()
        messages.success(request, "Job updated successfully!")
        return redirect('user:view_job')

    return render(request, "user/add_job.html", {"data": job})

def delete_job(request, job_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.filter(register_id=register_id).first()
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
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)
    internships = Internship.objects.all().order_by('-posted_at')
    return render(request, 'user/view_internship.html', {'internships': internships, 'user': user})

def internship_create(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)

    if user.role not in ["Admin", "Alumni"]:
        messages.error(request, "You are not authorized to post internships.")
        return redirect("user:internship_list")

    if request.method == "POST":
        title = request.POST.get("title")
        company_name = request.POST.get("company_name")
        description = request.POST.get("description")
        location = request.POST.get("location")
        stipend = request.POST.get("stipend")
        duration = request.POST.get("duration")
        last_date = request.POST.get("last_date")
        required_skills = request.POST.get("required_skills")

        try:
            last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
            if last_date <= datetime.now().date():
                messages.error(request, "The application deadline must be a future date.")
                return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
            if last_date > datetime.now().date() + timedelta(days=60):
                messages.error(request, "The application deadline must be within 2 months from today.")
                return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format. Please use the date picker.")
            return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
        
        text_check = {"Title": title, "Company": company_name, "Location": location}
        for field, value in text_check.items():
            if not value.replace(" ", "").isalpha():
                messages.error(request, f"{field} should only contain letters and spaces.")
                return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
            
        if stipend:
            try:
                if float(stipend) < 0:
                    messages.error(request, "Stipend cannot be negative.")
                    return render(request, "user/create_internship.html", {'user': user, 'data': request.POST})
            except ValueError:
                messages.error(request, "Stipend must be a valid number.")
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
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.get(register_id=register_id)
    internship = get_object_or_404(Internship, id=internship_id)

    # Permission Check
    if internship.posted_by != user and user.role != "Admin":
        messages.error(request, "You are not authorized to edit this internship.")
        return redirect("user:internship_list")

    if request.method == "POST":
        # Get data from POST
        internship.title = request.POST.get("title")
        internship.company_name = request.POST.get("company_name")
        internship.description = request.POST.get("description")
        internship.location = request.POST.get("location")
        internship.stipend = request.POST.get("stipend")
        internship.duration = request.POST.get("duration")
        internship.last_date = request.POST.get("last_date")
        internship.required_skills = request.POST.get("required_skills")

        # Basic Validation (Alphabet check for key fields)
        text_check = {"Title": internship.title, "Company": internship.company_name, "Location": internship.location}
        for field, value in text_check.items():
            if not value.replace(" ", "").isalpha():
                messages.error(request, f"{field} should only contain letters.")
                return render(request, "user/create_internship.html", {'user': user, 'data': internship})

        internship.save()
        messages.success(request, "Internship updated successfully!")
        return redirect("user:internship_list")

    return render(request, "user/create_internship.html", {'user': user, 'data': internship})

def internship_delete(request, internship_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.get(register_id=register_id)
    internship = get_object_or_404(Internship, id=internship_id)

    # Permission Check
    if internship.posted_by == user or user.role == "Admin":
        internship.delete()
        messages.success(request, "Internship deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this.")
        
    return redirect("user:internship_list")

def filter_internship(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)

    title = request.GET.get('title', '')
    loc = request.GET.get('loc', '')

    internships = Internship.objects.all().order_by('-posted_at')

    title_exists = False
    location_exists = False
    message = ''

    if title:
        title_exists = internships.filter(title__icontains=title).exists()

    if loc:
        location_exists = internships.filter(location__icontains=loc).exists()

    if title:
        internships = internships.filter(title__icontains=title)
    if loc:
        internships = internships.filter(location__icontains=loc)

    if not internships.exists():
        if title and loc:
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
    departments = Department.objects.all()
    if request.method == "POST":
        file = request.FILES.get("file")
        course_duration = int(request.POST.get("duration"))
        department = request.POST.get("department")

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
            
            if User.objects.filter(register_id=register_id).exists():
                error_reason = "Register ID already exists"
            elif User.objects.filter(email=email).exists():
                error_reason = "Email already exists"
            elif not email.endswith("@gmail.com"):
                error_reason = "Invalid email domain (must be @gmail.com)"
            elif gender not in ['male', 'female']:
                error_reason = f"Invalid gender: {gender}"
            elif not phone.isdigit() or len(phone) != 10:
                error_reason = f"Invalid phone number: {phone}"
            
            if error_reason:
                error_data = df.iloc[index].to_dict()
                error_data['error_reason'] = error_reason
                failed_rows.append(error_data)
                continue  

            password = random.randint(1000000000,9999999999)
            print(f"Generated password for {register_id}: {password}")
            
            try:
                send_mail(
                    "Welcome to Alumni Portal",
                    f"Your account has been created successfully! Your login credentials are:\n\nRegister ID: {register_id}\nPassword: {password}\n\nPlease change your password after logging in.",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
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
                success_count += 1
            except Exception as e:
                error_reason = str(e)
            
            if error_reason:
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
            
            messages.warning(request, f"{success_count} students registered. Downloaded errors for {len(failed_rows)} rows.")
            return response
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

def convert_alumni(request):
    students = Student.objects.filter(graduation_year=datetime.now().year)
    current_graduators = students.filter(user__role="Student")
    if current_graduators.exists():
        return render(request, "user/convert_alumni.html", {'convert': True, 'year': datetime.now().year, 'current_graduators': current_graduators})
    else:
        return render(request, "user/convert_alumni.html", {'convert': False, 'year': datetime.now().year})

def convert_to_alumni(request):
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
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")

    user = User.objects.get(register_id=register_id)

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
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)
    print(user)
    student = Student.objects.get(user=user) 
    print(student.resume.url if student.resume else "No resume")
    print(student)

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

        if request.FILES.get("photo"):
            photo = request.FILES.get("photo").name.split(".")[-1].lower()
            if photo not in ["jpg", "jpeg", "png"]:
                messages.error(request, "Photo must be a JPG, JPEG, or PNG file.")
                return redirect("user:update_profile_std")
            else:
                student.photo = request.FILES.get("photo")

        if request.FILES.get("resume"):
            resume = request.FILES.get("resume").name.split(".")[-1].lower()
            if resume not in ["pdf", "doc", "docx"]:
                messages.error(request, "Resume must be a PDF or Word document.")
                return redirect("user:update_profile_std")
            else:
                student.resume = request.FILES.get("resume")
                       
        student.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("user:profile_view")
    return render(request, "user/update_profile.html", {"user": user, "student": student})


def profile_view(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)
    student = Student.objects.get(user=user)
    alumni = None
    if user.role == "Alumni":
        alumni = Alumni.objects.get(user=user)
    return render(request, "user/profile_view.html", {"user": user, "student": student, "alumni": alumni})

def alumni_update(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)
    alumni = Alumni.objects.get(user = user)  
    if request.method == "POST":
        register_id = request.session.get("register_id")
        if not register_id:
            return redirect("login")
        user = User.objects.get(register_id=register_id)
        alumni = Alumni.objects.get(user = user)
        alumni.employment_status = request.POST.get("employment_status")
        alumni.job_title = request.POST.get("job_title")
        if request.POST.get("experience_year"):
            alumni.experience_year = int(request.POST.get("experience_year"))
        else:
            alumni.experience_year = None
        alumni.pursuing_degree = request.POST.get("pursuing_degree")
        alumni.university = request.POST.get("university")
        if request.POST.get("available_for_referral"):
            alumni.available_for_referral = True
        else:
            alumni.available_for_referral = False
        alumni.save()
        messages.success(request, "The Alumni Data Updated Sucessfully")
        return redirect("user:profile_view")
    return render(request, "user/alumni_track.html", {"alumni":alumni})


def alumni_directory(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)
    alumni_data = Alumni.objects.select_related('user', 'user__student_profile').all()
    return render(request, "user/alumni_directory.html", { "user": user, "alumni_data": alumni_data})

def student_directory(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)
    if user.role not in ["Admin", "Alumni"]:
        messages.error(request, "You are not authorized to view this page.")
        return redirect("user:home")
    students = Student.objects.select_related('user').filter(user__role="Student")
    return render(request, "user/student_directory.html", {"user": user, "students": students})

def alumni_career_track(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    if 'query' in request.session:
        del request.session['query']
    alumni = Alumni.objects.all().order_by('user__student_profile__graduation_year')
    print(alumni)
    return render(request, "user/alumni_career_track.html", {'alumni' : alumni})

def search_career_track(request):
    register_id = request.session.get("register_id")
    if not register_id:
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
    register_id = request.session.get("register_id")
    if not register_id:
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
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.get(register_id=register_id)
    query = request.GET.get('q', '').strip()

    if query:
        alumni_data = Alumni.objects.select_related('user', 'user__student_profile').filter(
            user__username__icontains=query  
        ) | Alumni.objects.select_related('user', 'user__student_profile').filter(
            user__student_profile__department__icontains=query  
        ) | Alumni.objects.select_related('user', 'user__student_profile').filter(
            user__student_profile__admission_year__icontains=query  
        ) | Alumni.objects.select_related('user', 'user__student_profile').filter(
            user__student_profile__graduation_year__icontains=query  
        ) | Alumni.objects.select_related('user', 'user__student_profile').filter(
            pursuing_degree__icontains=query  
        ) | Alumni.objects.select_related('user', 'user__student_profile').filter(
            university__icontains=query  
        ) | Alumni.objects.select_related('user', 'user__student_profile').filter(
            company_name__icontains=query  
        ) | Alumni.objects.select_related('user', 'user__student_profile').filter(
            job_title__icontains=query 
        )
        alumni_data = alumni_data.distinct()
    else:
        alumni_data = Alumni.objects.select_related('user', 'user__student_profile').all()

    context = {
        "user": user, 
        "alumni_data": alumni_data,
        "query": query  
    }
    return render(request, "user/alumni_directory.html", context)

def student_directory_search(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    
    user = User.objects.get(register_id=register_id)
    query = request.GET.get('q', '').strip()

    if query:
        students = Student.objects.select_related('user').filter(
            user__username__icontains=query  
        ) | Student.objects.select_related('user').filter(
            user__register_id__icontains=query  
        ) | Student.objects.select_related('user').filter(
            department__icontains=query  
        ) | Student.objects.select_related('user').filter(
            admission_year__icontains=query  
        ) | Student.objects.select_related('user').filter(
            graduation_year__icontains=query  
        )
        
        students = students.distinct()
    else:
        students = Student.objects.select_related('user').all()

    context = {
        "user": user,
        "students": students,
        "query": query
    }
    return render(request, "user/student_directory.html", context)

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'user/department_list.html', {'departments': departments})

def add_department(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Department.objects.create(name=name)
            messages.success(request, f"Department '{name}' added successfully!")
    return redirect('user:department_list')

def edit_department(request, dept_id):
    dept = get_object_or_404(Department, dept_id=dept_id)
    students = Student.objects.filter(department=dept.name)
    if request.method == "POST":
        new_name = request.POST.get('name')
        if new_name:
            dept.name = new_name
            students.update(department=new_name)
            students.save()
            dept.save()
            messages.success(request, "Department updated successfully.")
    return redirect('user:department_list')

def delete_department(request, dept_id):
    dept = get_object_or_404(Department, dept_id=dept_id)
    if request.method == "POST":
        dept.delete()
        messages.success(request, "Department deleted successfully.")
    return redirect('user:department_list')