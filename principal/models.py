from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    
    
    
    def __str__(self):
        return self.title + ' - '+ self.user.username


