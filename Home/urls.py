from django.urls import path
from .views import *

urlpatterns = [
    path('',home),
    path('create_post/', create_post, name='create_post'),
    path('search_post/', search_posts, name='search_posts'),
    path('load_more_posts/', load_more_posts, name='load_more_posts'),
]