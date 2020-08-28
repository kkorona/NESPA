from django.db import models
import configparser

LENGTH_CONFIG = {
}

def loadConfig():
    global LENGTH_CONFIG
    LENGTH_CONFIG = {
        'UN_MAXLEN' : 200,
        'ID_MAXLEN' : 200,
        'PW_MAXLEN' : 200,
        'SN_MAXLEN' : 200,
        'GR_MAXLEN' : 200,
        'MJ_MAXLEN' : 200,
        'EM_MAXLEN' : 200,
        'PH_MAXLEN' : 200,
    }
    

class vespaUser(models.Model):
    loadConfig()
    username = models.CharField(max_length = LENGTH_CONFIG['UN_MAXLEN'])
    studentNumber = models.CharField(max_length = LENGTH_CONFIG['SN_MAXLEN'])
    user_id = models.CharField(max_length = LENGTH_CONFIG['ID_MAXLEN'])
    password = models.CharField(max_length = LENGTH_CONFIG['PW_MAXLEN'])
    grade = models.CharField(max_length = LENGTH_CONFIG['GR_MAXLEN'])
    major = models.CharField(max_length = LENGTH_CONFIG['MJ_MAXLEN'])
    email = models.CharField(max_length = LENGTH_CONFIG['EM_MAXLEN'])
    phone = models.CharField(max_length = LENGTH_CONFIG['PH_MAXLEN'])
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.studentNumber
        
    class Meta:
        db_table = "users"

# Create your models here.
