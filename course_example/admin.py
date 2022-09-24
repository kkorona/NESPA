from django.contrib import admin
from .models import vespaUser
from .models import SubmissionModel, ProblemModel, GradeModel

@admin.register(vespaUser)
class UserAdmin(admin.ModelAdmin) :
    list_display = ('user_id', 'username', 'studentNumber', 'major', 'email', 'usertype')

@admin.register(SubmissionModel)

class submissionAdmin(admin.ModelAdmin) :
    list_display = ('id', 'client_ID', 'client_number', 'prob_ID', 'created_at', 'score', 'exec_time', 'code_size', 'token_size')
    
@admin.register(ProblemModel)
    
class submissionAdmin(admin.ModelAdmin) :
    list_display = ('id', 'prob_name','starts_at','ends_at','size_limit', 'token_limit', 'try_limit', 'time_limit', 'eval')
    
@admin.register(GradeModel)
    
class gradeAdmin(admin.ModelAdmin) :
    list_display = ('id', 'problem_ID')
# Register your models here.

from django.contrib import admin
from .models import Post, Attach, Comment

# Register your models here.
admin.autodiscover()
admin.site.enable_nav_sidebar = False

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'pub_date', 'mod_date','board_info')
    list_filter = ('mod_date',)
    search_fields = ('title', 'author', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'pub_date', 'mod_date')
    list_filter = ('pub_date',)
    search_fields = ('title', 'author')

@admin.register(Attach)
class AttachAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'ext')
