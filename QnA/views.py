from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, TodayArchiveView, YearArchiveView, MonthArchiveView, DayArchiveView
from django.core.exceptions import ObjectDoesNotExist

from QnA.models import Post, Comment

# Create your views here.

class PostLV(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 15

class PostDV(DetailView):
    model = Post
    comments = None
    try:
        comments = Comment.objects.filter(parent=model.get_id)
    except Comment.DoesNotExist:
        pass
        
def write(request):
    if request.method == "GET":
        return render(request, 'QnA/write.html')
    if request.method == "POST":
        username = request.session['username']
        usertype = request.session['usertype']
        if usertype == "unapproved":
            return HttpResponse('접근할 수 없는 기능입니다.')
            
        title = request.POST.get('post_title',None)
        content = request.POST.get('post_contents',None)
        author = username
        article = Post(title = title, author = author, content=content)
        article.save()
        return redirect('qna:post_list')
        

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