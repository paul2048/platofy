from django.test import TestCase

from .models import Answer, Question

class ModelstestCase(TestCase):
    def setUp(self):
        print(1)