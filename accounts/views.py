from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == "POST":
            if request.POST["password1"] == request.POST["password2"]:
                    user = User.objects.create_user(
                        user_name=request.POST["user_name"], password=request.POST["password1"])
                    auth.login(request, user)
                    return redirect('dev2020')
    return render(request, 'accounts/signup.html')

def login(request):
    if request.method == "GET":
            return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dev2020')
        else:
            return render(request, 'login.html', {'error' : 'username or password is incorrect.'})
    else:
        return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('dev2020')

# Create your views here.
