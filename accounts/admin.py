from django.contrib import admin
from .models import vespaUser

@admin.register(vespaUser)

class UserAdmin(admin.ModelAdmin) :
    list_display = ('user_id', 'username', 'studentNumber', 'major', 'email', 'usertype')

# Register your models here.
