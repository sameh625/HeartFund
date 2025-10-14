from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home:index") 
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("accounts:login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home:index")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect("home:index")
            else:
                messages.error(request, "Account not active. Please activate your account.")
        else:
            messages.error(request,"Invalid username or password")
        
    return render(request,"accounts/login.html")
    

def logout_view(request):
    messages.info(request, "Hope to see you again!")
    logout(request)
    return redirect("accounts:login")