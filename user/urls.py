from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("admin_home/", views.home, name="admin_home"),
    path("alumni_home/", views.home, name="alumni_home"),
    path("user_home/", views.home, name="user_home"),
    path("events/view/", views.vi_event, name="vi_event"),
    path("events/create/", views.create_event, name="event_create"),
    path("achievements/view/", views.view_achievements, name = "achievements_view"),
    path("achievements/create/", views.create_achievements, name = "create_achievement"),
    path('donations/', views.donation_list, name='donation_list'),
    path('donations/create/', views.create_donation, name='create_donation'),
    path('jobs/', views.view_job, name='view_job'),
    path('jobs/filter/', views.filter_job, name='filter_job'),
    path('jobs/add/', views.add_job, name='add_job'),
    path("internships/", views.internship_list, name="internship_list"),
    path("internships/create/", views.internship_create, name="internship_create"),
    path("internships/filter/", views.filter_internship, name="filter_internship"),
    path('college/create/', views.college_create, name='college_create'),
    path('college/list/',   views.college_list,   name='college_list'),
    path('college/detail/update/<int:college_id>/', views.college_detail_update, name='college_detail_update'),
    path('college/student/register/', views.student_register, name='student_register'),
    path('user/convert_alumni/', views.convert_alumni, name='convert_alumni'),
    path('user/convert_to_alumni/', views.convert_to_alumni, name='convert_to_alumni'),
    path('user/change_password/', views.change_password, name='change_password'),
    path('user/profile_update/', views.update_profile_std, name='update_profile_std'),
    path('user/profile_view/', views.profile_view, name='profile_view'),
    path("user/alumni/update_alumni", views.alumni_update, name = "alumni_update"),
    path('alumni-directory/', views.alumni_directory, name='alumni_directory'),
    path('student-directory/', views.student_directory, name='student_directory'),

]