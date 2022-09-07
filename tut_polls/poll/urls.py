from django.urls import path
from .views import index

urlpatterns = [
    path('questions', index, name='index')
]
