from django.db import models
from django.contrib.auth.models import User
#there is an in-built user model

class Board(models.Model):
    Name = models.CharField(max_length=30, unique=True)
    Description = models.CharField(max_length=100)

    def __str__(self):
    	return self.Name

class Topic(models.Model):
    subject = models.CharField(max_length=100, default='sample')
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='Topics')
    starter = models.ForeignKey(User, related_name='Topics') #reverse relationships exist by default, 'Topics' is the name given

class Post(models.Model):
    message = models.TextField(max_length=4000, default='sample')
    topic = models.ForeignKey(Topic, related_name='Posts', default='sample')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='Posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+') #related_name='+' means no reverse relationship
