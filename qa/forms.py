from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# from .models import UserAvatar
from .utils import QUESTION_TYPES, question_format

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=64, widget=forms.TextInput(attrs={'data-label': 'Username'})
    )
    password = forms.CharField(
        max_length=64, widget=forms.PasswordInput(attrs={'data-label': 'Password'})
    )

    # Method that is called after the login for form was submitted 
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        usern = cleaned_data.get('username')
        passw = cleaned_data.get('password')
        user = authenticate(username=usern, password=passw)

        # If the credetials are invalid
        if user is None:
            msg = 'There is no username with that password.'
            self.add_error('password', msg)

        return cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'data-label': 'Username'})
    )
    email = forms.CharField(
        max_length=64,
        widget=forms.EmailInput(attrs={'data-label': 'Email'})
    )
    first_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'data-label': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'data-label': 'Last Name'})
    )
    password = forms.CharField(
        max_length=64,
        widget=forms.PasswordInput(attrs={'data-label': 'Password'})
    )
    confirm = forms.CharField(
        label='Confirm Password',
        max_length=64,
        widget=forms.PasswordInput(attrs={'data-label': 'Confirm Password'})
    )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        usern = cleaned_data.get('username')
        email = cleaned_data.get('email')
        fname = cleaned_data.get('first_name').title() # e.g converts "de jon" into "De Jon"
        lname = cleaned_data.get('last_name').title()
        passw = cleaned_data.get('password')
        confr = cleaned_data.get('confirm')
        PASS_MIN_LENGTH = 8

        # Check the username is already taken
        if User.objects.filter(username=usern):
            self.add_error('username', 'Username is already taken.')

        # Check the email is already taken
        if User.objects.filter(email=email):
            self.add_error('email', 'Email is already taken.')

        # Check that the first name doesn't have only letters
        if not fname.isalpha():
            self.add_error('first_name', 'First name is not valid.')

        # Check that the last name doesn't have only letters
        if not lname.isalpha():
            self.add_error('last_name', 'Last name is not valid.')

        # Check for min length
        if len(passw) < PASS_MIN_LENGTH:
            self.add_error('password', f'Password must be at least {PASS_MIN_LENGTH} characters long.')

        # Check for digit
        if sum(c.isdigit() for c in passw) < 1:
            self.add_error('password', 'Password must contain at least 1 number.')

        # Check for uppercase letter
        if not any(c.isupper() for c in passw):
            self.add_error('password', 'Password must contain at least 1 uppercase letter.')

        # Check for lowercase letter
        if not any(c.islower() for c in passw):
            self.add_error('password', 'Password must contain at least 1 lowercase letter.')

        # Check for matching between password and confirmation
        if passw and confr:
            if passw != confr:
                self.add_error('confirm', 'The two password fields must match.')

        # Return the new clean data (the inputs without errors)
        return cleaned_data 

class AskQuestionForm(forms.Form):
    title = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    details = forms.CharField(max_length=512, required=False, widget=forms.Textarea(attrs={'rows': 5}))
    question_type = forms.ChoiceField(choices=QUESTION_TYPES)

    def clean(self):
        cleaned_data = super(AskQuestionForm, self).clean()
        title = question_format(cleaned_data.get('title'))
        
        # If the title of the question doesn't end in a question mark
        if title[-1] != '?':
            self.add_error('title', 'The question must end with a question mark.')
        
        # If the title has less than 2 words
        if len(title.split(' ')) < 2:
            self.add_error('title', 'The question must have at least 2 words.')

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return cleaned_data

class AnswerQuestionForm(forms.Form):
    content = forms.CharField(max_length=4096, required=False, widget=forms.Textarea(attrs={'rows': 5}))

    def clean_content(self):
        content = self.cleaned_data['content']

        if not content:
            raise forms.ValidationError('The answer is not valid.')

        return content