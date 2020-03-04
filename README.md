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
