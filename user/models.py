from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STUDENT', 'Student'),
        ('ALUMNI', 'Alumni'),
    ]

    user_id = models.AutoField(primary_key=True)
    register_id = models.CharField(max_length=14, unique=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username
    

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="student_profile"
    )
    bio = models.CharField(max_length=250, blank=True, null=True)
    department = models.CharField(max_length=50)
    admission_year = models.IntegerField()
    graduation_year = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    city = models.CharField(max_length=20, blank=True)
    permanent_address = models.TextField()
    photo = models.FileField(
        upload_to="student_photos/",
        blank=True,
        null=True
    )
    resume = models.FileField(
        upload_to="student_resumes/",
        blank=True,
        null=True
    )
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "student"

    def __str__(self):
        return self.user.username



class Alumni(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="alumni_profile"
    )

    EMPLOYMENT_STATUS_CHOICES = [
        ("Employed", "Employed"),
        ("Unemployed", "Unemployed"),
        ("Higher Studies", "Higher Studies"),
    ]

    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS_CHOICES
    )

    company_name = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    experience_year = models.IntegerField(blank=True, null=True)
    pursuing_degree = models.CharField(max_length=150, blank=True)
    university = models.CharField(max_length=150, blank=True)
    willing_to_mentor = models.BooleanField(default=False)
    available_for_referral = models.BooleanField(default=False)

    class Meta:
        db_table = "alumni"

    def __str__(self):
        return self.user.username