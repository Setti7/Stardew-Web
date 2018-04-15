'''
DATA > URLS.py
'''

from . import views
from django.urls import path, include
# from django.contrib import admin
# from django.views.generic import RedirectView
# from django.contrib.auth import views as auth_views
# from StardewWeb import views as core_views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('', views.ranking, name='ranking'),
    #path('data/generos', views.data_genero, name='data-generos'),

]



