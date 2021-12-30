"""vespa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
from django.shortcuts import render
import dev2020.views

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('board.urls')),
    path('notice/',include('board.urls')),
    path('winterschool2021/', include('board.urls')),
    path('syllabus/', dev2020.views.index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('assignment/', include('assignment.urls')),
    path('online_exam/', include('online_exam.urls')),
    path('forum/', include('forum.urls')),
    path('qna/', include('QnA.urls')),
    path('reports/', include('reports.urls')),
    path('about/', dev2020.views.index, name='index'),
    path('devs/', dev2020.views.nespa_dev, name='nespa_dev'),
    path('course/', include('course.urls')),    
    path('error_reports/', include('error_reports.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

'''
urlpatterns ( url(r'^media/(?P<path>.\*)$', serve, {
    'document_root': settings.MEDIA_ROOT,
}))
'''

handler404 = "dev2020.views.page_not_found"
