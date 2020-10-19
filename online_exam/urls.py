from django.urls import path
from online_exam import views

urlpatterns = [
    path('', views.exam_submission, name='exam_submission'),
    path('submission/', views.exam_submission, name='exam_submission'),
    path('submission_check/', views.exam_submission_check, name='exam_submission_check'),
    path('submission_list/', views.exam_submission_list, name='exam_submission_list'),
    path('submission_detail/', views.exam_submission_detail, name='exam_submission_detail'),
    path('watch_code/',views.exam_watch_code, name='watch_code'),
]
