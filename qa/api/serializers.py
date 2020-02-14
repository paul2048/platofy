from rest_framework import serializers
from qa.models import Answer, Question

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'author', 'content')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'author', 'title', 'details', 'answers')