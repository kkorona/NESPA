from django.urls import path
from . import views

urlpatterns = [
    path('submission/', views.submission, name='submission'),
    path('submission_check/', views.submission_check, name='submission_check'),
    path('assignment_list/', views.assignment_list, name='assignment_list'),
    path('submission_list/', views.submission_list, name='submission_list'),
    path('submission_detail/', views.submission_detail, name='submission_detail'),
    path('watch_code/',views.watch_code, name='watch_code'),

    path('assignment_registry/',views.assignment_registry, name='assignment_registry'),
    path('assignment_manage/',views.assignment_manage, name='assignment_manage'),
    path('user_approval/',views.user_approval, name='user_approval'),
    path('user_manage/',views.user_manage, name='user_manage'),
    path('settings/',views.web_settings, name='settings'),
]