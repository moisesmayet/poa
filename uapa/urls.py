from django.urls import path
from .views import *

urlpatterns = [
    path('test', Test, name="test"),
]
