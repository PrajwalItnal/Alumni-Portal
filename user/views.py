from django.shortcuts import render,redirect
from user.models import Event, User, Achievement, Job
from django.contrib import messages
from datetime import datetime
from .models import Donation
from .models import Internship
from .models import College




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
        description = request.POST.get('description', '').strip()
        location = request.POST.get('location', '').strip()
        salary = request.POST.get('salary', '').strip()
        last_date = request.POST.get('last_date', '').strip()
        required_skills = request.POST.get('required_skills', '').strip()

        
        if not all([title, company_name, description, location, last_date, required_skills]):
            messages.error(request, "❌ Please fill all required fields.")
            return redirect('user:add_job')

       
        if len(title) < 3:
            messages.error(request, "❌ Job title must be at least 3 characters.")
            return redirect('user:add_job')

        try:
            last_date_obj = datetime.strptime(last_date, "%Y-%m-%d").date()
            if last_date_obj < datetime.today().date():
                messages.error(request, "❌ Last date cannot be in the past.")
                return redirect('user:add_job')
        except ValueError:
            messages.error(request, "❌ Invalid date format.")
            return redirect('user:add_job')

        if salary and (not salary.isdigit() or int(salary) <= 0):
            messages.error(request, "❌ Salary must be a valid number greater than 0.")
            return redirect('user:add_job')

        if len(description.split()) < 5:
            messages.error(request, "❌ Description must be at least 5 words.")
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
    location_query = request.GET.get("loc", "").strip() # Matches name="loc"

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