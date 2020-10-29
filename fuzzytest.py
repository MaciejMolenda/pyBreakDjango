from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import re
import pandas as pd
import os
import requests
import json
import csv
import sys
import numpy as np
import datetime
import time
import html
import string


def fuzzyframes(data_dict, list_of_dataframes):

    for player in data_dict.keys():
        matches_pyBreak = data_dict[player][0]
        odds_pyBreak = data_dict[player][1]

        fullnames = [nazwisko for nazwisko in matches_pyBreak['Rival_name'].to_list()]
        shortnames = [skrot.lower().title().replace('-', ' ') for skrot in odds_pyBreak['Rival_org'].to_list()]
        rivals = []

        # now there is a process which searches for shortnames matching with fullnames from tennis abstract dataframe
        # checks if fullname starts with firstname's first letter and fullname matches with starting string in shortname
        for s in shortnames:
            z = [f for f in fullnames if f.startswith(s.split(' ')[-1][0]) and ''.join(
                re.findall(r'^[a-zA-Z]+\s?[a-zA-Z]*', s[:-3].split(' ')[0])) in f]
            if z:
                rivals.append(z[0])
            else:
                rivals.append('N/A')

        odds_pyBreak['Rival_name'] = rivals
        odds_pyBreak['Date'] = pd.to_datetime(odds_pyBreak['Date'])
        # odds_pyBreak = odds_pyBreak.loc[(odds_pyBreak['Date'] > pd.Timestamp('31/12/2018'))]

        odds_pyBreak = odds_pyBreak[
            ['Date', 'Tournament', 'Rival_org', 'Rival_name', 'Player_odd', 'Rival_odd', 'Score']]
        correct_scores = matches_pyBreak['Score'].to_list()
        matches_pyBreak['Date_Jeff'] = matches_pyBreak['Date']
        matches_pyBreak = matches_pyBreak.drop('Date', 1)
        matches_pyBreak['Score'] = matches_pyBreak.Score.str.replace(', 0-0', '')
        matches_pyBreak['Score'] = matches_pyBreak.Score.str.replace(', RET', '')
        matches_pyBreak['Score'] = np.where(matches_pyBreak['Tournament'] == 'Roland Garros',
                                            (matches_pyBreak['Score'].str.replace(r'\(\d*\)', '', regex=True)),
                                            matches_pyBreak['Score'])
        odds_pyBreak['Score'] = np.where(odds_pyBreak['Tournament'] == 'French Open',
                                         (odds_pyBreak['Score'].str.replace(r'\(\d*\)', '', regex=True)),
                                         odds_pyBreak['Score'])
        odds_pyBreak['Score'] = odds_pyBreak.Score.str.replace(', 0-0', '')
        odds_pyBreak['Score'] = odds_pyBreak.Score.str.replace(r'6\d-6\d', '6-6', regex=True)
        del odds_pyBreak['Tournament']

        df = pd.DataFrame.merge(matches_pyBreak, odds_pyBreak, on=['Rival_name', 'Score'], how='outer', indicator=True)
        df = df[df['_merge'] != 'right_only']

        for index, row in df.iterrows():
            if row['_merge'] == 'left_only':
                startdate = row['Startdate']
                finaldate = row['Finaldate']
                score = row['Score']
                match_row = (odds_pyBreak[(odds_pyBreak['Score'] == score) &
                                          (odds_pyBreak['Date'] >= startdate) &
                                          (odds_pyBreak['Date'] <= finaldate) &
                                          (odds_pyBreak['Rival_org'].str[-2] == row['Rival_name'][0])
                                          ])

                print(player, 'index: ', index, 'row: ', len(match_row))

                if len(match_row) > 0:
                    df.loc[index, 'Date'] = match_row['Date'].values[0]
                    df.loc[index, 'Player_odd'] = match_row['Player_odd'].values[0]
                    df.loc[index, 'Rival_odd'] = match_row['Rival_odd'].values[0]

        df['Date'] = np.where(df['Date'].isnull(), df['Date_Jeff'], df['Date'])
        del df['Startdate'], df['Finaldate'], df['Date_Jeff'], df['Rival_org'], df['_merge']

        colnames = df.columns.tolist()
        colnames.insert(1, colnames.pop(-3))
        colnames.insert(10, colnames.pop(-2))
        colnames.insert(11, colnames.pop(-1))

        df = df[colnames]

        def change_to_int(col):
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        for col in ['Rank', 'Rival_rank', 'Aces', 'Double_faults', 'Breakpoints_saved', 'Breakpoints_todefend',
                    'Breakpoints_converted', 'Breakpoints_created', 'Sets', 'Tiebreak_played', 'Tiebreak_won']:
            change_to_int(col)

        list_of_dataframes.append(df)
        df.to_csv('%s_pyBreak.csv' % player)
