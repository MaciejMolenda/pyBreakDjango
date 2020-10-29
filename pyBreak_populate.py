import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyBreakDjango.settings')

import django
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas as pd
import requests
import json
import csv
import sys
import numpy as np
import sqlite3

from baseabstract import abstract_parse
from tennisexp import tennisexp_parse
from fuzzytest import fuzzyframes


from pyBreak.models import RankingPyBreak
from pyBreak.models import DataPyBreak

matches_store = []
rank_store = []

RankingPyBreak.objects.all().delete()
DataPyBreak.objects.all().delete()

try:
    options = Options()
    # options.add_argument("--headless")
    chromedriver = "/home/bigmac/Downloads/chromedriver"
    driver = webdriver.Chrome(chromedriver, options=options)
except WebDriverException as e:
    print("Zainstaluj przeglądarkę Google Chrome oraz odpowiednią"
          " dla niej wersję chromedriver"
          "\n%s" % e)
    sys.exit()

driver.get("https://www.minorleaguesplits.com/tennisabstract/cgi-bin/jsplayers/curr_rank_atp.js")
bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
var = json.loads((re.findall(r'{.+}', str(bs_obj)))[0])
ranking = dict((k, int(v)) for k, v in var.items())
ranking_pyBreak = (
    pd.DataFrame(ranking.items(), columns=['Player', 'Rank']).sort_values('Rank', ascending=True))
ranking_pyBreak['PyID'] = ranking_pyBreak['Player'].str.replace(' ', '')

top200 = ranking_pyBreak.loc[ranking_pyBreak['Rank'] <= 200]
top200IDs = [player.replace(' ', '') for player in list(top200['Player'])]

data_dict = {player: [] for player in top200IDs}

today = datetime.now()
dayname = datetime.strftime(today, '%Y')+ datetime.strftime(today, '%m') + datetime.strftime(today, '%d')

list_of_dataframes = []

abstract_parse(driver, top200IDs, data_dict)
tennisexp_parse(top200, ranking_pyBreak, data_dict)
driver.quit()

fuzzyframes(data_dict, list_of_dataframes)
data_pyBreak = pd.concat(list_of_dataframes)
data_pyBreak['Player_odd'] = pd.to_numeric(data_pyBreak['Player_odd'], errors='coerce').astype('float')
data_pyBreak['Rival_odd'] = pd.to_numeric(data_pyBreak['Rival_odd'], errors='coerce').astype('float')

for i in range(len(ranking_pyBreak)):
    record = RankingPyBreak(PyID=ranking_pyBreak.iloc[i]['PyID'],
                            Rank=ranking_pyBreak.iloc[i]['Rank'],
                            Name=ranking_pyBreak.iloc[i]['Player'])
    rank_store.append(record)


for i in range(len(data_pyBreak)):
    match = DataPyBreak(PyID=data_pyBreak.iloc[i]['PyID'],
    Date=data_pyBreak.iloc[i]['Date'],
    Tournament=data_pyBreak.iloc[i]['Tournament'],
    Round=data_pyBreak.iloc[i]['Round'],
    Tournament_level=data_pyBreak.iloc[i]['Tournament_level'],
    Surface=data_pyBreak.iloc[i]['Surface'],
    Rank=data_pyBreak.iloc[i]['Rank'],
    Rival_rank=data_pyBreak.iloc[i]['Rival_rank'],
    Rival_hand=data_pyBreak.iloc[i]['Rival_hand'],
    Rival_name=data_pyBreak.iloc[i]['Rival_name'],
    Player_odd=data_pyBreak.iloc[i]['Player_odd'],
    Rival_odd=data_pyBreak.iloc[i]['Rival_odd'],
    Result=data_pyBreak.iloc[i]['Result'],
    Score=data_pyBreak.iloc[i]['Score'],
    Match_completed=data_pyBreak.iloc[i]['Match_completed'],
    Aces=data_pyBreak.iloc[i]['Aces'],
    Double_faults=data_pyBreak.iloc[i]['Double_faults'],
    First_serve_accuracy=data_pyBreak.iloc[i]['First_serve_accuracy'],
    First_serve_points=data_pyBreak.iloc[i]['First_serve_points'],
    Second_serve_points=data_pyBreak.iloc[i]['Second_serve_points'],
    Total_serve_points_won=data_pyBreak.iloc[i]['Total_serve_points_won'],
    Breakpoints_saved=data_pyBreak.iloc[i]['Breakpoints_saved'],
    Breakpoints_todefend=data_pyBreak.iloc[i]['Breakpoints_todefend'],
    Breakpoints_saved_ratio=data_pyBreak.iloc[i]['Breakpoints_saved_ratio'],
    Return_1st_serve_points=data_pyBreak.iloc[i]['Return_1st_serve_points'],
    Return_2nd_serve_points=data_pyBreak.iloc[i]['Return_2nd_serve_points'],
    Total_return_points=data_pyBreak.iloc[i]['Total_return_points'],
    Breakpoints_converted=data_pyBreak.iloc[i]['Breakpoints_converted'],
    Breakpoints_created=data_pyBreak.iloc[i]['Breakpoints_created'],
    Breakpoints_converted_ratio=data_pyBreak.iloc[i]['Breakpoints_converted_ratio'],
    Total_points=data_pyBreak.iloc[i]['Total_points'],
    Service_games_won=data_pyBreak.iloc[i]['Service_games_won'],
    Service_games_won_ratio=data_pyBreak.iloc[i]['Service_games_won_ratio'],
    Return_games_won=data_pyBreak.iloc[i]['Return_games_won'],
    Return_games_won_ratio=data_pyBreak.iloc[i]['Return_games_won_ratio'],
    Total_games=data_pyBreak.iloc[i]['Total_games'],
    Total_games_ratio=data_pyBreak.iloc[i]['Total_games_ratio'],
    Sets=data_pyBreak.iloc[i]['Sets'],
    Tiebreak_played=data_pyBreak.iloc[i]['Tiebreak_played'],
    Tiebreak_won=data_pyBreak.iloc[i]['Tiebreak_won'])

    matches_store.append(match)

RankingPyBreak.objects.bulk_create(rank_store)
DataPyBreak.objects.bulk_create(matches_store)


