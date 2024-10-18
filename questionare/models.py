from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
  
    # track sessions
    session_id = models.CharField(max_length=255, null=True, blank=True)

    # Question and selected choice
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


    # Optional: Add timestamp for when the answer was given
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user or self.session_id} - Question: {self.question.text}, Choice: {self.choice.text}"


class Song(models.Model):
    title = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    # ManyToManyField establishes the many-to-many relationship with Choice
    choices = models.ManyToManyField('Choice', related_name='songs')

    def __str__(self):
        return self.title
    

