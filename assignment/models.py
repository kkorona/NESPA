from django.db import models

# Create your models here.
    
class SubmissionModel(models.Model):
    client = models.CharField(max_length=20)
    prob_ID = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    result = models.CharField(max_length = 20)
    def __str__(self):
        return self.id
        
    class Meta:
        db_table = "submissions"