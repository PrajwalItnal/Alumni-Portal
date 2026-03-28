from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect
import user
from user.models import Event, User, Achievement, Job, Student
from django.contrib import messages
from datetime import datetime, timedelta
from .models import Alumni, Donation
from .models import Internship
from .models import College
import pandas as pd
import random
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import openpyxl


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

        Job.objects.create(
            posted_by=user,
            company_name=company_name,
            title=title,
            description=description,
            location=location,
            salary=salary,
            last_date=last_date,
            required_skills=required_skills
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
        status = request.POST.get("status", "Open")

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
            status=status,
        )
        messages.success(request, "Internship posted successfully!")
        return redirect("user:internship_list")

    return render(request, "user/create_internship.html", {'user': user})

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


def college_list(request):
    if not College.objects.exists():
        return render(request, "user/college_create.html")
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)
    colleges = College.objects.all().order_by("-created_at")
    return render(request, "user/college_list.html", {
        "user": user,
        "colleges": colleges,
    })


def college_create(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    user = User.objects.get(register_id=register_id)
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        website = request.POST.get("website") or None
        established_year = request.POST.get("established_year") or None

        if College.objects.filter(email=email).exists():
            messages.error(request, "A college with this email already exists.")
            return redirect("user:college_create")

        College.objects.create(
            name=name,
            address=address,
            city=city,
            state=state,
            email=email,
            phone=phone,
            website=website,
            established_year=established_year,
        )
        messages.success(request, "College added successfully!")
        return redirect("user:college_list")

    return render(request, "user/college_create.html", {"user": user})


def college_detail_update(request, college_id):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")

    user = User.objects.get(register_id=register_id)
    college = College.objects.get(id=college_id)

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        website = request.POST.get("website")
        established_year = request.POST.get("established_year")

      
        if "@gmail.com" not in email:
            messages.error(request, "Enter valid gmail address")
            return redirect("user:college_detail_update", college_id=college.id)
        
        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Phone must be 10 digits")
            return redirect("user:college_detail_update", college_id=college.id)
    
        if established_year and len(established_year) != 4:
            messages.error(request, "Year must be 4 digits")
            return redirect("user:college_detail_update", college_id=college.id)
     
        if website and not website.startswith("http"):
            messages.error(request, "Website must start with http or https")
            return redirect("user:college_detail_update", college_id=college.id)
      
        college.name = name
        college.address = address
        college.city = city
        college.state = state
        college.email = email
        college.phone = phone
        college.website = website or None
        college.established_year = established_year or None
        college.save()

        messages.success(request, "College updated successfully!")
        return redirect("user:college_list")

    return render(request, "user/college_detail_update.html", {
        "user": user,
        "college": college,
    })
    
def student_register(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        admission_year = request.POST.get("adm_year")
        graduation_year = request.POST.get("grad_year")
        department = request.POST.get("department")

        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file, engine='openpyxl')
        except Exception as e:
            messages.error(request, "Error reading file: " + str(e))
            return redirect("user:student_register")

        if admission_year >= graduation_year:
            messages.error(request, "Admission year must be less than graduation year.")
            return redirect("user:student_register")
        
        required_columns = ['register id', "name", "email", "phone", "gender"]

        df.columns = df.columns.str.lower().str.strip()

        for column in required_columns:
            if column not in df.columns:
                messages.error(request, f"Columns are not present in the file. Required columns: {', '.join(required_columns)}")
                return redirect("user:student_register")
        
        for row in df.iterrows():
            register_id = row[1]['register id']
            name = row[1]['name']
            email = row[1]['email']
            phone = str(row[1]['phone'])
            gender = row[1]['gender']
            
            if User.objects.filter(register_id=register_id).exists() or User.objects.filter(email=email).exists():
                print(f"User with register ID {register_id} or email {email} already exists. Skipping.")
                continue

            if "@gmail.com" not in email:
                print(f"Invalid email {email} for register ID {register_id}. Skipping.")
                continue

            if gender.lower().lower() in ['male', 'female']:
                print(f"Invalid gender: {gender}")
                continue

            
            
            password = random.randint(1000000000,9999999999)
            print(f"Generated password for {register_id}: {password}")
            user = User.objects.create(
                register_id=register_id,
                username = name.strip().title(),
                email = email,
                role = "Student",
                password = make_password(str(password))
            )

            print(user)

            send_email(
                "Welcome to Alumni Portal",
                f"Your account has been created successfully! Your login credentials are:\n\nRegister ID: {register_id}\nPassword: {password}\n\nPlease change your password after logging in.",
                [email]
            )

            student = Student.objects.create(
                user = user,
                department = department,
                admission_year = admission_year,
                graduation_year = graduation_year,
                phone = phone,
                gender = gender.lower().strip()
            )

            user.save()
            student.save()
        messages.success(request, "Students registered successfully! Login credentials have been sent to their email addresses.")
        return redirect("user:admin_home")
    return render(request, "user/student_registration.html")

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

