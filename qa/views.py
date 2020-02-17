from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.models import User

from .models import Answer, Question, Topic
from .forms import LoginForm, RegisterForm, AskQuestionForm, AnswerQuestionForm

import re
import json

def index(request):
    """ Renders index.html for GET requests and creates questions for POST requests """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        # "request.POST" as argument, fills the form with user input 
        ask_form = AskQuestionForm(request.POST)

        if ask_form.is_valid():
            # Get the user that is logged in
            user = User.objects.get(id=request.user.id)
            form_data = ask_form.cleaned_data

            # Convert the string '[{"value":"aaa"},{"value":"bbb"},{"value":"bbb"}]' to {'a', 'b'}
            topics_names = {x['value'] for x in json.loads(form_data['topics'])}
            topics = Topic.objects.filter(name__in=topics_names)

            for topic_name in topics_names:
                # Try to increment the number of times the topic was used 
                try:
                    topic = Topic.objects.get(name=topic_name)
                    topic.times_used += 1
                    topic.save()
                # If the selected topic doesn't exist yet
                except Topic.DoesNotExist:
                    Topic.objects.create(name=topic_name)

            topics = Topic.objects.filter(name__in=topics_names)

            # Create the question submitted by the user
            question = Question.objects.create(
                author=user,
                title=form_data['title'],
                details=form_data['details'],
                question_type=form_data['question_type']
            )
            
            # Link the selected topics to the question
            question.topics.set(topics)

            # Redirect to the question page 
            return HttpResponseRedirect(reverse('question', args=[question.id]))
    # If the request method is GET, use an empty form
    else:
        ask_form = AskQuestionForm()

    questions = Question.objects.all()

    return render(
        request,
        'qa/index.html',
        context={
            'ask_form': ask_form,
            'questions': questions
        }
    )

def profile(request, uid):
    """ """
    user = User.objects.get(id=uid)
    questions = Question.objects.filter(author=user)

    return render(request, 'qa/profile.html', context={'viewed_user': user, 'questions': questions})

def question(request, question_id):
    """ """
    question = Question.objects.get(id=question_id)
    answer_form = AnswerQuestionForm()
    answers_authors = [answer.author for answer in question.answers.all()]
    can_answer = request.user.is_authenticated and question.author.id != request.user.id and request.user not in answers_authors

    if request.method == 'POST':
        answer_form = AnswerQuestionForm(request.POST)

        # If the user tries to answer his own question OR
        # he tries to answer a question he already answered to
        if not can_answer:
            return HttpResponseRedirect(reverse('index'))

        if answer_form.is_valid():
            content = answer_form.cleaned_data['content']
            # Get the user that is logged in
            user = User.objects.get(id=request.user.id)
            # Clear the form
            answer_form = AnswerQuestionForm()
            # Create the answer submitted by the user
            answer = Answer.objects.create(author=user, content=content)
            # Automatically upvotes the user's own answer
            answer.upvoters.add(request.user)
            # Add the answer to the "list" of answers of the questions
            question.answers.add(answer)
    else:
        # Increment the number of views by one, if the user is not the author
        if request.user != question.author:
            question.views += 1
            question.save()

    return render(
        request,
        'qa/question.html',
        context={
            'question': question,
            'can_answer': can_answer,
            'answer_form': answer_form
        }
    )


def login(request):
    """ Logs the user in """
    if request.method == 'POST':
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        form = LoginForm(request.POST)

        # If the form is valid, log the user in
        if form.is_valid():
            user = authenticate(username=usern, password=passw)
            login_user(request, user)

            return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()

    return render(request, 'qa/login.html', context={'form': form})

def register(request):
    """ Registers the user """
    if request.method == 'POST':
        usern = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('first_name').title() # e.g converts "de jon" into "De Jon"
        lname = request.POST.get('last_name').title()
        passw = request.POST.get('password')
        confr = request.POST.get('confirm')
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Register the user
            user = User.objects.create_user(
                username=usern,
                email=email,
                first_name=fname,
                last_name=lname,
                password=passw
            )
            login_user(request, authenticate(username=usern, password=passw))
            
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, 'qa/register.html', context={'form': form})

def logout(request):
    """ Signs the user out """
    logout_user(request)

    return HttpResponseRedirect(reverse('index'))