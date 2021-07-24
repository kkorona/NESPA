from django.urls import path
from online_exam import views

urlpatterns = [
    path('', views.exam_submission, name='exam_submission'),
    path('exam_submission/', views.exam_submission, name='exam_submission'),
    path('exam_submission_check/', views.exam_submission_check, name='exam_submission_check'),
    path('exam_submission_list/', views.exam_submission_list, name='exam_submission_list'),
    path('exam_submission_detail/', views.exam_submission_detail, name='exam_submission_detail'),
    path('exam_watch_code/',views.exam_watch_code, name='exam_watch_code'),
]