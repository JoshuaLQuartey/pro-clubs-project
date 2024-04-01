import requests 
from bs4 import BeautifulSoup

players_url =  "https://proclubshead.com/24/club-squad/gen5-179156/" 
data = requests.get(players_url) 

soup = BeautifulSoup(data.text) 
members = soup.select('div.bg-gradient')[0] 
links = members.find_all('a') 
links = (l.get("href") for l in links) 
links = [l for l in links if '/club-player/']
player_url = [f"https://proclubshead.com/{l}" for l in links]  

data = requests.get(player_url[0])
soup = BeautifulSoup(data.text, 'html.parser')
current_table = soup.select('div.flex-nowrap')[1] 
table_soup = BeautifulSoup(str(current_table), 'html.parser')
