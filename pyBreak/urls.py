from django.urls import path
from . import views

urlpatterns = [
    # path('pairenis.html', views.pyBreak_startpage, name='pairenis'),
    path('index.html', views.startpage, name='index'),
    path('players/<str:id>', views.players, name='players'),
    path('players-stats.html', views.index, name='players-stats'),
    ]
