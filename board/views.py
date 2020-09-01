from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.dates import ArchiveIndexView, TodayArchiveView, YearArchiveView, MonthArchiveView, DayArchiveView

from board.models import Post

# Create your views here.

class PostLV(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 15

class PostDV(DetailView):
    model = Post

def write(request):
    if request.method == "GET":
        return render(request, 'board/write.html')
    if request.method == "POST":
        username = request.session['username']
        usertype = request.session['usertype']
        if usertype == "normal":
            return HttpResponse('접근할 수 없는 기능입니다.')
            
        title = request.POST.get('post_title',None)
        content = request.POST.get('post_contents',None)
        author = username
        article = Post(title = title, author = author, content=content)
        article.save()
        return redirect('board:post_list')
        
        '''
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
        '''

'''        
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'mod_date'


class PostYAV(YearArchiveView):
    model = Post
    date_field = 'mod_date'
    make_object_list = True


class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'mod_date'

class PostDAV(DayArchiveView):
    model = Post
    date_field = 'mod_date'

class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'mod_date'

'''