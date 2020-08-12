from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin) :
    list_display = ('username', 'password1')

admin.site.register(User)

# Register your models here.
