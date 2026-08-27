from django.db import models

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=100)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return f"Title:{self.name}, Last edited:{self.last_edited}, Published:{self.is_published},"