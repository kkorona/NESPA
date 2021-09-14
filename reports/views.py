# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.dates import ArchiveIndexView, TodayArchiveView, YearArchiveView, MonthArchiveView, DayArchiveView
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from reports.models import Post, Comment, Attach
from reports.forms import CommentForm

import os, shutil, glob, urllib.parse
# Create your views here.

class PostLV(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 15

class PostDV(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    def get_success_url(self, **kwargs):
        return reverse('reports:post_detail', kwargs = {'pk': self.object.pk })
        
    def get_context_data(self, **kwargs):
        context = super(PostDV, self).get_context_data(**kwargs)

        post_id = self.kwargs['pk']
        if f'username/reports/{post_id}' not in self.request.session:
            current_post = Post.objects.get(pk=post_id)
            current_post.update_counter
            self.request.session[f'username/reports/{post_id}'] = True

        context['form'] = CommentForm(initial={
            'text' : '',
        })
        if 'logged_in' in self.request.session:
            context['user'] = self.request.session['userid']
        else:
            context['user'] = 'anonymous'
        #context['comments'] = self.object.comment_set.all()
        context['comments'] = sorted(list(self.object.comment_set.all()), key=lambda x: x.pub_date, reverse=False)
        context['attachments'] = self.object.attach_set.all()
        context['content'] = self.object.content
        context['content'] = self.object.content.replace('\\n', '\\\n')
        context['content'] = context['content'].replace('\r\n', '\\n').replace('\r', '\\n').replace('\n', '\\n')
        context['content'] = context['content'].replace("\"", "\\\"").replace('\'', '\\\'').replace('/', '\/')
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
    def form_valid(self, form):
        comment_id = int(self.request.POST.get('comment_id'))
        retweet_id = int(self.request.POST.get('retweet_id'))
        if retweet_id != -1 and comment_id == -1:
            comment = form.save(commit=False)
            comment.parent = get_object_or_404(Post, pk=self.object.pk)
            comment.author = self.request.session['userid']
            comment.retweet = get_object_or_404(Comment, pk=retweet_id)
            comment.save()
            return super(PostDV, self).form_valid(form)

        if comment_id == -1:
            comment = form.save(commit=False)
            comment.parent = get_object_or_404(Post, pk=self.object.pk)
            comment.author = self.request.session['userid']
            comment.save()
        else:
            comment = get_object_or_404(Comment, pk=comment_id)
            comment.text = self.request.POST.get('text')
            comment.save()
        return super(PostDV, self).form_valid(form)

def deleteComment(request, article_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.deleted = True
    comment.save()
    return redirect('/reports/post/' + str(article_id))

def edit(request, article_id):
    username = request.session['username']
    usertype = request.session['usertype']
    userid = request.session['userid']
    article = Post.objects.get(id=article_id)
    
    if usertype == "unapproved":
        return HttpResponse('접근할 수 없는 기능입니다.')
    
    if usertype == "normal":
        if article.author != username:
            HttpResponse('수정 권한이 없습니다.')
            
    if request.method == "POST":
        title = request.POST.get('post_title',None)
        content = request.POST.get('post_contents',None)
        if title == "" or content == "":
            return HttpResponse('제목 또는 내용이 비어있습니다.')
        article.title = title
        article.content = content
        article.save()

        files = request.FILES.getlist('attach_files')
        existing_files = request.POST.getlist('existing_files')
        print(existing_files)
        for attach in article.attach_set.all():
            if str(attach.id) not in existing_files:
                attach.delete()
        
        fs = FileSystemStorage()
        for file in files:
            fname = urllib.parse.unquote(file.name)
            filename = fs.save(fname,file)
            uploaded_file_url = fs.url(filename);
            departure_path = os.path.join(settings.BASE_DIR, uploaded_file_url[1:])
            destination_path = os.path.join(settings.BASE_DIR, 'media','attached','board',str(article.id))
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            destination_path = os.path.join(destination_path, fname)
            shutil.move(departure_path,destination_path)
            ext = filename.split(".")[-1]
            attach = Attach(parent=article, path = destination_path,name=fname, ext = ext)
            attach.save()

        return redirect('/reports/post/' + str(article_id))
        
    if request.method == "GET":
        content = article.content
        content = content.replace('\\n', '\\\n')
        content = content.replace('\r\n', '\\n').replace('\r', '\\n').replace('\n', '\\n')
        content = content.replace("\"", "\\\"").replace('\'', '\\\'').replace('/', '\/')
        return render(request, 'reports/edit.html',{'article_content' : content, 'article_title' : article.title, 'attachments' : article.attach_set.all()})
        
def write(request):
    if request.method == "GET":
        return render(request, 'reports/write.html')
    if request.method == "POST":
        username = request.session['username']
        usertype = request.session['usertype']
        userid = request.session['userid']
        if usertype == "unapproved":
            return HttpResponse('접근할 수 없는 기능입니다.')
        title = request.POST.get('post_title',None)
        content = request.POST.get('post_contents',None)
        if title == "" or content == "":
            return HttpResponse('제목 또는 내용이 비어있습니다.')
        author = userid
        article = Post(title = title, author = author, content=content, post_hit = 0)
        article.save()

                     
        files = request.FILES.getlist('attach_files')
        fs = FileSystemStorage()
        for file in files:
            fname = urllib.parse.unquote(file.name)
            filename = fs.save(fname,file)
            uploaded_file_url = fs.url(filename)
            departure_path = urllib.parse.unquote(os.path.join(settings.BASE_DIR, uploaded_file_url[1:]))
            destination_path = urllib.parse.unquote(os.path.join(settings.BASE_DIR, 'media','attached','reports',str(article.id)))
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            destination_path = os.path.join(destination_path, fname)
            shutil.move(departure_path,destination_path)
            ext = filename.split(".")[-1]
            attach = Attach(parent=article, path = destination_path,name=fname, ext = ext)
            attach.save()
            
        return redirect('reports:post_list')

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
