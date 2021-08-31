from django.contrib import admin
from board.models import Post, Attach, Comment

# Register your models here.
admin.autodiscover()
admin.site.enable_nav_sidebar = False

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'pub_date', 'mod_date')
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
