from django.db import models
import configparser

LENGTH_CONFIG = {
}

def loadConfig():
    global LENGTH_CONFIG
    LENGTH_CONFIG = {
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
    usertype = models.CharField(max_length = LENGTH_CONFIG['TY_MAXLEN'])
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.studentNumber
        
    class Meta:
        db_table = "users"

# Create your models here.
