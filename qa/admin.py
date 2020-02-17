from django.contrib import admin
from .models import Answer, Question, Topic

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Topic)