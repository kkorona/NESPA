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
from django.shortcuts import render
import course_example.views

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    ###
    # append new courses by editing path examples below
    #
    # path('course_example/',include('course_example.urls', namespace="course_example")),
    #
    ###
    path('course_example/',include('course_example.urls', namespace="course_example")),
    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

'''
urlpatterns ( url(r'^media/(?P<path>.\*)$', serve, {
    'document_root': settings.MEDIA_ROOT,
}))
'''

handler404 = "course_example.views.page_not_found"
