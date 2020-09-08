from django.urls import path
from . import views

urlpatterns = [
    path('submission/', views.submission, name='submission'),
    path('submission_check/', views.submission_check, name='submission_check'),
    path('assignment_list/', views.assignment_list, name='assignment_list'),
    path('submission_list/', views.submission_list, name='submission_list'),
]