from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are successfully logged in')
            return redirect('/')
        else:
            messages.warning(request, 'invalid credential')
    return render(request, 'account/signIn.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:

            # If username and email are already in database
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username already exits")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exits")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created Successfully.')
                return redirect("signin")
        else:
            messages.warning(request, 'Password do not match.')
            return redirect("signup")

    return render(request, 'account/signUp.html')


def signout(request):
    logout(request)
    messages.success(request, 'Successfully logout.')
    return redirect("/")


