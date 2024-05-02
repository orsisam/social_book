from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile

# Create your views here.


@login_required(login_url="login")
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email has been taken")
            return redirect("signup")
        elif User.objects.filter(username=username).exists():
            messages.info(request, "Username has been taken")
            return redirect("signup")
        elif password != password2:
            messages.info(request, "Password Not Matching")

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()

        # Log user in and redirect to profile setting

        # create a Profile object for the new User
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(
            user=user_model, id_user=user_model.id)
        new_profile.save()
        return redirect('login')
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Username or Password is wrong")
            return redirect('login')
    else:
        return render(request, "signin.html")


@login_required(login_url="login")
def logout(request):
    auth_logout(request)
    return redirect('login')
