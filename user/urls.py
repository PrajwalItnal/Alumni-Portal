from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("<str:register_id>/", views.home, name="home"),
]