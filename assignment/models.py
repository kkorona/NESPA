from django.db import models
from django.core.files.storage import FileSystemStorage
from vespa.settings import PROBLEM_UPLOAD_ROOT, SUBMISSION_UPLOAD_ROOT
from accounts.models import vespaUser
import os
# Create your models here.

problem_upload_storage = FileSystemStorage(location=PROBLEM_UPLOAD_ROOT, base_url='/assignment')
submission_upload_storage = FileSystemStorage(location=SUBMISSION_UPLOAD_ROOT, base_url='/submission')

def document_upload_path(instance, filename):
    return 'assignment/documents/{}'.format(filename)

def sample_data_upload_path(instance, filename):
    return 'assignment/sampledata/{}/{}'.format(instance.prob_id, filename)

def sub_data_upload_path(instance, filename):
    return '{}/subs/{}'.format(instance.prob_id, filename)

def header_data_upload_path(instance, filename):
    return '{}/header/{}'.format(instance.prob_id, filename)

def grade_data_upload_path(instance, filename):
    return '{}/eval/{}'.format(instance.problem.prob_id,filename)

def submission_upload_path(instance, filename):
    filename = '{}.{}'.format(instance.id, instance.lang)
    return '{}/{}/{}'.format(instance.user.studentNumber, instance.problem.prob_id, filename)



class ProblemModel(models.Model):
    prob_id = models.CharField(max_length=20)
    prob_name = models.CharField(max_length=20)
    document = models.FileField(upload_to=document_upload_path, blank=True, null=True)
    sample_data = models.FileField(upload_to=sample_data_upload_path, blank=True, null=True)
    sub_data = models.FileField(upload_to=sub_data_upload_path, storage=problem_upload_storage, blank=True, null=True)
    header_data = models.FileField(upload_to=header_data_upload_path, storage=problem_upload_storage, blank=True, null=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    size_limit = models.IntegerField()
    try_limit = models.IntegerField()
    time_limit = models.FloatField()
    eval = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.prob_id)
        
    class Meta:
        db_table = "problems"
        ordering = ('prob_id',)

class GradeModel(models.Model):
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE, null=True)
    grade_input = models.FileField(upload_to=grade_data_upload_path, storage=problem_upload_storage, null=True)
    grade_output = models.FileField(upload_to=grade_data_upload_path, storage=problem_upload_storage, null=True)

    def __str__(self):
        return '{}({})'.format(str(self.problem.prob_id), str(self.grade_input.name))

    def input_filename(self):
        return os.path.basename(self.grade_input.name)

    def output_filename(self):
        return os.path.basename(self.grade_output.name)

    def problem_ID(self):
        return str(self.problem.prob_id)


    problem_ID.short_description = 'PROBLEM ID'


class SubmissionModel(models.Model):
    client_ID = models.CharField(max_length=20)
    client_number = models.CharField(max_length=20)
    prob_ID = models.CharField(max_length=20)
    prob_name = models.CharField(max_length=20, default="-")

    user = models.ForeignKey(vespaUser, on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE, null=True)
    sub_file = models.FileField(upload_to=submission_upload_path, storage=submission_upload_storage, null=True)

    created_at = models.DateTimeField(auto_now_add = True)
    score = models.IntegerField()
    exec_time = models.FloatField()
    code_size = models.IntegerField()
    lang = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.id)

    def user_ID(self):
        return self.user.user_id

    def user_number(self):
        return self.user.studentNumber

    def problem_ID(self):
        return str(self.problem.prob_id)

    def filename(self):
        return str(os.path.basename(self.sub_file.name))

    user_ID.short_description = 'CLIENT ID'
    user_number.short_description = 'CLIENT NUMBER'
    problem_ID.short_description = 'PROB ID'
        
    class Meta:
        db_table = "submissions"
        ordering = ('-id',)

