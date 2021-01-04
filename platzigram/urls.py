""" Platzigram URL Configuration Module """
from django.urls import path

from platzigram import views as local_views
from posts import views as posts_views


urlpatterns = [
    path('hi/', local_views.hi),
    path('posts/', posts_views.list_posts),
]
