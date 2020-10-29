from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas as pd
import os
import requests
import json
import csv
import sys
import numpy as np
import sqlite3

from baseabstract import abstract_parse
from tennisexp import tennisexp_parse
from fuzzytest import fuzzyframes

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
ranking_pyBreak.to_csv('ranking_pyBreak.csv')

data_dict = {player: [] for player in top200IDs}

today = datetime.now()
dayname = datetime.strftime(today, '%Y')+ datetime.strftime(today, '%m') + datetime.strftime(today, '%d')

conn = sqlite3.connect('%s.db' % dayname)
cur = conn.cursor()

list_of_dataframes = []

abstract_parse(driver, top200IDs, data_dict)
tennisexp_parse(top200, ranking_pyBreak, data_dict)
fuzzyframes(data_dict, list_of_dataframes)

ranking_pyBreak.to_sql('ranking_pyBreak', con=conn, index=False, if_exists='replace')
data_pyBreak = pd.concat(list_of_dataframes)

data_pyBreak.to_sql('data_pyBreak', con=conn, index=False, if_exists='append')

driver.quit()




