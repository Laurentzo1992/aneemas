# Code by niklacode
import requests
from bs4 import BeautifulSoup
#import os
import pandas as pd
import numpy as np


"""    
def get_data_by_url():
    
    url = "https://www.veracash.com/fr/cours-or"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        table = soup.find_all('table')[0]
        rows = table.find_all('tr')
    except:
        print("pas de données trouvé")

    data = []  # Utiliser une liste pour stocker les données sous forme de dictionnaires

    # Récupérer les noms de colonnes (première ligne du tableau)
    header_row = rows[0]
    header_columns = header_row.find_all('th')
    column_names = [column.get_text().strip() for column in header_columns]
    # Renommer '1_once_(31,1_grammes)' en '1_onces'
    column_names = [name.replace('1 gramme', 'gramme').replace('1 once (31,grammes)', 'once').replace('1 kilogramme', 'kilogramme').replace('Variation 24H', 'variation') for name in column_names]



    for row in rows[1:]:
        columns = row.find_all('td')
        values = [column.get_text() for column in columns]
        data.append(dict(zip(column_names, values)))

    return data
"""






def get_data_by_url():
    
    url = "https://or.fr/cours/or#live-chart"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')

    data = []  # Utiliser une liste pour stocker les données sous forme de dictionnaires

    # Récupérer les noms de colonnes (première ligne du tableau)
    header_row = rows[0]
    header_columns = header_row.find_all('th')
    column_names = [column.get_text().strip() for column in header_columns]
    # Renommer '1_once_(31,1_grammes)' en '1_onces'
    column_names = [name.replace('1 gramme', 'gramme').replace('1 once (31,10 grammes)', 'once').replace('1 kilogramme', 'kilogramme').replace('Variation 24H', 'variation') for name in column_names]

    for row in rows[1:5]:
        columns = row.find_all('td')
        values = [column.get_text() for column in columns]
        data.append(dict(zip(column_names, values)))

    return data








