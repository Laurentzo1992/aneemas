# Code by niklacode
import requests
import json
from modules_externe.api_url import HEADER_TOKEN



def get_data_by_api_enrolement(url):
    results = []
    kobo = requests.get(url, headers=HEADER_TOKEN)
    if kobo.status_code == 200:
        api_data = json.loads(kobo.content)
        data = api_data.get('results', [])
        for result in data:
            validation_status = result.get('_validation_status', {}).get('uid')
            if validation_status == 'validation_status_approved':
                result['identifiant'] = result.pop('_id')
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
        for entry in results:
            if 'type_carte' in entry:
                entry['type_carte'] = entry['type_carte'].split()
    return results



def get_api_data_id_enrolement(url, identifiant):
    
    results = get_data_by_api_enrolement(url)
    # Utilisation de filter et lambda pour rechercher l'ID
    desired_result = next(filter(lambda result: result['identifiant'] == identifiant, results), None)
    # Si un élément correspondant est trouvé
    return desired_result