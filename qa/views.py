from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm, RegisterForm, AskQuestionForm, AnswerQuestionForm
from .models import Answer, Question, Topic

import json
import re

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

            # Convert the string '[{"value":"a"},{"value":"B"},{"value":"b"}]' to {'A', 'B'}
            topics_names = {x['value'].upper() for x in json.loads(form_data['topics'])}
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
    
    # Get the every questions except for those asked by the user
    questions = Question.objects.exclude(author=request.user)
    # Get the name of the topic from the URL's query string
    topic_name = request.GET.get("topic")

    # If the user provided a "topic_name" URL query string
    if topic_name:
        try:
            topic = Topic.objects.get(name=topic_name.upper())
        except Topic.DoesNotExist:
            topic = None

        # Get every question with the specified topic
        questions = questions.filter(topics=topic)

    return render(
        request,
        'qa/index.html',
        context={
            'ask_form': ask_form,
            'questions': questions
        }
    )

def profile(request, uid):
    """ Renders the a specified user's profile """
    user = User.objects.get(id=uid)
    questions = Question.objects.filter(author=user)
    answers = Answer.objects.filter(author=user)
    # Questions asked, excluing the anonymous questions
    public_questions = questions.filter(type='public')
    upvotes_received = answers.aggregate(Count('upvoters'))['upvoters__count']
    upvotes_given = Answer.objects.filter(upvoters=user).count()

    return render(
        request,
        'qa/profile.html',
        context={
            'viewed_user': user,
            'questions': questions,
            'answers': answers,
            'public_questions': public_questions,
            'upvotes_received': upvotes_received,
            'upvotes_given': upvotes_given
        }
    )

def question(request, question_id):
    """ Renders question pages and handles question answerings """
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

def vote(request):
    """ Answer upvote and downvote feature """
    uid = request.POST.get('user_id')
    answer_id = request.POST.get('answer_id')
    vote_type = request.POST.get('vote_type')
    user = User.objects.get(id=uid)
    answer = Answer.objects.get(id=answer_id)
    upvoters = answer.upvoters
    downvoters = answer.downvoters

    if vote_type == 'upvote':
        # If the user is already a upvoter, remove the upvote
        if user.id in upvoters.values_list('id', flat=True):
            upvoters.remove(user)
        # Else, remove the downvote (if the user is a downvoter), and add an upvote
        else:
            downvoters.remove(user)
            upvoters.add(user)
    else:
        # If the use is already a downvoter, remove the downvote
        if user.id in downvoters.values_list('id', flat=True):
            downvoters.remove(user)
        # Else, remove the upvote (if the user is an upvoter), and add a downvote
        else:
            upvoters.remove(user)
            downvoters.add(user)

    return HttpResponse(json.dumps({
        'new_points': upvoters.count() - downvoters.count()
    }))

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