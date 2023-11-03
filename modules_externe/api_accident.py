# Code by niklacode
import requests
import json
from modules_externe.api_url import HEADER_TOKEN



def get_data_by_api_accident(url):
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
                result['nom_localite'] = result.pop('labeled_select_group1/nom_localite')
                result['nom_site'] = result.pop('labeled_select_group1/nom_site')
                result['type_rapport'] = result.pop('labeled_select_group1/type_rapport')
                result['question5'] = result.pop('labeled_select_group1/question5')
                result['question6'] = result.pop('labeled_select_group1/question6')
                result['type'] = result.pop('labeled_select_group1/type')
                result['question'] = result.pop('labeled_select_group1/question')
                result['question14'] = result.pop('labeled_select_group1/question14')
                result['question7'] = result.pop('labeled_select_group1/question7')
                result['question8'] = result.pop('labeled_select_group1/question8')
                result['question9'] = result.pop('labeled_select_group1/question9')
                result['question10'] = result.pop('labeled_select_group1/question10')
                result['question11'] = result.pop('labeled_select_group1/question11')
                result['question12'] = result.pop('labeled_select_group1/question12')
                result['question13'] = result.pop('labeled_select_group1/question13')
                result['question14_001'] = result.pop('labeled_select_group1/question14_001')
                result['vict_hom'] = result.pop('labeled_select_group1/vict_hom')
                result['vict_fem'] = result.pop('labeled_select_group1/vict_fem')
                result['vict_enf'] = result.pop('labeled_select_group1/vict_enf')
                result['mort_hom'] = result.pop('labeled_select_group1/mort_hom')
                result['mort_fem'] = result.pop('labeled_select_group1/mort_fem')
                result['mort_enf'] = result.pop('labeled_select_group1/mort_enf')
                result['statut'] = result.pop('_validation_status')
                results.append(result)
    return results




def get_api_data_id_accident(url, identifiant):
    
    results = get_data_by_api_accident(url)
    # Utilisation de filter et lambda pour rechercher l'ID
    desired_result = next(filter(lambda result: result['identifiant'] == identifiant, results), None)
    # Si un élément correspondant est trouvé
    return desired_result