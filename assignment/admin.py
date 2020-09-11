from django.contrib import admin
from .models import SubmissionModel, ProblemModel

@admin.register(SubmissionModel)

class submissionAdmin(admin.ModelAdmin) :
    list_display = ('id', 'client_ID', 'client_number', 'prob_ID', 'created_at', 'score', 'exec_time', 'code_size')
    
@admin.register(ProblemModel)
    
class submissionAdmin(admin.ModelAdmin) :
    list_display = ('id', 'prob_name','starts_at','ends_at','size_limit', 'try_limit', 'time_limit', 'eval')
    

# Register your models here.

