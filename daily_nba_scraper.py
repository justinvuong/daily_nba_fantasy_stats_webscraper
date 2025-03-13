from bs4 import BeautifulSoup
import requests
import pandas as pd

# get URL
page = requests.get("https://www.basketball-reference.com/friv/dailyleaders.fcgi")
soup = BeautifulSoup(page.content, 'html.parser')

#list of columns not needed
omit_columns = ['team_id', 'game_location', 'opp_id', 'game_result', 'mp', 'game_score']
omit_headers = ['Rk',' ', 'Tm', 'Opp', 'MP', 'GmSc']

#table of players and stats
table = soup.find('table', id='stats')
thead = table.find('thead')
tbody = table.find('tbody')
trs = tbody.find_all('tr')

# \xa0 is unicode for &nbsp;
headers = [header.get_text(strip=True).replace('\xa0', '') for header in thead.find_all('th')]
headers = [header for header in headers if header != '']
filtered_headers = [header for header in headers if header not in omit_headers]

print(filtered_headers)

data = []

for tr in trs:
    columns = tr.find_all('td')
    column_data = [
        col.get_text(strip=True)
        for col in columns if col.get('data-stat') not in omit_columns
    ]

    if column_data:
        data.append(column_data)

df = pd.DataFrame(data, columns=filtered_headers)
df.to_excel('daily_basketball_fantasy_stats.xlsx', index=False, engine='openpyxl')

print('saved to excel')