""" Posts views. """

# Django
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

# Models
from posts.models import Post

# Forms
from posts.forms import PostForm

class PostDetailView(LoginRequiredMixin, DetailView):
    """ Return post detail """

    template_name = "posts/detail.html"
    queryset = Post.objects.all()
    context_object_name = 'post'

class PostFeedView(LoginRequiredMixin, ListView):
    """ Return all published posts. """
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created')
    paginate_by = 20
    context_object_name = 'posts'

class CreatePostView(LoginRequiredMixin, CreateView):
    """ Create a post """
    template_name='posts/new.html'
    form_class= PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile 
        return context
    