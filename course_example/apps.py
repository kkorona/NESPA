from django.apps import AppConfig
from . import configs

class Course_exampleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = configs.COURSE_NAME