from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import date
import re
import pandas as pd
import os
import requests
import json
import csv
import sys
import numpy as np
import datetime
import sqlite3


def abstract_parse(driver, top200IDs, data_dict):
    startlink = "http://tennisabstract.com/cgi-bin/player-classic.cgi?p="
    players = [startlink + player for player in top200IDs]

    count = 0
    for p in players:
        imie = p.split('=')[1]
        print(imie)
        driver.get(str(p))

        # wyciąganie zmiennych z twardymi danymi dotyczącymi spotkań, potrzebnymi do utworzenia tabeli z danymi i przetłumaczenia niektórych skrótów myślowych Jeffa
        headers = driver.execute_script("return matchhead")
        data = driver.execute_script("return matchmx")
        currank = driver.execute_script("return currentrank")
        levdict2 = driver.execute_script("return levdict2")
        rddict2 = driver.execute_script("return rddict2")
        levdict2['C'] = 'Challengers'
        levdict2['A'] = 'ATP'
        resultdict = {'W': 'Win', 'L': 'Lose', 'U': 'To be played'}
        handsdict = {'R': 'Right', 'L': 'Left', 'U': 'Unknown'}

        # DO NAPRAWIENIA opcja pandas pozwalająca wyświetlać przyjemny format procentowy, właściwy dla typu danych float64 jakie przechowujemy w tabeli,
        # niestety taka forma występuje jedynie podczas pracy w Py zapis dataframe do pliku csv  w ostatniej linii umożliwia jedynie opcję decimal (np. 0.64)
        # dałoby radę pozamieniać format permanentnie funkcją "map" dla pd ale ona spowalnia, wręcz wiesza program podczas egzekucji, nie do przyjęcia
        pd.set_option('display.float_format', '{:,.2%}'.format)

        # kryterium zaciągania meczów tylko z ostatniego roku, od aktualnej daty
        # year_criteria = pd.Timestamp.today() - datetime.timedelta(weeks=52)
        # wyhaszowane przez covid, kiedyś do poprawy
        year_criteria = pd.Timestamp('30/12/2018')

        # baza tennisabstract i utworzona od zera nasza autorska
        jeff_df = pd.DataFrame(data=data, columns=headers)
        matches_pyBreak = pd.DataFrame()

        # tworzenie kolumn tabeli pyBreak na podstawie danych ze zmiennej matchmx źródła tennisabstract.com
        matches_pyBreak['Date'] = pd.to_datetime(jeff_df['date'])
        matches_pyBreak = matches_pyBreak.loc[(matches_pyBreak['Date'] > year_criteria)]
        matches_pyBreak['Tournament'] = jeff_df['tourn']
        matches_pyBreak['Round'] = jeff_df['round']
        matches_pyBreak['Tournament_level'] = jeff_df['level']
        matches_pyBreak['Surface'] = jeff_df['surf']
        matches_pyBreak['Rank'] = pd.to_numeric(jeff_df['rank'], errors='coerce').fillna(0).astype(int)
        matches_pyBreak['Rival_rank'] = pd.to_numeric(jeff_df['orank'], errors='coerce').fillna(0).astype(int)
        matches_pyBreak['Rival_hand'] = jeff_df['ohand']
        matches_pyBreak['Rival_name'] = jeff_df['opp']
        matches_pyBreak['Result'] = jeff_df['wl']

        # ustawienie kryterium roku czasu i przetłumaczenia skrótów myślowych Jeffa w dwóch kolumnach
        matches_pyBreak['Tournament_level'].replace(levdict2, inplace=True)
        matches_pyBreak['Round'].replace(rddict2, inplace=True)
        matches_pyBreak['Result'].replace(resultdict, inplace=True)
        matches_pyBreak['Rival_hand'].replace(handsdict, inplace=True)

        # ustalenie długości kolumn i utworzenie list do odwrócenia wyniku przegranego meczu
        length = (matches_pyBreak.shape[0])
        scores_win = []
        scores_reversed = []
        scores = list(jeff_df['score'])[:length]
        sets = []

        for line in scores:
            spaces = r"\s+"
            line = re.split(spaces, line)
            scores_win.append(line)
            sets.append(len(line))

        def reversescore(s): # function to get reversed match score in case of possible match lose
            if len(s) > 3: # match score is list of strings, if there was tiebreak, it's length is > 3 because it looks like '7-6(4)'
                s1 = ''.join(reversed(s[:3])) + s[3:] # there's only set score to reverse, tiebreak score in parenth. to be saved
                return s1
            else:
                if s in ['RET', 'W/O']: # case of set not contested
                    return s
                else:
                    s = ''.join(reversed(s[:3])) # set score without tiebreak to be reversed
                    return s

        for score in scores_win:
            scores_reversed.append(list((reversescore(s) for s in score)))
        # utworzenie właściwej kolumny z wynikiem z perspektywy wygranej/przegranej w meczu oraz kolejnych kolumn
        # styl wymuszony zniwelowaniem błędów wynikających z ewentualnych pustych komórek danych z tennisabstract

        def num_valid(col):
            new_col = pd.to_numeric(jeff_df[col], errors='coerce').fillna(0)
            return new_col

        matches_pyBreak['Score_list'] = np.where(matches_pyBreak['Result'] == 'Win', scores_win, scores_reversed)
        matches_pyBreak['Score'] = matches_pyBreak['Score_list'].apply(', '.join)
        matches_pyBreak['Match_completed'] = np.where(matches_pyBreak['Score'].str.contains('RET'), 'No', 'Yes')
        matches_pyBreak['Match_completed'] = np.where(matches_pyBreak['Score'].str.contains('Def'), 'No', 'Yes')
        matches_pyBreak['Aces'] = num_valid('aces').astype(int)
        matches_pyBreak['Double_faults'] = num_valid('dfs').astype(int)
        matches_pyBreak['First_serve_accuracy'] = (num_valid('firsts') / num_valid('pts'))
        matches_pyBreak['First_serve_points'] = (num_valid('fwon') / num_valid('firsts'))
        matches_pyBreak['Second_serve_points'] = (num_valid('swon') / (num_valid('pts') - num_valid('firsts')))
        matches_pyBreak['Total_serve_points_won'] = (num_valid('fwon') + num_valid('swon')) / num_valid('pts')
        matches_pyBreak['Breakpoints_saved'] = num_valid('saved').astype(int)
        matches_pyBreak['Breakpoints_todefend'] = num_valid('chances').astype(int)
        matches_pyBreak['Breakpoints_saved_ratio'] = num_valid('saved') / num_valid('chances')
        matches_pyBreak['Return_1st_serve_points'] = (num_valid('ofirsts') - num_valid('ofwon')) / num_valid('ofirsts')
        matches_pyBreak['Return_2nd_serve_points'] = (num_valid('opts') - num_valid('ofirsts') - num_valid('oswon')) / (
                    num_valid('opts') - num_valid('ofirsts'))
        matches_pyBreak['Total_return_points'] = (num_valid('opts') - num_valid('ofwon') - num_valid('oswon')) / num_valid('opts')
        matches_pyBreak['Breakpoints_converted'] = (num_valid('ochances').astype(int) - num_valid('osaved').astype(int))
        matches_pyBreak['Breakpoints_created'] = num_valid('ochances').astype(int)
        matches_pyBreak['Breakpoints_converted_ratio'] = (num_valid('ochances').astype(int) - num_valid('osaved').astype(int)) / num_valid('ochances')
        matches_pyBreak['Total_points'] = (num_valid('fwon') + num_valid('swon') + num_valid('opts') - num_valid('ofwon') - num_valid('oswon')) / (num_valid('pts') + num_valid('opts'))
        matches_pyBreak['Service_games_won'] = (num_valid('games').astype(int) - num_valid('chances').astype(int) + num_valid('saved').fillna(0).astype(int)).astype(str) + '/' + (num_valid('games').astype(int).astype(str))
        matches_pyBreak['Service_games_won_ratio'] = (num_valid('games') - num_valid('chances') + num_valid('saved')) / num_valid('games')
        matches_pyBreak['Return_games_won'] = (num_valid('ochances').astype(int) - num_valid('osaved').fillna(0).astype(int)).astype(str) + '/' + (num_valid('ogames').astype(int).astype(str))
        matches_pyBreak['Return_games_won_ratio'] = (num_valid('ochances') - num_valid('osaved')) / num_valid('ogames')
        matches_pyBreak['Total_games'] = (num_valid('games').astype(int) - num_valid('chances').astype(int) + num_valid('saved').fillna(0).astype(int) + num_valid('ochances').astype(int) - num_valid('osaved').astype(int)).astype(
            str) + '/' + (num_valid('ogames').astype(int) + num_valid('games').astype(int)).astype(str)
        matches_pyBreak['Total_games_ratio'] = (num_valid('games') - num_valid('chances') + num_valid('saved') + num_valid('ochances') - num_valid('osaved')) / (num_valid('ogames') + num_valid('games'))

        # matches_pyBreak['Score string'] = matches_pyBreak['Score'].apply(', '.join)
        # utworzenie list z danymi dot. tiebreaków rozegranych i wygranych w meczu, utworzenie kolumny do tabeli
        tiebreak_search = list(matches_pyBreak['Score_list'])
        tiebreak_won = []
        tiebreak_played = []

        for tb in tiebreak_search:
            tb_win = str(tb).count('7-6')
            tb_lose = str(tb).count('6-7')
            tb_sum = tb_win + tb_lose
            tiebreak_won.append(tb_win)
            tiebreak_played.append(tb_sum)

        tiebreak_won = pd.Series(tiebreak_won)
        tiebreak_played = pd.Series(tiebreak_played)
        # matches_pyBreak['Tiebreaks won/played'] = tiebreak_won.astype(str)+'/'+tiebreak_played.astype(str)

        # # lista z liczbą setów w każdym meczu potrzebna do wyliczenia % tiebreaków na rozegrane sety zawodnika
        # # z warunkiem brzegowym dotyczącym walkowerów
        # sets = pd.Series(sets)
        matches_pyBreak.replace(r'\sCH', '', inplace=True, regex=True)
        matches_pyBreak.replace(r'ATP\s', '', inplace=True, regex=True)
        matches_pyBreak.replace(r'\sMasters', '', inplace=True, regex=True)
        matches_pyBreak.loc[(matches_pyBreak['Tournament'] == 'Indian Wells') & (matches_pyBreak['Tournament_level'] == 'Challengers'), 'Tournament'] = 'Indian Wells CH'

        # zamiana kolejności linii i wyrzucenie listy z wynikami z pozostawieniem ich w postaci string
        matches_pyBreak['PyID'] = imie
        del matches_pyBreak['Score_list']
        matches_pyBreak = matches_pyBreak[[list(matches_pyBreak.columns)[-1]] + list(matches_pyBreak.columns)[:-1]]
        matches_pyBreak['Sets'] = sets
        matches_pyBreak['Sets'] = np.where(matches_pyBreak['Score'].str.contains("RET"),matches_pyBreak['Sets']-1,matches_pyBreak['Sets'])
        matches_pyBreak['Tiebreak_played'] = tiebreak_played
        matches_pyBreak['Tiebreak_won'] = tiebreak_won

        # zmiana linijek stringowych w wypadku meczów nieodbytych - walkowerów, lub to be played
        empties = ['Aces','Double_faults','Breakpoints_saved','Breakpoints_converted','Service_games_won','Return_games_won','Total_games','Tiebreak_played','Tiebreak_won','Sets']
        for e in empties:
            matches_pyBreak.loc[(matches_pyBreak['Result'] == 'To be played') | (matches_pyBreak['Score'] == 'W/O') | (
                        matches_pyBreak['Score'] == 'O/W'), '%s' % e] = ''

        slams = ['Wimbledon', 'Roland Garros', 'French Open', 'US Open', 'Australian Open']
        indians = ['Indian Wells', 'Indian Wells Masters', 'Miami', 'Miami Masters']
        quals = ['Q1','Q2','Q3']
        atpcup = ['Atp Cup', 'ATP Cup']

        matches_pyBreak['Startdate'] = matches_pyBreak['Date'] - datetime.timedelta(days=3)
        matches_pyBreak['Startdate'] = np.where(
            matches_pyBreak['Tournament'].isin(slams) & matches_pyBreak['Round'].isin(quals),
            matches_pyBreak['Date'] - datetime.timedelta(days=7), matches_pyBreak['Startdate'])
        matches_pyBreak['Startdate'] = np.where(
            matches_pyBreak['Tournament'].isin(slams) & (~matches_pyBreak['Round'].isin(quals)),
            matches_pyBreak['Date'] - datetime.timedelta(days=1), matches_pyBreak['Startdate'])
        matches_pyBreak['Startdate'] = np.where(matches_pyBreak['Tournament'].isin(indians), matches_pyBreak['Date'], matches_pyBreak['Startdate'])
        matches_pyBreak['Startdate'] = np.where(matches_pyBreak['Tournament'].isin(atpcup),
                                                matches_pyBreak['Date'] - datetime.timedelta(days=5), matches_pyBreak['Startdate'])
        matches_pyBreak['Startdate'] = np.where((~matches_pyBreak['Tournament'].isin(slams)) &
                (~matches_pyBreak['Tournament'].isin(indians)) &
                (matches_pyBreak['Round'].isin(quals)) &
               (matches_pyBreak['Date'] > pd.Timestamp('29/12/2019')), matches_pyBreak['Date'] - datetime.timedelta(days=4), matches_pyBreak['Startdate'])


        slamdate = matches_pyBreak['Date'] + datetime.timedelta(days=14)
        matches_pyBreak['Finaldate'] = matches_pyBreak['Date'] + datetime.timedelta(days=7)

        matches_pyBreak['Finaldate'] = np.where(matches_pyBreak['Tournament'].isin(slams) & matches_pyBreak['Round'].isin(quals), matches_pyBreak['Date'], matches_pyBreak['Finaldate'])
        matches_pyBreak['Finaldate'] = np.where(matches_pyBreak['Tournament'].isin(slams) & (~matches_pyBreak['Round'].isin(quals)), slamdate, matches_pyBreak['Finaldate'])
        matches_pyBreak['Finaldate'] = np.where(matches_pyBreak['Tournament'].isin(indians), slamdate, matches_pyBreak['Finaldate'])


        # zapis przykładowej autorskiej tabeli matches do pliku csv, zamknięcie drivera w celu czyszczenia procesu
        matches_pyBreak = matches_pyBreak[(matches_pyBreak.Score != 'W/O') & (matches_pyBreak.Score != 'O/W') & (matches_pyBreak.Result != 'To be played')]
        matches_pyBreak.to_csv('%s_abstract.csv' % imie, float_format='%.2f')

        data_dict[imie].append(matches_pyBreak)
        print(matches_pyBreak.dtypes)
