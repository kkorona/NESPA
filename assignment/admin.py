from django.contrib import admin
from .models import SubmissionModel

@admin.register(SubmissionModel)

class submissionAdmin(admin.ModelAdmin) :
    list_display = ('client_ID', 'client_number', 'prob_ID', 'created_at', 'score', 'exec_time', 'code_size', 'result')

# Register your models here.
