from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    register_id = request.session.get("register_id")
    if not register_id:
        return redirect("login")
    else:
        return render(request, "user/user_home.html", {"register_id": register_id})

def logout(request):
    request.session.flush()
    return redirect('home')