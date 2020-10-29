from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import DataPyBreak, RankingPyBreak, PlayersSummary, PlayersOvrYear, PlayersOvrCurrent, PlayersClay, PlayersClayCurrent, PlayersClayYear, PlayersHard, PlayersHardCurrent, PlayersHardYear
from django.db import connection
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.core import serializers
import json

def startpage(request):
    return render(request, 'pyBreak/index.html')

def index(request):
    player = PlayersSummary.objects.all
    ovr = serializers.serialize('json', PlayersSummary.objects.all())
    players_dict = {'player': player, 'ovr': ovr}
    return render(request, 'pyBreak/players-stats.html', context=players_dict)
#
#
def players(request, id):
    player = get_object_or_404(PlayersSummary, pk=id)
    player_columns = [field.name for field in PlayersSummary._meta.get_fields()]
    ovrobj = PlayersSummary.objects.all()
    ovr = serializers.serialize('json', PlayersSummary.objects.all())
    ovryear = serializers.serialize('json', PlayersOvrYear.objects.all())
    ovrcur = serializers.serialize('json', PlayersOvrCurrent.objects.all())
    clay = serializers.serialize('json', PlayersClay.objects.all())
    clayyear = serializers.serialize('json', PlayersClayYear.objects.all())
    claycur = serializers.serialize('json', PlayersClayCurrent.objects.all())
    hard = serializers.serialize('json', PlayersHard.objects.all())
    hardyear = serializers.serialize('json', PlayersHardYear.objects.all())
    hardcur = serializers.serialize('json', PlayersHardCurrent.objects.all())


    players_dict = {'player': player, 'label': player_columns,
                    'ovr': ovr, 'ovryear': ovryear, 'ovrcur': ovrcur,
                    'clay': clay, 'clayyear': clayyear, 'claycur': claycur,
                    'hard': hard, 'hardyear': hardyear, 'hardcur': hardcur,
                    'ovrobj': ovrobj}
    return render(request, 'pyBreak/players.html', context=players_dict)