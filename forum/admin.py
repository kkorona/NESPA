from django.contrib import admin
from forum.models import Post, Comment

# Register your models here.

#admin.site.register(Post)
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'pub_date', 'mod_date')
    list_filter = ('pub_date',)
    search_fields = ('title', 'author', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'pub_date', 'mod_date')
    list_filter = ('pub_date',)
    search_fields = ('title', 'author')