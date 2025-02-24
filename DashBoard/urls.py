from django.urls import path
from .views import dashboard_view, create_post, edit_post, delete_post

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('create/', create_post, name='create_post'),
    path('edit/<int:post_id>/', edit_post, name='edit_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
]