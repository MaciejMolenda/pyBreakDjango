from django.urls import path
from . import views

urlpatterns = [
    path('index.html', views.startpage, name='startpage'),
    ]