""" Platzigram URL Configuration Module """

# Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# media
from django.conf.urls.static import static

urlpatterns = [
    # Admin url path
    path('admin/', admin.site.urls, name='admin'),
    # Posts url paths
    path('', include(('posts.urls', 'posts'), namespace='posts')),
    # User url paths
    path('users/', include(('users.urls', 'users'), namespace='users')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

