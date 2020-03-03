from django.test import Client, TestCase
from django.db.models import Max
from django.contrib.auth.models import User

from .models import Answer, Question, Topic

class ModelstestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user(username='a', password='a')
        u2 = User.objects.create_user(username='b', password='b')

        t1 = Topic.objects.create(name='TOPIC1')
        t2 = Topic.objects.create(name='TOPIC2')
        t3 = Topic.objects.create(name='TOPIC3')
        t4 = Topic.objects.create(name='REPEATED_TOPIC_NAME')
        t5 = Topic.objects.create(name='REPEATED_TOPIC_NAME')
        t6 = Topic.objects.create(name='topic6')
        t7 = Topic.objects.create(name='TOPIC7', times_used=0)

        q1 = Question.objects.create(author=u1, title='Question 1?')
        q2 = Question.objects.create(author=u2, title='Question 2?')
        q3 = Question.objects.create(author=u2, title='Question 3?', views=0)
        q4 = Question.objects.create(author=u1, title='Question 4?')

        a1 = Answer.objects.create(author=u1, content='Lorem Lorem foo.')
        a2 = Answer.objects.create(author=u2, content='Lorem Lorem bar.')
        a3 = Answer.objects.create(author=u2, content='foo.')

        q1.answers.add(a1, a3)
        q2.answers.add(a1, a2)

        q1.topics.add(t1, t2)
        q2.topics.add(t1, t2, t3, t4, t5, t6, t7)
        q4.topics.add(t4, t5)

        a1.upvoters.add(u1)
        a1.upvoters.add(u2)
        a2.upvoters.add(u1)
        a2.downvoters.add(u1)

    def test_answers_count(self):
        q = Question.objects.get(title='Question 1?')
        self.assertEqual(q.answers.count(), 2)

    def test_topics_count(self):
        q = Question.objects.get(title='Question 1?')
        self.assertEqual(q.topics.count(), 2)

    def test_upvoters_count(self):
        a = Answer.objects.get(content='Lorem Lorem foo.')
        self.assertEqual(a.upvoters.count(), 2)

    def test_downvoters_count(self):
        a = Answer.objects.get(content='Lorem Lorem bar.')
        self.assertEqual(a.downvoters.count(), 1)

    def test_valid_question(self):
        q = Question.objects.get(title='Question 1?')
        self.assertTrue(q.is_valid_question())

    def test_valid_answer(self):
        a = Answer.objects.get(content='Lorem Lorem foo.')
        self.assertTrue(a.is_valid_answer())

    def test_valid_topic(self):
        t = Topic.objects.get(name='TOPIC1')
        self.assertTrue(t.is_valid_topic())

    def test_invalid_question_topics_count(self):
        q = Question.objects.get(title='Question 2?')
        self.assertFalse(q.is_valid_question())

    def test_invalid_question_views(self):
        q = Question.objects.get(title='Question 3?')
        self.assertFalse(q.is_valid_question())

    def test_invalid_question_repeated_topic_name(self):
        q = Question.objects.get(title='Question 4?')
        self.assertFalse(q.is_valid_question())

    def test_invalid_answer_voters(self):
        a = Answer.objects.get(content='Lorem Lorem bar.')
        self.assertFalse(a.is_valid_answer())

    def test_invalid_answer_length(self):
        a = Answer.objects.get(content='foo.')
        self.assertFalse(a.is_valid_answer())

    def test_invalid_topic_times_used(self):
        t = Topic.objects.get(name='TOPIC7')
        self.assertFalse(t.is_valid_topic())

    def test_invalid_topic_uppercase(self):
        t = Topic.objects.get(name='topic6')
        self.assertFalse(t.is_valid_topic())

    def test_index(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['questions'].count(), 4)

    def test_valid_profile_page(self):
        u = User.objects.get(username='a')
        c = Client()
        response = c.get(f'/profile/{u.id}/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_profile_page(self):
        max_id = User.objects.aggregate(Max('id'))['id__max']
        c = Client()
        response = c.get(f'/profile/{max_id + 1}/')
        self.assertEqual(response.status_code, 404)

    def test_valid_question_page(self):
        q = Question.objects.get(title='Question 1?')
        c = Client()
        response = c.get(f'/question/{q.id}/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_question_page(self):
        max_id = Question.objects.aggregate(Max('id'))['id__max']
        c = Client()
        response = c.get(f'/question/{max_id + 1}/')
        self.assertEqual(response.status_code, 404)