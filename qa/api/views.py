from rest_framework import viewsets
from qa.models import Answer, Question
from .serializers import AnswerSerializer, QuestionSerializer

class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer