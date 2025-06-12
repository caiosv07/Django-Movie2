from django.db import models
from  accounts.models import User


class Comment(models.Model):
    comments = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField(null=False,)
    
   

    def __str__(self):
        return self.comments


