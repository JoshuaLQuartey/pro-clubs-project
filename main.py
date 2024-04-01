import requests 

players_url =  "https://proclubshead.com/24/club-squad/gen5-179156/" #url of the page with all squad members link
data = requests.get(players_url) 