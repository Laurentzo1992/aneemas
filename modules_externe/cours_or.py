# Code by niklacode
import requests
from bs4 import BeautifulSoup
#import os
import pandas as pd
import numpy as np
import requests
import json
from modules_externe.api_url import HEADER_TOKEN

def get_data_by_api(url):
    results = []
    kobo = requests.get(url, headers=HEADER_TOKEN)
    if kobo.status_code == 200:
        api_data = json.loads(kobo.content)
        data = api_data.get('results', [])
        for result in data:
            validation_status = result.get('_validation_status', {}).get('uid')
            if validation_status == 'validation_status_approved':
                result['id'] = result.pop('_id')
                result['submitted_by'] = result.pop('_submitted_by')
                result['nom'] = result.pop('labeled_select_group1/nom_personne')
                result['prenom'] = result.pop('labeled_select_group1/prenom_personne')
                result['type_carte'] = result.pop('labeled_select_group1/t_carte')
                result['date'] = result.pop('labeled_select_group1/date')
                result['localite'] = result.pop('labeled_select_group1/nom_localite')
                result['telephone'] = result.pop('labeled_select_group2/telephone1')
                result['telephone2'] = result.pop('labeled_select_group2/telephone2')
                result['quittance'] = result.pop('labeled_select_group2/quittance')
                result['engagement'] = result.pop('labeled_select_group2/engagement')
                result['num_carte'] = result.pop('labeled_select_group2/n_carte')
                result['observation'] = result.pop('labeled_select_group2/obs')
                result['ref_piece'] = result.pop('labeled_select_group2/ref_piece')
                result['statut'] = result.pop('_validation_status')
                results.append(result)
    return results



def get_api_data_id(url, id):
    
    results = get_data_by_api(url)
    # Utilisation de filter et lambda pour rechercher l'ID
    desired_result = next(filter(lambda result: result['id'] == id, results), None)
    # Si un élément correspondant est trouvé
    return desired_result








####################################################################
# Fonction de scraping pour le cours de l'or
####################################################################


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








