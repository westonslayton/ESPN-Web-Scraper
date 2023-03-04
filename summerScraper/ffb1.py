import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import operator

league_id = 8432293
year = 2020
url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
      str(league_id) + "?seasonId=" + str(year)



r = requests.get(url)
d = r.json()[0]

#print(d)


r = requests.get(url, params={"view": "mMatchup"})
d = r.json()[0]

#that's the json code from this url: https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/8432293?seasonId=2020&view=mMatchup





df = [[
        game['matchupPeriodId'],
        game['home']['teamId'], game['home']['totalPoints'],
        game['away']['teamId'], game['away']['totalPoints']
    ] for game in d['schedule']]
df = pd.DataFrame(df, columns=['Week', 'Team1', 'Score1', 'Team2', 'Score2'])
#the pandas DataFrame method organizes the data into a table
df['Type'] = ['Regular' if w<=12 else 'Playoff' for w in df['Week']]
#print(df.head(20))
#the pandas head method gives the number of rows you want to view




df3 = df.assign(Margin1 = df['Score1'] - df['Score2'],
                Margin2 = df['Score2'] - df['Score1'])
df3 = (df3[['Week', 'Team1', 'Margin1', 'Type']]
 .rename(columns={'Team1': 'Team', 'Margin1': 'Margin'})
 .append(df3[['Week', 'Team2', 'Margin2', 'Type']]
 .rename(columns={'Team2': 'Team', 'Margin2': 'Margin'}))
)
# Look into the assign, rename, append methods and what they're doing here
#print(df3.head(20))




fig, ax = plt.subplots(1,1, figsize=(16,6))
#organized by order of standings (found team ids in urls)
final_standings = [4, 1, 3, 9, 6, 2, 8, 5, 7, 10]
order = final_standings
sns.boxplot(x='Team', y='Margin', hue='Type',
            data=df3,
            palette='muted',
            order=order)
ax.axhline(0, ls='--')
ax.set_xlabel('')
ax.set_title('Win/Loss margins')
#plt.show()






# get average score per week
avgs = (df
 .filter(['Week', 'Score1', 'Score2'])
 .melt(id_vars=['Week'], value_name='Score')
 .groupby('Week')
 .mean()
 .reset_index()
)
#Look over these methods/what library they're from
#print(avgs.head(20))
#This code generates the average score for each week





tm = 1

# grab all games with this team
df2 = df.query('Team1 == @tm | Team2 == @tm').reset_index(drop=True)

# move the team of interest to "Team1" column
ix = list(df2['Team2'] == tm)
df2.loc[ix, ['Team1','Score1','Team2','Score2']] = \
    df2.loc[ix, ['Team2','Score2','Team1','Score1']].values

# add new score and win cols
df2 = (df2
 .assign(Chg1 = df2['Score1'] - avgs['Score'],
        # Chg2 = df2['Score2'] - avgs['Score'],
        #This column I don't love
         Win  = df2['Score1'] > df2['Score2'])
)

eval_list = []
for w1, w2 in zip(df2['Chg1'], df2['Win']):
    if w1 < 0 and w2 == True:
        eval_list.append('Lucky Win')
    elif w1 > 0 and w2 == False:
        eval_list.append('Unlucky Loss')
    else:
        eval_list.append('Normal')

df2 = df2.assign(Eval = eval_list)
print(df2)

"""Most importantly shows whether someone won compared to how
 they did relative to the average score that week
 If they won and got under, it's a 'lucky win'
If they lost and got over, it's an  'unlucky loss'

Want to use this eval column to find every players'
luckiness rating. Lucky win adds 1, unlucky subtracts 1,
normal remains the same.
Then make a rankings of every team from most lucky to
least.
Then compare this to the final standings of the league
and will show how much of fantasy is luck
"""

league_luck = dict()
for tm in range (1,11):

# grab all games with this team
    df2 = df.query('Team1 == @tm | Team2 == @tm').reset_index(drop=True)

    # move the team of interest to "Team1" column
    ix = list(df2['Team2'] == tm)
    df2.loc[ix, ['Team1','Score1','Team2','Score2']] = \
        df2.loc[ix, ['Team2','Score2','Team1','Score1']].values

    # add new score and win cols
    df2 = (df2
     .assign(Chg1 = df2['Score1'] - avgs['Score'],
            # Chg2 = df2['Score2'] - avgs['Score'],
            #This column I don't love
             Win  = df2['Score1'] > df2['Score2'])
    )

    eval_list = []
    for w1, w2 in zip(df2['Chg1'], df2['Win']):
        if w1 < 0 and w2 == True:
            eval_list.append('Lucky Win')
        elif w1 > 0 and w2 == False:
            eval_list.append('Unlucky Loss')
        else:
            eval_list.append('Normal')

    df2 = df2.assign(Eval = eval_list)

    luck_count = 0

    for week in eval_list:
        if week == 'Lucky Win':
            luck_count += 1
        elif week == 'Unlucky Loss':
            luck_count -= 1
        else:
            luck_count += 0

    league_luck[tm] = luck_count


league_luck = sorted(league_luck.items(), key=operator.itemgetter(1), reverse=True)
for x in league_luck:
    print(x)
print(final_standings)


"""
 league_luck along with final_standings shows
 the standings of luckiness with regards to scheduling
 compared to the actual final standings
 Want to put this in a table to visualize the 2 better
 Also want to eliminate last 2 weeks (playoffs)

 This data basically confirms that scheudling luck plays
 a huge part in final standings. There are a couple outliers
 like Jack and Jonah but the rest pretty much alligns.
 Outliers probably mean they either had unlucky injury problems
 or just had poorly managed teams (think it's injury).
 If it is injuries then I came to the conclusion that, whether
 it be scheduling or injuries (the 2 main things you don't
 have any control over/can't predict), it is luck and not how
 well you manage your team that plays the main factor in fantasy
 football.
"""
