from django.urls import path
from . import views

urlpatterns = [
    path('', views.submission, name='submission'),
    path('submission/', views.submission, name='submission'),
]