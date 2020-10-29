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
import lxml.html as lh
import fuzzywuzzy
from lxml import etree
import html

try:
    options = Options()
    options.add_argument("--kiosk")
    options.add_argument("--headless")
    chromedriver = "/home/bigmac/Downloads/chromedriver"
    driver = webdriver.Chrome(chromedriver, options=options)
except WebDriverException as e:
    print("Zainstaluj przeglądarkę Google Chrome oraz odpowiednią"
          " dla niej wersję chromedriver"
          "\n%s" % e)
    sys.exit()


def tennisexp_parse(top200, ranking_pyBreak, data_dict):
    mans = top200.shape[0]

    if mans % 50 == 0:
        pages = int(mans//50)
    else:
        pages = int(mans//50 + 1)

    startlink = 'https://www.tennisexplorer.com'
    startlist = startlink + '/ranking/atp-men/?page='
    # rank_pages = []
    playerlinks = {}
    playernames = dict(zip(ranking_pyBreak['Rank'], ranking_pyBreak['PyID']))
    count = 0
    rankvalue = 0

    fullnames = [fullname.lower() for fullname in ranking_pyBreak['Player'].tolist()]
    stranges = {'Ramos-Vinolas A.': 'Ramos A.'}
    print(fullnames)

    for n in range(1, pages+1):
        driver.get(str(startlist)+str(n))
        bs_obj = BeautifulSoup(driver.page_source, 'html.parser').find('tbody', {'class': 'flags'})
        players = bs_obj.find_all('td', {'class': 't-name'})
        for p in players:
            rankvalue += 1
            playerlink = startlink + str(p.find('a').get('href'))
            playerlinks.update({playerlink: rankvalue})
            # playernames.append(ranking_pyBreak.loc[ranking_pyBreak['Rank'] == count, 'PyID'].iloc[0])

    print(playerlinks)
    print(playernames)

    # tennisexplorer oddsy
    year = datetime.date.today().year
    prev = '?annual='
    years = [str(year),str(year-1)]

    matches = []
    headers = ['PyID', 'Date', 'Tournament', 'Round', 'Rival_org', 'Result', 'Player_odd', 'Rival_odd', 'Score']

    for k, v in playerlinks.items():
        if v <= mans:
            matches = []
            headers = ['PyID', 'Date', 'Tournament', 'Round', 'Rival_org', 'Result', 'Player_odd', 'Rival_odd', 'Score']
            count += 1
            print(k, v)
            framename = playernames[count]

            for y in years:
                driver.get(str(k) + str(prev) + str(y))
                print(str(k) + str(prev) + str(y))
                bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
                try:
                    code = bs_obj.find('div', {'id': re.findall(r'matches-\d{4}-1-data', str(bs_obj))}).find('tbody')
                    table = code.find_all('tr', {'class': ['head flags', 'one', 'two']})
                    mecze = code.find_all('tr', {'class': ['one', 'two']})
                    surname = framename

                    for t in table:
                        if t in mecze:
                            next_year = ['%s.12.' % i for i in range(24, 32)]
                            date_var = t.find("td", "first time").text
                            if date_var not in next_year:
                                data = (date_var) + str(y)
                            else:
                                data = (date_var) + str(int(y) - 1)
                            names = (t.find("td", "t-name").text).split(' - ')
                            runda = t.find("td", "round").text
                            score = t.find("td", "tl").text
                            score = score.split(', ')
                            score_translated = []

                            for s in score:
                                tbw = re.match(r'7-6\d*', s)
                                tbl = re.match(r'6\d*-7', s)
                                tbwexh = re.match(r'4-3\d*', s)
                                tblexh = re.match(r'3\d*-4', s)
                                if tbl:
                                    if len(s) == 4:
                                        score_translated.append('6-7' + '(' + s[1] + ')')
                                    else:
                                        score_translated.append('6-7' + '(' + s[1] + s[2] + ')')
                                elif tbw:
                                    if len(s) == 4:
                                        score_translated.append('7-6' + '(' + s[-1] + ')')
                                    else:
                                        score_translated.append(('7-6' + '(' + s[-2] + s[-1] + ')'))
                                elif tbwexh:
                                    if len(s) == 4:
                                        score_translated.append('4-3' + '(' + s[-1] + ')')
                                    else:
                                        score_translated.append(('4-3' + '(' + s[-2] + s[-1] + ')'))
                                elif tblexh:
                                    if len(s) == 4:
                                        score_translated.append('3-4' + '(' + s[-1] + ')')
                                    else:
                                        score_translated.append(('3-4' + '(' + s[-2] + s[-1] + ')'))
                                else:
                                    score_translated.append(s)
                            score = ', '.join(score_translated)

                            turniej = t.find_previous_sibling('tr', {'class': ['head flags']}).find("td").text.replace(u'\xa0', u'')
                            course = [element.text for element in t.find_all("td", "course")]
                            rival = str([element.find("a", "").text for element in t.find_all("td", "t-name")][0])
                            if rival == names[0]:
                                result = 'Lose'
                                rivalodd, playerodd = course[0], course[1]
                            else:
                                result = "Win"
                                playerodd, rivalodd = course[0], course[1]
                            string = surname, data, turniej, runda, rival, result, playerodd, rivalodd, score
                            matches.append(string)

                except AttributeError:
                    print('{} has played no matches in {} year.'.format(k, y))

        odds_pyBreak = pd.DataFrame(data=matches, columns=headers)

        length = (odds_pyBreak.shape[0])
        scores_win = []
        scores_reversed = []
        scores = list(odds_pyBreak['Score'])[:length]
        sets = []

        for line in scores:
            spaces = r"\s+"
            line = re.split(spaces, line)
            scores_win.append(line)
            sets.append(len(line))

        def reversescore(s):
            if len(s) > 3:
                s1 = ''.join(reversed(s[:3])) + s[3:]
                return s1
            else:
                if s == 'RET':
                    return s
                else:
                    s = ''.join(reversed(s[:3]))
                    return s

        for score in scores_win:
            scores_reversed.append(list((reversescore(s) for s in score)))

        odds_pyBreak['Date'] = pd.to_datetime(odds_pyBreak['Date'], dayfirst=True)
        odds_pyBreak['score_list'] = np.where(odds_pyBreak['Result'] == 'Win', scores_win, scores_reversed)
        odds_pyBreak['Score'] = odds_pyBreak['score_list'].apply(' '.join)
        del (odds_pyBreak['score_list'])
        odds_pyBreak.to_csv('%s_odds.csv' % odds_pyBreak['PyID'].iloc[0])
        data_dict[odds_pyBreak['PyID'].iloc[0]].append(odds_pyBreak)
        print(surname)

# flashscore tabela

# def open_driver():
#     try:
#         options = Options()
#         options.add_argument("--kiosk")
#         options.add_argument("--headless")
#         chromedriver = "/home/bigmac/Downloads/chromedriver"
#         driver = webdriver.Chrome(chromedriver, options=options)
#     except WebDriverException as e:
#         print("Zainstaluj przeglądarkę Google Chrome oraz odpowiednią"
#             " dla niej wersję chromedriver"
#             "\n%s" % e)
#         sys.exit()
#
# driver.get("https://www.flashscore.com/player/paire-benoit/CMfsaHsr/results/")
# bs_cookies = driver.find_element_by_css_selector('#cookie-law > div.cookie-law-exit > div').click()
# bs_more = driver.find_element_by_css_selector('#participant-page-results_s-more > tbody > tr > td > a')
# bs_more.click()
# time.sleep(1)
# bs_more.click()
#
# time.sleep(1)
# bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
#
# loaded = []
# matches_links = []
# headers = ['range','tour','date','player 1','player 2','final score(sets)']
# code = bs_obj.find('div', {'PyID': 'fs-results_s'})
# tour_table = code.find_all('table', {'class': 'tennis'})
#
# for tour in tour_table:
#     range = tour.find_all('span', {'class':'country_part'})
#     tour_name = tour.find_all('span', {'class':'tournament_part'})
#     mecze = tour.find_all('tr', {'class': ['even stage-finished', 'odd stage-finished']})
#     for m in mecze:
#         m.td.append(BeautifulSoup(str(range)[1:-1], 'html.parser'))
#         m.td.append(BeautifulSoup(str(tour_name)[1:-1], 'html.parser'))
#         ranga = m.find('span', {'class': 'country_part'}).text
#         turniej = m.find('span', {'class': 'tournament_part'}).text
#         czas = m.find('td', {'class': 'cell_ad time'}).text
#         zawodnicy = [element.text for element in m.find_all('span', {'class': 'padl'})]
#         wynik = m.find('td', {'class': 'cell_sa score bold'}).text
#         mecz_link = (re.findall('2_\S+"',str(m)))[0][2:-1]
#         matches_links.append(mecz_link)
#         line = ranga,turniej,czas,zawodnicy[0],zawodnicy[1],wynik
#         loaded.append(line)
#
# today = datetime.date.today()
# year = today.year
# flashscore_pyBreak = pd.DataFrame(data=loaded, columns=headers)
# tourn_split = flashscore_pyBreak['tour'].str.split(", ", n=1, expand=True)
# flashscore_pyBreak['tournament'] = tourn_split[0]
# flashscore_pyBreak['surf'] = tourn_split[1]
# flashscore_pyBreak.drop(columns=['tour'],inplace=True)
#
# flashscore_pyBreak.replace(r'\s\d{2}\:\d{2}', '%s'%year, inplace=True, regex=True)
# flashscore_pyBreak.replace(r'\s\([A-Z]{1}.+\)', '', inplace=True, regex=True)
#
# surf_split = flashscore_pyBreak['surf'].str.split(" ", n=1, expand=True)
# flashscore_pyBreak['surface'] = surf_split[0]
# flashscore_pyBreak['outdoor/indoor'] = surf_split[1]
# flashscore_pyBreak['outdoor/indoor'].fillna("outdoor",inplace=True)
# flashscore_pyBreak.replace('(indoor)', 'indoor', inplace=True)
# flashscore_pyBreak.drop(columns=['surf'],inplace=True)
#
# flashscore_pyBreak.replace(r'\s\-\sSINGLES\:', '', inplace=True, regex=True)
# flashscore_pyBreak.replace(r'\sMEN', '', inplace=True, regex=True)
#
# # if today.weekday() == 6:
# #     n = -1
# # elif today.weekday() == 5:
# #     n = -2
# # elif today.weekday() == 4:
# #     n = -3
# # elif today.weekday() == 3:
# #     n = -4
# # elif today.weekday() == 2:
# #     n = -5
# # elif today.weekday() == 1:
# #     n = -6
# # else:
# #     n = -7
#
# # oneyearago = today - timedelta(weeks=52,days=n)
# flashscore_pyBreak['date'] = pd.to_datetime(flashscore_pyBreak['date'],format='%d.%m.%Y')
# print(flashscore_pyBreak.dtypes)
# flashscore_pyBreak.to_csv('flashscore3.csv')
#
#
# # flashscore mecz scrape
#
# web = 'https://www.flashscore.com/match/'
# pbp = '/#point-by-point;1'
# player1 = []
# player2 = []
#
#
# for m in matches_links:
#     mecz = m
#     driver.get('%s%s%s'%(web,mecz,pbp))
#     bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
#     set1 = bs_obj.find('div',{'PyID':'tab-mhistory-1-history'})
#     set2 = bs_obj.find('div',{'PyID':'tab-mhistory-2-history'})
#     set3 = bs_obj.find('div',{'PyID':'tab-mhistory-3-history'})
#     set4 = bs_obj.find('div',{'PyID':'tab-mhistory-4-history'})
#     set5 = bs_obj.find('div',{'PyID':'tab-mhistory-5-history'})
#
#     sets = []
# #
# #
# #
#     for set in (set1,set2,set3,set4,set5):
#         if set:
#             sets.append(set)
#     for s in sets:
#         gem = s.find('table',{'class':'parts-first'}).find_all('tr',{'class':['odd fifteens_available','even fifteens_available']})
#
#         for g in gem:
#             p1break = g.find('td',{'class':'match-history-vertical fr lostserve'})
#             p2break = g.find('td',{'class':'match-history-vertical fl lostserve'})
#             p1served = g.find_all('td',{'class':'server'})[0].find('div',{'class':'icon-box'})
#             p2served = g.find_all('td',{'class':'server'})[1].find('div',{'class':'icon-box'})
#             if p1break:
#                 player1.append('lose')
#             elif p2break:
#                 player2.append('lose')
#             else:
#                 if p1served:
#                     player1.append('win')
#                 if p2served:
#                     player2.append('win')
#
#
# print(player1)
# print(player2)
#
# driver.quit()
