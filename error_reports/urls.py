from django.urls import path
from error_reports import views

app_name = 'error_reports'

urlpatterns =[
    path('',views.PostLV.as_view(), name='index'),
    path('post/',views.PostLV.as_view(), name='post_list'),
    path('edit/<int:article_id>',views.edit, name='edit'),
    path('write/',views.write, name='write'),
    path('post/<int:pk>/',views.PostDV.as_view(), name='post_detail'),
    path('post/<int:article_id>/deleteComment/<int:comment_id>',views.deleteComment, name='delete_comment'),
]

'''
path('archive/',views.PostAV.as_view(), name='post_archive'),
path('archive/<int:year>',views.PostYAV.as_view(), name='post_year_archive'),
path('archive/<int:year>/<str:month>/',views.PostMAV.as_view(), name='post_month_archive'),
path('archive/<int:year>/<str:month>/<int:day>/',views.PostDAV.as_view(), name='post_day_archive'),
path('archive/today',views.PostTAV.as_view(), name='post_today'),
'''