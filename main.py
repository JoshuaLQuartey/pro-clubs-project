import requests 
from bs4 import BeautifulSoup
import pandas as pd
import json

squad_url =  "https://proclubshead.com/24/club-squad/gen5-179156/" 
data = requests.get(squad_url) 

soup = BeautifulSoup(data.text) 

squad_list_div = soup.select('div.bg-gradient')[0] 
player_links = squad_list_div.find_all('a') 
player_hrefs = (link.get("href") for link in player_links) 
player_slugs = [links for links in player_hrefs if '/club-player/']
player_urls = [f"https://proclubshead.com/{slug}" for slug in player_slugs]  

all_data = []
for player_url in player_urls:
    data = requests.get(player_url)
    soup = BeautifulSoup(data.text, 'html.parser')
    current_table = soup.select('div.flex-nowrap')  
    table_soup = BeautifulSoup(str(current_table), 'html.parser')

    player_name = player_url.split("/")[-2].replace("gen5-179156-", "") 

    data = []
    for category in table_soup.find_all('div', class_='col-auto'): 
        category_title = category.find('h3')
        if category_title:
            for stat_div in category.find_all('div', class_='border-bottom'):
                stat_name = stat_div.find_all('div', class_='col') 
                stat_value = stat_div.find_all('div', class_='col-auto')  
                data.append({'player_name': player_name, 'stat_name': stat_name, 'stat_value': stat_value})
    all_data.extend(data)

df = pd.DataFrame(all_data)

df_exploded = df.apply(pd.Series.explode) 
df_exploded.reset_index(drop=True, inplace=True)
print(df_exploded)

records = df_exploded.to_dict(orient='records')

supabase_url = 'https://wqdoemgzcvnhviizniim.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxZG9lbWd6Y3ZuaHZpaXpuaWltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE1NDM5MzAsImV4cCI6MjAyNzExOTkzMH0.-40hkzpWnjWp3baLZ28XoonI6Yvk4vM3QGTe_HOwjYs'
table_name = 'playerstats'

for record in records:
    record['stat_name'] = record['stat_name'].text
    record['stat_value'] = record['stat_value'].text
    
headers = {
    'Content-Type': 'application/json',
    'apikey': supabase_key,
}

insert_url = f"{supabase_url}/rest/v1/{table_name}"
response = requests.post(insert_url, headers=headers, data=json.dumps(records))

print(response.text)

if response.status_code == 201:
    print("Records inserted successfully into Supabase table!")
else:
    print(f"Failed to insert records. Status code: {response.status_code}, Response: {response.text}")