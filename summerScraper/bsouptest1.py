import requests
from bs4 import BeautifulSoup

source = requests.get('https://www.fftoday.com/rankings/playerproj.php?PosID=20').text

soup = BeautifulSoup(source,'lxml')

# print(soup.prettify())

table = soup.find('div', class_ = 'pills-wrap feature-secondary')
print(table)

player1 = soup.find('tr', class_ = 'player-row')
# print(player1)
