'''
DATA > URLS.py
'''

from django.urls import path

from . import views

urlpatterns = [
    path('', views.ranking, name='ranking'),
]
