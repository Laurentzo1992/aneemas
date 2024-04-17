# Code by niklacode
import requests
import json
from modules_externe.api_url import HEADER_TOKEN



def get_data_by_api_accident(url):  # sourcery skip: extract-method
    results = []
    kobo = requests.get(url, headers=HEADER_TOKEN)
    if kobo.status_code == 200:
        api_data = json.loads(kobo.content)
        data = api_data.get('results', [])
        for result in data:
            validation_status = result.get('_validation_status', {}).get('uid')
            if validation_status == 'validation_status_approved':
                result['identifiant'] = result.get('_id', None)
                result['submitted_by'] = result.get('_submitted_by', None)
                result['nom_localite'] = result.get('labeled_select_group1/nom_localite', None)
                result['type_rapport'] = result.get('labeled_select_group1/type_rapport', None)
                result['question5'] = result.get('labeled_select_group1/question5', None)
                result['question6'] = result.get('labeled_select_group1/question6', None)
                result['question'] = result.get('labeled_select_group1/question', None)
                result['question14'] = result.get('labeled_select_group1/question14', None)
                result['question7'] = result.get('labeled_select_group1/question7', None)
                result['question8'] = result.get('labeled_select_group1/question8', None)
                result['question9'] = result.get('labeled_select_group1/question9', None)
                result['question10'] = result.get('labeled_select_group1/question10', None)
                result['question11'] = result.get('labeled_select_group1/question11', None)
                result['question12'] = result.get('labeled_select_group1/question12',None)
                result['question13'] = result.get('labeled_select_group1/question13', None)
                result['question14_001'] = result.pop('labeled_select_group1/question14_001', None)
                result['vict_hom'] = result.get('labeled_select_group1/vict_hom', None)
                result['vict_fem'] = result.get('labeled_select_group1/vict_fem', None)
                result['vict_enf'] = result.get('labeled_select_group1/vict_enf', None)
                result['mort_hom'] = result.get('labeled_select_group1/mort_hom', None)
                result['mort_fem'] = result.get('labeled_select_group1/mort_fem', None)
                result['mort_enf'] = result.get('labeled_select_group1/mort_enf', None)
                result['statut'] = result.get('_validation_status', None)
                results.append(result)
    return results




def get_api_data_id_accident(url, identifiant):
    
    results = get_data_by_api_accident(url)
    # Utilisation de filter et lambda pour rechercher l'ID
    desired_result = next(filter(lambda result: result['identifiant'] == identifiant, results), None)
    # Si un élément correspondant est trouvé
    return desired_result