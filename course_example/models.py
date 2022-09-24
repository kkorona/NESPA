from . import configs
import configparser
from django.db import models
from django.core.files.storage import FileSystemStorage
from vespa.settings import BASE_DIR
from django.utils import timezone
from django.urls import reverse
import os

PROBLEM_UPLOAD_ROOT = os.path.join(BASE_DIR, 'data',configs.COURSE_NAME,'assignment')
SUBMISSION_UPLOAD_ROOT = os.path.join(BASE_DIR, 'data',configs.COURSE_NAME,'submission')

problem_upload_storage = FileSystemStorage(location=PROBLEM_UPLOAD_ROOT, base_url='/assignment')
submission_upload_storage = FileSystemStorage(location=SUBMISSION_UPLOAD_ROOT, base_url='/submission')

def loadConfig():
    result = {
        'UN_MAXLEN' : 20,
        'ID_MAXLEN' : 20,
        'PW_MAXLEN' : 200,
        'SN_MAXLEN' : 20,
        'GR_MAXLEN' : 20,
        'MJ_MAXLEN' : 40,
        'EM_MAXLEN' : 40,
        'PH_MAXLEN' : 20,
        'TY_MAXLEN' : 20,
    }
    return result
    

class vespaUser(models.Model):
    LENGTH_CONFIG = loadConfig()
    
    username = models.CharField(max_length = LENGTH_CONFIG['UN_MAXLEN'])
    studentNumber = models.CharField(max_length = LENGTH_CONFIG['SN_MAXLEN'])
    user_id = models.CharField(max_length = LENGTH_CONFIG['ID_MAXLEN'])
    password = models.CharField(max_length = LENGTH_CONFIG['PW_MAXLEN'])
    grade = models.CharField(max_length = LENGTH_CONFIG['GR_MAXLEN'])
    major = models.CharField(max_length = LENGTH_CONFIG['MJ_MAXLEN'])
    email = models.CharField(max_length = LENGTH_CONFIG['EM_MAXLEN'])
    phone = models.CharField(max_length = LENGTH_CONFIG['PH_MAXLEN'])
    usertype = models.CharField(max_length = LENGTH_CONFIG['TY_MAXLEN'])
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.studentNumber
        
    class Meta:
        db_table = configs.COURSE_NAME + "_users"
        ordering = ('username',)

def document_upload_path(instance, filename):
    return '{}/assignment/documents/{}'.format(configs.COURSE_NAME,filename)

def sample_data_upload_path(instance, filename):
    return '{}/assignment/sampledata/{}/{}'.format(configs.COURSE_NAME,instance.prob_id, filename)

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
    token_limit = models.IntegerField(default=1000)
    eval = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.prob_id)
        
    class Meta:
        db_table = configs.COURSE_NAME+"_problems"
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
    token_size = models.IntegerField(default=1000)
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
        db_table = configs.COURSE_NAME+"_submissions"
        ordering = ('-id',)
    
class Post(models.Model):
    title = models.CharField(max_length=200, blank = False)
    author = models.CharField(max_length=50)
    content = models.TextField('CONTENT', blank = False)
    pub_date = models.DateTimeField('PUBLISH DATE', default = timezone.now)
    mod_date = models.DateTimeField('MODIFY DATE', auto_now = True)
    board_info = models.CharField(max_length=50, blank = False)
    post_hit = models.IntegerField()
    
    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = configs.COURSE_NAME+'_posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
        
    def get_id(self):
        return self.id

    def get_absolute_url(self):
        return reverse(self.board_info + ':post_detail', args=(self.id,))

    def get_previous(self):
        return self.get_previous_by_mod_date()

    def get_next(self):
        return self.get_next_by_mod_date()
    
    def get_board_info(self):
        return self.board_info
        
    @property
    def update_counter(self):
        self.post_hit += 1
        self.save()
        return ''

    def comments_count(self):
        return len(self.comment_set.filter(deleted=False))

class Comment(models.Model):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)
    retweet = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    author = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateTimeField('PUBLISH DATE', default = timezone.now)
    mod_date = models.DateTimeField('MODIFY DATE', auto_now = True)
    
    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        db_table = configs.COURSE_NAME+'_comments'
        ordering = ('-pub_date',)
        
    def get_parent(self):
        return self.parent
        
class Attach(models.Model):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    path = models.CharField(max_length=100)
    ext = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = 'attachment'
        verbose_name_plural = 'attachments'
        db_table = configs.COURSE_NAME+'_attachments'
