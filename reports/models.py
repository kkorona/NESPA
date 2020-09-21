from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    content = models.TextField('CONTENT', default='')
    pub_date = models.DateTimeField('PUBLISH DATE', default = timezone.now)
    mod_date = models.DateTimeField('MODIFY DATE', auto_now = True)
    post_hit = models.IntegerField()
    
    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'reports_posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
        
    def get_id(self):
        return self.id

    def get_absolute_url(self):
        return reverse('reports:post_detail', args=(self.id,))

    def get_previous(self):
        return self.get_previous_by_mod_date()

    def get_next(self):
        return self.get_next_by_mod_date()
        
    @property
    def update_counter(self):
        self.post_hit += 1
        self.save()
        return ''

class Comment(models.Model):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateTimeField('PUBLISH DATE', default = timezone.now)
    mod_date = models.DateTimeField('MODIFY DATE', auto_now = True)
    
    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        db_table = 'reports_comments'
        ordering = ('-pub_date',)
        
    def get_parent(self):
        return self.parent