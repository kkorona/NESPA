from django.contrib import admin
from board.models import Post, Attach

# Register your models here.

#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'pub_date', 'mod_date')
    list_filter = ('mod_date',)
    search_fields = ('title', 'author', 'content')

@admin.register(Attach)
class AttachAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'ext')