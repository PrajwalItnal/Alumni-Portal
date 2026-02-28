from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
]