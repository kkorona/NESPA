from django.contrib import admin
from .models import vespaUser

class UserAdmin(admin.ModelAdmin) :
    list_display = ('username', 'password1')

admin.site.register(vespaUser)

# Register your models here.
