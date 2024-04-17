# Code by niklacode
import requests
import json
from modules_externe.api_url import HEADER_TOKEN



def get_data_by_api_guide(url):
    kobo = requests.get(url, headers=HEADER_TOKEN)
    if kobo.status_code == 200:
        api_data = json.loads(kobo.content)
        data = api_data.get('results', [])
        approved_data = []
        for result in data:
            validation_status = result.get('_validation_status', {}).get('uid')
            if validation_status == 'validation_status_approved':
                result['identifiant'] = result.pop('_id')
                result['submitted_by'] = result.pop('_submitted_by')
                result['statut'] = result.pop('_validation_status')
                approved_data.append(result)
        for approved in approved_data:
            if 'type_contrat' in approved:
                approved['type_contrat'] = approved['type_contrat'].split()
        return approved_data

    return []

def get_api_data_id_guide(url, identifiant):
    
    results = get_data_by_api_guide(url)
    # Utilisation de filter et lambda pour rechercher l'ID
    desired_result = next(filter(lambda result: result['identifiant'] == identifiant, results), None)
    # Si un élément correspondant est trouvé
    return desired_result