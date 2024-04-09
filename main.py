import requests 
from bs4 import BeautifulSoup
import pandas as pd

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

#Creating my own table 
data = []
for category in table_soup.find_all('div', class_='col-auto'): #create my own table
    category_title = category.find('h3')
    if category_title:
        # category_name = category_title.text  # Extract category name
        for stat_div in category.find_all('div', class_='border-bottom'):
            stat_name = stat_div.find_all('div', class_='col')  # Extract stat name
            stat_value = stat_div.find_all('div', class_='col-auto')  # Extract stat value
            data.append({'stat_name': stat_name, 'stat_value': stat_value})
df = pd.DataFrame(data)
print (df)