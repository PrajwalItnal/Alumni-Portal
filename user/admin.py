from django.contrib import admin
from .models import User, Student, Alumni, Job, Event, Internship, Donation

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Alumni)
admin.site.register(Job)
admin.site.register(Event)
admin.site.register(Internship)
admin.site.register(Donation)