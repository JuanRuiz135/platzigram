""" Platzigram middleware catalog """

# Django
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from users.models import Profile
from django.urls import reverse

class ProfileCompletionMiddleware:
    """ Profile completion middleware.

    Ensure every user that interacts with the platform has a 
    picture and a biography. """

    def __init__(self, get_response):
        """ Middleware initialization """
        self.get_response = get_response

    def __call__(self, request):
        """ Code to be executed for each request before the view is called. """
        # first check if the user is logged in
        if not request.user.is_anonymous:
            profile = request.user.profile
            # check if the profile picture or the biography exists
            if not profile.picture or not profile.biography:
                if request.path not in [reverse('update_profile'), reverse('logout')]:
                    return redirect('update_profile')
        
        response = self.get_response(request)
        return response