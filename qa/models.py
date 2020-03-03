from django.db import models
from django.contrib.auth.models import User

from .utils import QUESTION_TYPES

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=4096)
    upvoters = models.ManyToManyField(User, blank=True, related_name='+')
    downvoters = models.ManyToManyField(User, blank=True, related_name='+')
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_valid_answer(self):
        for upvoter in self.upvoters.all():
            if upvoter in self.downvoters.all():
                return False
        return len(self.content) > 5

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.content[:200]}'

class Topic(models.Model):
    name = models.CharField(max_length=32)
    times_used = models.PositiveIntegerField(default=1)

    def is_valid_topic(self):
        return self.times_used > 0 and self.name == self.name.upper()

    def __str__(self):
        return f'{self.name} ({self.times_used})'

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=256)
    details = models.CharField(max_length=512, blank=True)
    topics = models.ManyToManyField(Topic)
    type = models.CharField(max_length=256, choices=QUESTION_TYPES, default=QUESTION_TYPES[0][0])
    answers = models.ManyToManyField(Answer, blank=True)
    views = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_valid_question(self):
        topics_name = list(self.topics.values_list('name', flat=True))
        unique_topics_names = set(self.topics.values_list('name', flat=True))

        return 7 > self.topics.count() > 0 and self.views > 0 and len(topics_name) == len(unique_topics_names)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'({self.answers.count()} answers) {self.author.username} asked: {self.title}'