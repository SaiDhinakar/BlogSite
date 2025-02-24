from django.urls import path
from .views import *

urlspattern = [
    path('', settings_view)
]