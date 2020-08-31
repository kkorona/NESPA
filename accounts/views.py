from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from .models import vespaUser
import re

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
        
        # user ID
        
        p = re.compile('[a-zA-Z0-9]+')
        
        if p.match(user_id) == None:
            return HttpResponse('잘못된 아이디입니다: '+user_id + '<br>Wrong user id: '+ user_id)
        
        if len(user_id) < 4 or len(user_id) > 10:
            return HttpResponse('user id is too long or too short.')
            
        # student number
        if not len(studentNumber) == 9:
            return HttpResponse('Wrong Student Number.')
        
        # email match
        
        p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if p.match(email) == None:
            return HttpResponse('Wrong Email.')
        
        # all-fill validation
        if not (username and studentNumber and user_id and password1 and password2 and grade and major and email and phone):
            return HttpResponse('Please fill all the blanks in registeration form.')
            
        # validate passwords
        elif password1 != password2:
            return HttpResponse('Please fill all the blanks in registeration form.')
        else:
            user = vespaUser(username=username, studentNumber=studentNumber, password=make_password(password1), user_id=user_id, grade=grade, major=major, email=email, phone=phone)
            try:
                c_user = vespaUser.objects.get(user_id=user_id)
                return HttpResponse('이미 등록된 사용자입니다.<br>Already registerd user.')
            except vespaUser.DoesNotExist:
                user.save()
                return redirect('/login')
        return render(request, 'accounts/signup.html')

def login(request):
    response_data = {}
    if request.method == "GET":
        return render(request, 'accounts/login.html')
        
    elif request.method == "POST":
        login_userid = request.POST["user_id"]
        login_password = request.POST["password"]
        
        if not (login_userid and login_password):
            return HttpResponse('ID나 비밀번호는 비울 수 없습니다.<br>ID or password cannot be empty.')
        else:
            try:
                myuser = vespaUser.objects.get(user_id=login_userid)
                if check_password(login_password, myuser.password):
                    request.session['userid'] = myuser.user_id
                    request.session['username'] = myuser.username
                    return redirect('/ds2020')
                else:
                    return HttpResponse('ID 또는 비밀번호가 잘못되었습니다.<br>ID or password is invalid.')
            except vespaUser.DoesNotExist:
                return HttpResponse('ID 또는 비밀번호가 잘못되었습니다.<br>ID or password is invalid.')
    return render(request,'accounts/login.html')

def logout(request):
    request.session.pop('userid')
    request.session.pop('username')
    return redirect('/ds2020')
