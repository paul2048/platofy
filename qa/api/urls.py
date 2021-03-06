from django.urls import path, include
from . import views 
from rest_framework import routers

router = routers.DefaultRouter()
router.register('answers', views.AnswerView)
router.register('questions', views.QuestionView)
router.register('topics', views.TopicView)

urlpatterns = [
    path('', include(router.urls)),
]