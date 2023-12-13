# Code by niklacode
import requests
import json
from modules_externe.api_url import HEADER_TOKEN



def get_data_by_api_convention(url):
    headers = {"Authorization": "Token 3a90e95769451669784df608082cf4a546467002"}
    kobo = requests.get(url, headers=headers)
    if kobo.status_code == 200:
        api_data = json.loads(kobo.content)
        data = api_data.get('results', [])
        approved_data = []

        for result in data:
            validation_status = result.get('_validation_status', {}).get('uid')
            if validation_status == 'validation_status_approved':
                result['identifiant'] = result.pop('_id')
                result['submitted_by'] = result.pop('_submitted_by')
                approved_data.append(result)
        for approved in approved_data:
            if 'type_autorisation' in approved:
                    approved['type_autorisation'] = approved['type_autorisation'].split()
            #if 'point' in approved:
            #    approved['point'] = approved['point'].split()
            #if 'question35' in approved:
            #   approved['question35'] = approved['question35'].split()

        return approved_data

    return []


def get_api_data_id_convention(url, identifiant):
    
    results = get_data_by_api_convention(url)
    # Utilisation de filter et lambda pour rechercher l'ID
    desired_result = next(filter(lambda result: result['identifiant'] == identifiant, results), None)
    # Si un élément correspondant est trouvé
    return desired_result




