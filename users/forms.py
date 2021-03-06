""" User forms. """

# Django 
from django import forms 

# Models
from django.contrib.auth.models import User
from users.models import Profile

class SignupForm(forms.Form):
    """ Signup form """

    username = forms.CharField(min_length=4, max_length=50, required=True)

    password = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.PasswordInput()
    )

    first_name = forms.CharField(min_length=3, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )

    def clean_username(self):
        """ username must be unique """
        # get the username from the cleaned data
        username = self.cleaned_data['username'] 
        # check if it exists in the db 
        username_taken = User.objects.filter(username=username).exists()

        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        
        return username
    
    def clean_email(self):
        """ email must be unique """
        # get the username from the cleaned data
        email = self.cleaned_data['email'] 
        # check if it exists in the db 
        email_taken = User.objects.filter(email=email).exists()

        if email_taken:
            raise forms.ValidationError('Email is already in use.')
        
        return email
    
    def clean(self):
        """ Verify password confirmation match. """

        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')

        return data
    
    def save(self):
        """ Create user and profile """
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()