import sqlite3
import pandas as pd
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

base = '''
SELECT pyBreak_datapybreak.PyID AS id ,
pyBreak_rankingpybreak.Name as Name,
pyBreak_rankingpybreak.Rank as Rank,
SUM(pyBreak_datapybreak.Result = 'Win') as Matches_won ,SUM(pyBreak_datapybreak.Result = 'Lose') as Matches_lost ,
(SUM(pyBreak_datapybreak.Result='Lose')+SUM(pyBreak_datapybreak.Result='Win')) as Matches_played ,
AVG(Rival_rank) as Rival_rank ,
(SUM(pyBreak_datapybreak.Result = 'Win')*1.0 / (SUM(pyBreak_datapybreak.Result='Lose')+SUM(pyBreak_datapybreak.Result='Win')))*100 as Matches_won_perc, 
(SUM(pyBreak_datapybreak.Aces)*1.0 /SUM(pyBreak_datapybreak.Sets)) as Aces_AVG ,
(SUM(pyBreak_datapybreak.Double_faults)*1.0 /SUM(pyBreak_datapybreak.Sets)) as DoubleFaults_AVG ,
AVG(pyBreak_datapybreak.First_serve_accuracy)*100 First_serve_accuracy, 
AVG(pyBreak_datapybreak.First_serve_points)*100 as First_serve_points ,AVG(pyBreak_datapybreak.Second_serve_points)*100 'Second_serve_points', 
AVG(pyBreak_datapybreak.Total_serve_points_won)*100 'Total_serve_points_won', 
(SUM(pyBreak_datapybreak.Breakpoints_todefend)*1.0 / SUM(pyBreak_datapybreak.Sets)) as Breakpoints_to_defend_per_set ,
AVG(pyBreak_datapybreak.Breakpoints_saved_ratio)*100 'Breakpoints_saved_ratio', AVG(pyBreak_datapybreak.Return_1st_serve_points)*100 'Return_1st_serve_points' ,
AVG(pyBreak_datapybreak.Return_2nd_serve_points)*100 'Return_2nd_serve_points', AVG(pyBreak_datapybreak.Total_return_points)*100 'Total_return_points' ,
(SUM(pyBreak_datapybreak.Breakpoints_created)*1.0 / SUM(pyBreak_datapybreak.Sets)) as Breakpoints_created_per_set, 
AVG(pyBreak_datapybreak.Breakpoints_converted_ratio)*100 'Breakpoints_converted_ratio', AVG(pyBreak_datapybreak.Total_points)*100 'Total_points' ,
AVG(pyBreak_datapybreak.Service_games_won_ratio)*100 'Service_games_won_ratio', AVG(pyBreak_datapybreak.Return_games_won_ratio)*100 'Return_games_won_ratio' ,
AVG(pyBreak_datapybreak.Total_games_ratio)*100 'Total_games_ratio', SUM(pyBreak_datapybreak.sets) as 'Sets_played', 
SUM(pyBreak_datapybreak.Tiebreak_played) as 'Tiebreak_played', SUM(pyBreak_datapybreak.Tiebreak_won) as 'Tiebreak_won' ,
(SUM(pyBreak_datapybreak.Tiebreak_played)*1.0 / SUM(pyBreak_datapybreak.Sets))*100 as Sets_ended_by_tiebreak, 
(SUM(pyBreak_datapybreak.Tiebreak_won)*1.0 / SUM(pyBreak_datapybreak.Tiebreak_played))*100 as Tiebreak_won_perc ,
SUM(pyBreak_datapybreak.Result='Lose' and pyBreak_datapybreak.Player_odd <= 1.20)+SUM(pyBreak_datapybreak.Result='Win' and pyBreak_datapybreak.Player_odd <= 1.20) as Surety_played ,
SUM(pyBreak_datapybreak.Result = 'Win' and pyBreak_datapybreak.Player_odd <= 1.20) as Surety_won ,
SUM(pyBreak_datapybreak.Result='Lose' and pyBreak_datapybreak.Player_odd between 1.20 and 1.50 )+SUM(pyBreak_datapybreak.Result='Win' and pyBreak_datapybreak.Player_odd between 1.20 and 1.50) as Favorite_played ,
SUM(pyBreak_datapybreak.Result = 'Win' and pyBreak_datapybreak.Player_odd between 1.20 and 1.50) as Favorite_won ,
SUM(pyBreak_datapybreak.Result='Lose' and pyBreak_datapybreak.Player_odd between 1.50 and 1.80)+SUM(pyBreak_datapybreak.Result='Win' and pyBreak_datapybreak.Player_odd between 1.50 and 1.80) as Slightfav_played ,
SUM(pyBreak_datapybreak.Result = 'Win' and pyBreak_datapybreak.Player_odd between 1.50 and 1.80) as Slightfav_won ,
SUM(pyBreak_datapybreak.Result='Lose' and pyBreak_datapybreak.Rival_odd <= 1.20)+SUM(pyBreak_datapybreak.Result='Win' and pyBreak_datapybreak.Rival_odd <= 1.20) as Underdog_played ,
SUM(pyBreak_datapybreak.Result = 'Win' and pyBreak_datapybreak.Rival_odd <= 1.20) as Underdog_won ,
SUM(pyBreak_datapybreak.Result='Lose' and pyBreak_datapybreak.Rival_odd between 1.20 and 1.50)+SUM(pyBreak_datapybreak.Result='Win' and pyBreak_datapybreak.Rival_odd between 1.20 and 1.50) as Under_played ,
SUM(pyBreak_datapybreak.Result = 'Win' and pyBreak_datapybreak.Rival_odd between 1.20 and 1.50) as Under_won ,
SUM(pyBreak_datapybreak.Result='Lose' and pyBreak_datapybreak.Rival_odd between 1.50 and 1.80)+SUM(pyBreak_datapybreak.Result='Win' and pyBreak_datapybreak.Rival_odd between 1.50 and 1.80) as Slightunder_played ,
SUM(pyBreak_datapybreak.Result = 'Win' and pyBreak_datapybreak.Rival_odd between 1.50 and 1.80) as Slightunder_won 

FROM pyBreak_datapybreak ,pyBreak_rankingpybreak
WHERE pyBreak_datapybreak.PyID = pyBreak_rankingpybreak.PyID
AND pyBreak_datapybreak.score != 'W/O' 
AND pyBreak_datapybreak.score != 'O/W' 
AND pyBreak_datapybreak.result != 'To be played' 
AND pyBreak_datapybreak.Total_games NOT LIKE '%/0'
'''

cur.execute('DROP VIEW IF EXISTS players_summary')
cur.execute('DROP VIEW IF EXISTS players_ovr_2020')
cur.execute('DROP VIEW IF EXISTS players_ovr_current')
cur.execute('DROP VIEW IF EXISTS players_clay')
cur.execute('DROP VIEW IF EXISTS players_clay_2020')
cur.execute('DROP VIEW IF EXISTS players_clay_current')
cur.execute('DROP VIEW IF EXISTS players_hard')
cur.execute('DROP VIEW IF EXISTS players_hard_2020')
cur.execute('DROP VIEW IF EXISTS players_hard_current')

players_summary = cur.execute('CREATE VIEW players_summary AS %s GROUP BY pyBreak_datapybreak.PyID ORDER BY pyBreak_rankingpybreak.Rank' % base)
players_ovr_2020 = cur.execute('CREATE VIEW players_ovr_2020 AS %s AND "Date" > Datetime("2020-01-01") GROUP BY pyBreak_datapybreak.PyID ORDER BY pyBreak_rankingpybreak.Rank' % base)
players_ovr_current = cur.execute('CREATE VIEW players_ovr_current AS %s AND "Date" > Datetime("2020-08-01") GROUP BY pyBreak_datapybreak.PyID ORDER BY pyBreak_rankingpybreak.Rank' % base)
players_clay = cur.execute('CREATE VIEW players_clay AS %s AND pyBreak_datapybreak.Surface == "Clay" GROUP BY pyBreak_datapybreak.PyID ORDER BY pyBreak_rankingpybreak.Rank' % base)
players_clay_2020 = cur.execute('CREATE VIEW players_clay_2020 AS %s AND pyBreak_datapybreak.Surface == "Clay" AND "Date" > Datetime("2020-01-01") GROUP BY pyBreak_datapybreak.PyID ORDER BY pyBreak_rankingpybreak.Rank' % base)
players_clay_current = cur.execute('CREATE VIEW players_clay_current AS %s AND pyBreak_datapybreak.Surface == "Clay" AND "Date" > Datetime("2020-08-01") GROUP BY pyBreak_datapybreak.PyID ORDER BY pyBreak_rankingpybreak.Rank' % base)
players_hard = cur.execute('CREATE VIEW players_hard AS %s AND pyBreak_datapybreak.Surface == "Hard" GROUP BY pyBreak_datapybreak.PyID ORDER BY pyBreak_rankingpybreak.Rank' % base)
players_hard_2020 = cur.execute('CREATE VIEW players_hard_2020 AS %s AND pyBreak_datapybreak.Surface == "Hard" AND "Date" > Datetime("2020-01-01") GROUP BY pyBreak_datapybreak.PyID ORDER BY pyBreak_rankingpybreak.Rank' % base)
players_hard_current = cur.execute('CREATE VIEW players_hard_current AS %s AND pyBreak_datapybreak.Surface == "Hard" AND "Date" > Datetime("2020-08-01") GROUP BY pyBreak_datapybreak.PyID ORDER BY pyBreak_rankingpybreak.Rank' % base)


conn.commit()
conn.close()




