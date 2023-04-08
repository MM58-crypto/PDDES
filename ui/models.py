from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib import admin


# Create your models here.


class Question(models.Model):

    question_text = models.TextField()
    
    # add a field for the choices
    
    def __str__(self):
        return self.question_text
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
   

    def __str__(self):
        return self.choice_text


