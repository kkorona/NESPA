from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .models import User

def signup(request):
    if request.method == "GET":
        return render(request, 'accounts/signup.html')
        
    if request.method == "POST":
        username = request.POST.get('user_name',None)
        studentNumber = request.POST.get('student_number',None)
        user_id = request.POST.get('user_id',None)
        password1 = request.POST.get('password1',None)
        password2 = request.POST.get('password2',None)
        grade = request.POST.get('grade',None)
        major = request.POST.get('major',None)
        email = request.POST.get('email',None)
        phone = request.POST.get('phone',None)
        res_data = {}
        
        # validation zone
        
        # all-fill validation
        if not (username and studentNumber and user_id and password1 and password2 and grade and major and email and phone):
            res_data['error'] = 'Please fill all the blanks in registeration form.'
            
        # validate passwords
        elif password1 != password2:
            res_data['error'] = 'Please fill all the blanks in registeration form.'
        else:
            user = User(username=username, studentNumber=studentNumber, password=make_password(password1), user_id=user_id, grade=grade, major=major, email=email, phone=phone)
            user.save()
    return render(request, 'accounts/signup.html', res_data)

def login(request):
    if request.method == "POST":
        username = request.POST["user_id"]
        password1 = request.POST["password1"]
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
