# models.py
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200, default="Default Title")

    # title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='projects/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Achievement(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_awarded = models.DateField()

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# file = models.FileField(upload_to='projects/', null=True)
