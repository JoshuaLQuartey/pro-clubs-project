import requests 
from bs4 import BeautifulSoup

players_url =  "https://proclubshead.com/24/club-squad/gen5-179156/" 
data = requests.get(players_url) 

soup = BeautifulSoup(data.text) 

squad_list_div = soup.select('div.bg-gradient')[0] 
player_links = squad_list_div.find_all('a') 
player_hrefs = (link.get("href") for link in player_links) 
player_slugs = [links for links in player_hrefs if '/club-player/']
player_urls = [f"https://proclubshead.com/{slug}" for slug in player_slugs]  

data = requests.get(player_urls[0])
soup = BeautifulSoup(data.text, 'html.parser')
current_table = soup.select('div.flex-nowrap')[1] 
table_soup = BeautifulSoup(str(current_table), 'html.parser')