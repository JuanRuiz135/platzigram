""" User views module """

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Models
from django.contrib.auth.models import User
from users.models import Profile

# Exceptions
from django.db.utils import IntegrityError

# Forms
from users.forms import ProfileForm

@login_required
def update_profile(request):
    """ Update user's profile view. """
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']

            profile.save()

            return redirect('update_profile')
    else:
        form = ProfileForm()

    return render(request, template_name = 'users/update_profile.html', context={
        'profile': profile,
        'user': request.user,
        'form': form,
    })

def signup(request):
    """ sign up view """
    if request.method == "POST":
        username = request.POST['username']
        passwd = request.POST['passwd']
        passwd_confirmation = request.POST['passwd_confirmation']

        # check password confirmation
        if passwd != passwd_confirmation:
            return render(request, 'users/signup.html', {'passswd_error': 'Password confirmation does not match.'})

        # create user
        try:
            user = User.objects.create_user(username=username, password=passwd)
        except IntegrityError:
            return render(request, 'users/signup.html', {'username_error': 'Username is already in use.'})

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        # create profile for user
        profile = Profile.objects.get_or_create(user=user)

        return redirect('login')
        
    return render(request, 'users/signup.html')

def login_view(request):
    """ Login view """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('feed')
        else:
            return render(request, 'users/login.html', {'login_error': 'Invalid username and password'})
        
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    """ Logout a user """
    logout(request)
    return redirect('login')