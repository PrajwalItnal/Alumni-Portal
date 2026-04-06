import os
import django

# Set the settings module (update the name if your project folder is named differently)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_portal.settings')
django.setup()

from user.models import User, Student, Alumni, Department
from django.contrib.auth.hashers import make_password
from datetime import date

def create_user(username, role, register_id, email, password):
    user, created = User.objects.get_or_create(
        register_id=register_id,
        defaults={
            'username': username,
            'role': role,
            'email': email,
            'password': make_password(password)
        }
    )
    if not created:
        user.username = username
        user.role = role
        user.email = email
        user.password = make_password(password)
        user.save()
    return user

# Create Admin
admin = create_user('Test Admin', 'Admin', 'ADM001', 'admin@test.com', 'admin123')

# Create Departments
dept_cs, _ = Department.objects.get_or_create(name='Computer Science')
dept_is, _ = Department.objects.get_or_create(name='Information Science')

# Create Student
std_user = create_user('Test Student', 'Student', 'STD001', 'student@test.com', 'student123')
student, _ = Student.objects.get_or_create(
    user=std_user,
    defaults={
        'department': 'Computer Science',
        'admission_year': 2023,
        'graduation_year': 2027,
        'phone': '1234567890',
        'gender': 'Male',
        'dob': date(2005, 1, 1)
    }
)

# Create Alumni
alu_user = create_user('Test Alumni', 'Alumni', 'ALU001', 'alumni@test.com', 'alumni123')
alumni_std, _ = Student.objects.get_or_create(
    user=alu_user,
    defaults={
        'department': 'Information Science',
        'admission_year': 2019,
        'graduation_year': 2023,
        'phone': '0987654321',
        'gender': 'Female',
        'dob': date(2001, 1, 1)
    }
)
alumni_profile, _ = Alumni.objects.get_or_create(
    user=alu_user,
    defaults={
        'employment_status': 'Employed',
        'company_name': 'Test Corp',
        'job_title': 'Developer',
        'experience_year': 2,
        'pursuing_degree': 'None',
        'university': 'None',
        'available_for_referral': True
    }
)

print("Test users created/updated successfully.")
