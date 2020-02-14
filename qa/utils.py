import re

QUESTION_TYPES = (('public', 'Public'), ('anonymous', 'Anonymous'))

def question_format(title):
    """Formats a question to be a bit more gramatically correct"""
    title = title.capitalize()
    title = re.sub(r' +', ' ', title) # Replaces '  a  ' with ' a ' 
    title = re.sub(r' \?', '?', title)
    # Removes the possible addition space at the end of the question
    title = re.sub(r'\? $', '?', title)

    return title