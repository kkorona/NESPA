from django.db import models

# Create your models here.
    
class SubmissionModel(models.Model):
    client_ID = models.CharField(max_length=20)
    client_number = models.CharField(max_length=20)
    prob_ID = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    score = models.IntegerField()
    exec_time = models.FloatField()
    code_size = models.IntegerField()
    result = models.CharField(max_length = 40)
    
    def __str__(self):
        return self.id
        
    class Meta:
        db_table = "submissions"