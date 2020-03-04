# Platofy
Platofy is a place on the internet where you can get answers for your questions and share your knowledge by answering other's people questions.  
You can ask any question and tag it accordingly, so people specialized in the specific topic can easily answer your question by filtering questions by topic.  
If you wish to ask a question without everybody knowing that YOU asked the question, you can set the question to be anonymous.

IMG

## Files

### requirements.txt
This text file includes a list with every necessay packet for Platofy.  
Run `pip3 install -r requirements.txt` to install all of them.

### .gitignore
It contains file paths of files and folders that don't neee to be commited.  
For instance, there is no point to commit the environment folder ("env", in this case).

### .travis.yml
It's a yml configuration file that has the purpose of allowing CI.

### qa/context_processor.py
The functions defined in this script will be callable in the Django templates.  
`top_topics` is a functions that returns the top `n` topics from the database based on the number of times the topic has been used.

### qa/forms.py
Every form on Platofy is made with the help of `forms.py` (i.e the login form, the question asking form)  
To render the question asking form to the page, you must import `AskQuestionForm` in `views.py` and give it as context.  

### qa/models.py
This file contains the `Answer`, `Question` and `Topic` modeles.

### qa/tests.py
The purpose of this file is to run a set of tests when the `python3 manage.py test` command is executed.  
In the `setUp` method, we define the variables that are needed for the tests.  
Some of the tests included in this script are:
- testing that the number of upvoters is correct after performing some upvotes
- testing that a question is valid (i.e it has at least 2 words)
- testing that the a 404 error is returned after a profile of a non-existent user was tried to be accessed

### qa/urls.py
The valid URLs live in this file. For example, the 
    `path('profile/<int:uid>/', views.profile, name='profile')` line specifies that 

### qa/utils.py

### qa/views.py
