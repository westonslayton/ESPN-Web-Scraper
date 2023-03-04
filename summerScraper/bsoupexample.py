import requests
from bs4 import BeautifulSoup

source = requests.get('https://coreyms.com').text

soup = BeautifulSoup(source,'lxml')

# print(soup.prettify())

article = soup.find('article')

headline = article.h2
print(headline)
