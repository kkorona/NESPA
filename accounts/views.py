from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import vespaUser

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
            user = vespaUser(username=username, studentNumber=studentNumber, password=make_password(password1), user_id=user_id, grade=grade, major=major, email=email, phone=phone)
            user.save()
            return redirect('/accounts/login')
    return render(request, 'accounts/signup.html', res_data)

def login(request):
    response_data = {}
    if request.method == "GET":
        return render(request, 'accounts/login.html')
        
    elif request.method == "POST":
        login_userid = request.POST["user_id"]
        login_password = request.POST["password"]
        
        if not (login_userid and login_password):
            response_data['error'] = 'ID or password cannot be empty.'
        else:
            myuser = vespaUser.objects.get(user_id=login_userid)
            if check_password(login_password, myuser.password):
                request.session['user'] = myuser.id
                return redirect('/')
            else:
                response_data['error']="Invalid password."
    return render(request,'accounts/login.html', response_data)

def logout(request):
    request.session.pop('user')
    return redirect('/')
