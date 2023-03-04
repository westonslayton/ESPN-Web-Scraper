import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

league_id = 8432293
year = 2020
url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
      str(league_id) + "?seasonId=" + str(year)

r = requests.get(url, params={"view": "mRoster"})
d = r.json()[0]

#that's the json code from this url: https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/8432293?seasonId=2020&view=mRoster

"""my_team =[]
for player in d['teams'][0]['roster']['entries']:
    my_team.append(player['playerPoolEntry']['player']['fullName'])
print(my_team)

#This code gives the list of players on team[0] (my team)
"""



"""
leagueRoster = []
for team in d['teams']:
    teamRoster = []
    for player in team['roster']['entries']:
        teamRoster.append(player['playerPoolEntry']['player']['fullName'])
    leagueRoster.append(teamRoster)
#This creates a list called leagueRoster of each team's roster as separate lists

rosterTable = pd.DataFrame(leagueRoster)
#print(rosterTable)
#This code prints leagueRoster out as a table
"""


leagueRoster = dict()
for team in d['teams']:
    leagueRoster[team['id']] = [player['playerPoolEntry']['player']['fullName']
    for player in team['roster']['entries']]
#This creates a list called leagueRoster of each team's roster as separate lists
#print(leagueRoster)
for key in leagueRoster:
    if len(leagueRoster[key]) == 17:
        leagueRoster[key].pop(16)
    elif len(leagueRoster[key]) == 18:
        leagueRoster[key].pop(17)
        leagueRoster[key].pop(16)
    elif len(leagueRoster[key]) == 19:
        leagueRoster[key].pop(18)
        leagueRoster[key].pop(17)
        leagueRoster[key].pop(16)


pd.set_option("display.max_columns", None)
rosterTable = pd.DataFrame(leagueRoster)
print(rosterTable)
#Prints leagueRoster dict() out as a table
