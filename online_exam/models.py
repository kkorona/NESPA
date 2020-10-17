from django.db import models

# Create your models here.
    
class SubmissionModel(models.Model):
    client_ID = models.CharField(max_length=20)
    client_number = models.CharField(max_length=20)
    prob_ID = models.CharField(max_length=20)
    prob_name = models.CharField(max_length=20, default="-")
    created_at = models.DateTimeField(auto_now_add = True)
    score = models.IntegerField()
    exec_time = models.FloatField()
    code_size = models.IntegerField()
    lang = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.id)
        
    class Meta:
        db_table = "exam_submissions"
        ordering = ('-id',)
        
class ProblemModel(models.Model):
    prob_id = models.CharField(max_length=20)
    prob_name = models.CharField(max_length=20)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    size_limit = models.IntegerField()
    try_limit = models.IntegerField()
    time_limit = models.FloatField()
    eval = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.prob_id)
        
    class Meta:
        db_table = "exam_problems"
        ordering = ('prob_id',)