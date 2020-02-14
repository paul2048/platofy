from django.db import models
from django.contrib.auth.models import User

from .utils import QUESTION_TYPES

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=4096)
    upvoters = models.ManyToManyField(User, blank=True, related_name='+')
    downvoters = models.ManyToManyField(User, blank=True, related_name='+')
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.content[:200]}'

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=256)
    details = models.CharField(max_length=512, blank=True)
    question_type = models.CharField(max_length=256, choices=QUESTION_TYPES, default=QUESTION_TYPES[0][0])
    answers = models.ManyToManyField(Answer, blank=True)
    views = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.author.username} asked: {self.title}'

class Topic(models.Model):
    name = models.CharField(max_length=32)
    times_used = models.PositiveIntegerField(default=0)