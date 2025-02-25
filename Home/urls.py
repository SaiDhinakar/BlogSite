from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('categories/', views.category_list, name='category_list'),
    path('search/', views.search_posts, name='search_posts'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('my-posts/', views.user_posts, name='user_posts'),
    path('load-more-posts/', views.load_more_posts, name='load_more_posts'),
    path('author/<str:username>/', views.author_posts, name='author_posts'),
]