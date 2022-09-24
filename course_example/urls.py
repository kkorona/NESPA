from django.urls import path
from . import views
from . import configs

app_name = configs.COURSE_NAME

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
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
    path('settings/',views.web_setting, name='settings'),
    path('lexer/',views.lexer, name='lexer'),

    path('board',views.PostLV.as_view(),name='post_list_null'),
    path('board/<str:board_info>',views.PostLV.as_view(), name='post_list'),
    path('board/<str:i_board_info>/write',views.write, name='write'),
    path('edit/<int:article_id>',views.edit, name='edit'),
    path('post/<int:pk>/',views.PostDV.as_view(), name='post_detail'),
    path('post/<int:article_id>/deleteComment/<int:comment_id>',views.deleteComment, name='delete_comment'),

    path('about/', views.index, name='index'),
    path('devs/', views.nespa_dev, name='nespa_dev'),
]
