from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Profile
from django.forms.widgets import DateInput

class LoginForm(forms.Form):
    '''
    Form used to authenticate users against the database.
    Required fields include username and password.
    '''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    '''
    Form used to register users, which allows them to enter a username, real name, and a password.
    Checks the second password against the first one and does not allow the form to validate if they don't match.
    Required fields include username, password, and password2. All other fields are optional.
    '''
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

class UserEditForm(forms.ModelForm):
    '''
    Allow users to edit their first name, last name, and email, which are attributes of the built-in Django User model.
    No required fields. Optional fields include first_name, last_name, and email.
    '''
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    '''
    Allow users to edit the profile data to save in the Profile model.
    Users will be able to edit their date of birth and upload a picture for their profile.
    No required fields. Optional fields include date_of_birth and photo.
    '''
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
        widgets = {'date_of_birth': DateInput(attrs={'type':'date'})}
