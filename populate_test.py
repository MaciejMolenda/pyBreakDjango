import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyBreakDjango.settings')

import django
django.setup()

import pandas as pd

matches_pyBreak = pd.read_csv('/home/bigmac/PycharmProjects/djangoportfolio/pyBreakDjango/pyBreak/ReillyOpelka_abstract.csv')

from pyBreak.models import Matches

matches_store = []

for i in range(len(matches_pyBreak)):
    match = Matches(PyID=matches_pyBreak.iloc[i]['ID'],
    Date=matches_pyBreak.iloc[i]['Date'],
    Tournament=matches_pyBreak.iloc[i]['Tournament'],
    Round=matches_pyBreak.iloc[i]['Round'],
    Tournament_level=matches_pyBreak.iloc[i]['Tournament_level'],
    Surface=matches_pyBreak.iloc[i]['Surface'],
    Rank=matches_pyBreak.iloc[i]['Rank'],
    Rival_rank=matches_pyBreak.iloc[i]['Rival_rank'],
    Rival_hand=matches_pyBreak.iloc[i]['Rival_hand'],
    Rival_name=matches_pyBreak.iloc[i]['Rival_name'],
    Result=matches_pyBreak.iloc[i]['Result'],
    Score=matches_pyBreak.iloc[i]['Score'],
    Aces=matches_pyBreak.iloc[i]['Aces'],
    Double_faults=matches_pyBreak.iloc[i]['Double_faults'],
    First_serve_accuracy=matches_pyBreak.iloc[i]['First_serve_accuracy'],
    First_serve_points=matches_pyBreak.iloc[i]['First_serve_points'],
    Second_serve_points=matches_pyBreak.iloc[i]['Second_serve_points'],
    Total_serve_points_won=matches_pyBreak.iloc[i]['Total_serve_points_won'],
    Breakpoints_saved=matches_pyBreak.iloc[i]['Breakpoints_saved'],
    Breakpoints_todefend=matches_pyBreak.iloc[i]['Breakpoints_todefend'],
    Breakpoints_saved_ratio=matches_pyBreak.iloc[i]['Breakpoints_saved_ratio'],
    Return_1st_serve_points=matches_pyBreak.iloc[i]['Return_1st_serve_points'],
    Return_2nd_serve_points=matches_pyBreak.iloc[i]['Return_2nd_serve_points'],
    Total_return_points=matches_pyBreak.iloc[i]['Total_return_points'],
    Breakpoints_converted=matches_pyBreak.iloc[i]['Breakpoints_converted'],
    Breakpoints_created=matches_pyBreak.iloc[i]['Breakpoints_created'],
    Breakpoints_converted_ratio=matches_pyBreak.iloc[i]['Breakpoints_converted_ratio'],
    Total_points=matches_pyBreak.iloc[i]['Total_points'],
    Service_games_won=matches_pyBreak.iloc[i]['Service_games_won'],
    Service_games_won_ratio=matches_pyBreak.iloc[i]['Service_games_won_ratio'],
    Return_games_won=matches_pyBreak.iloc[i]['Return_games_won'],
    Return_games_won_ratio=matches_pyBreak.iloc[i]['Return_games_won_ratio'],
    Total_games=matches_pyBreak.iloc[i]['Total_games'],
    Total_games_ratio=matches_pyBreak.iloc[i]['Total_games_ratio'],
    Sets=matches_pyBreak.iloc[i]['Sets'],
    Tiebreak_played=matches_pyBreak.iloc[i]['Tiebreak_played'],
    Tiebreak_won=matches_pyBreak.iloc[i]['Tiebreak_won']
    )
    matches_store.append(match)

for i in matches_store:
    print(i)

Matches.objects.bulk_create(matches_store)


