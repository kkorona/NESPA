from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.dates import ArchiveIndexView, TodayArchiveView, YearArchiveView, MonthArchiveView, DayArchiveView
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage

from board.models import Post, Comment
from board.forms import CommentForm

import os, shutil
# Create your views here.

class PostLV(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 15

class PostDV(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    def get_success_url(self, **kwargs):
        return reverse('board:post_detail', kwargs = {'pk': self.object.pk })
        
    def get_context_data(self, **kwargs):
        context = super(PostDV, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={
            'text' : '댓글을 입력해주세요.',
        })
        if 'logged_in' in self.request.session:
            context['user'] = self.request.session['userid']
        else:
            context['user'] = 'anonymous'
        context['comments'] = self.object.comment_set.all()
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.parent = get_object_or_404(Post, pk=self.object.pk)
        comment.author = self.request.session['userid']
        comment.save()
        return super(PostDV, self).form_valid(form)

def write(request):
    if request.method == "GET":
        return render(request, 'board/write.html')
    if request.method == "POST":
        username = request.session['username']
        usertype = request.session['usertype']
        userid = request.session['userid']
        if usertype == "unapproved":
            return HttpResponse('접근할 수 없는 기능입니다.')
            
        title = request.POST.get('post_title',None)
        content = request.POST.get('post_contents',None)
        author = username
        article = Post(title = title, author = author, content=content, post_hit = 0)
        article.save()

                     
        files = request.FILES.getlist('attach_files')
        fs = FileSystemStorage()
        for file in files:
            filename = fs.save(file.name,file)
            uploaded_file_url = fs.url(filename);
            departure_path = os.path.join(settings.BASE_DIR, uploaded_file_url[1:])
            destination_path = os.path.join(settings.BASE_DIR, 'media','attached',str(article.id))
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            shutil.move(departure_path, os.path.join(destination_path, file.name))
        return redirect('board:post_list')
        

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
