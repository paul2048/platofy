from rest_framework import serializers
from qa.models import Answer, Question, Topic

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'author', 'content', 'upvoters', 'downvoters', 'timestamp', 'edited_timestamp')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'author', 'title', 'details', 'topics', 'answers', 'question_type', 'views', 'timestamp', 'edited_timestamp')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'times_used')