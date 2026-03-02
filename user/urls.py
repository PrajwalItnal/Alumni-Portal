from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("admin_home/", views.home, name="admin_home"),
    path("alumni_home/", views.home, name="alumni_home"),
    path("user_home/", views.home, name="user_home"),
    path("events/user/", views.vi_event, name="vi_event"),
    path("events/create/", views.create_event, name="event_create"),
]