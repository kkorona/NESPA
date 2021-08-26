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
import dev2020.views

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('board.urls')),
    path('notice/',include('board.urls')),
    path('ds2021/', include('board.urls')),
    path('ds2020/', include('board.urls')),
    path('syllabus/', dev2020.views.index, name='index'),
    path('lecture/', dev2020.views.index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('assignment/', include('assignment.urls')),
    path('online_exam/', include('online_exam.urls')),
    path('forum/', include('forum.urls')),
    path('qna/', include('QnA.urls')),
    path('reports/', dev2020.views.index, name='index'),
    path('about/', dev2020.views.index, name='index'),
    path('devs/', dev2020.views.nespa_dev, name='nespa_dev'),
    path('nespa_qna/', dev2020.views.index, name='index'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
