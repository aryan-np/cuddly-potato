from django.db import models
from django.contrib.auth.models import User

class TodoModel(models.Model):
    
    class PriorityChoices(models.IntegerChoices):
        LESS_IMPORTANT = 1
        IMPORTANT = 2
        VERY_IMPORTANT = 3
        
    class Status(models.IntegerChoices):
        PENDING = 1
        IN_PROGRESS = 2
        COMPLETED = 3
        
    title = models.CharField(max_length=500,null=False,blank=False)
    description = models.TextField()
    priority = models.IntegerField(choices=PriorityChoices.choices, default=PriorityChoices.IMPORTANT)
    status = models.IntegerField(choices=Status.choices, default= Status.PENDING)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    