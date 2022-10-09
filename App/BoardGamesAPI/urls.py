from django.urls import path,include
from rest_framework import routers

from . import views

urlpatterns=[
    path('games/getAllGames',views.getAllGames,name='games/getAllGames'),
    path('games/top10',views.top10,name='games/top10')
    
    
    ]