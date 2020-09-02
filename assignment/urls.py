from django.urls import path
from . import views

urlpatterns = [
    path('submission/', views.submission, name='submission'),
    path('assignment_list/', views.assignment_list, name='assignment_list'),
]