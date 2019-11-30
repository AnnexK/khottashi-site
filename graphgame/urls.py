from django.urls import path

from . import views

app_name = 'graphgame'
urlpatterns = [
    path('', views.game, name='game'),
]
