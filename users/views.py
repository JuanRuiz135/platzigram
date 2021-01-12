""" User views module """

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile

# Forms
from users.forms import SignupForm


class UserDetailView(LoginRequiredMixin, DetailView):
    """ User detail; view. """

    template_name = "users/detail.html"
    slug_field = 'username'
    slug_url_kwarg = 'username' # this is the name that is assigned in the urls side 
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context
    
class SignupView(FormView):
    """ Users sign up view. """
    template_name='users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('posts:feed')

    def form_valid(self, form):
        """ Save form data and logs the user in. """
        form.save()

        username = form['username'].value()
        password = form['password'].value()

        user = authenticate(
            self.request, username=username, password=password)
        
        login(self.request, user)

        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """ Update profile view. """
    template_name='users/update_profile.html'
    model= Profile
    fields= ['website','biography','phone_number','picture']

    def get_object(self):
        """ Return user's profile """
        return self.request.user.profile

    def get_success_url(self):
        """ Returns to user's profile """
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})


def login_view(request):
    """ Login view """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('posts:feed')
        else:
            return render(request, 'users/login.html', {'login_error': 'Invalid username and password'})
        
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    """ Logout a user """
    logout(request)
    return redirect('users:login')