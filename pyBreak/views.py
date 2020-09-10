from django.shortcuts import render
from django.http import HttpResponse
from .models import Player


# def pyBreak_startpage(request):
#     return render(request, 'pyBreak/paire.html')
#
#
# def index(request):
#     return render(request, 'pyBreak/index.html')
#
#
# def players(request):
#     players_list = Player.objects.order_by('name')
#     players_dict = {'players': players_list}
#     return render(request, 'pyBreak/players.html', context=players_dict)
