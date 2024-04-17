# Code by niklacode
import requests
import json
from modules_externe.api_url import HEADER_TOKEN



def get_data_by_api_prelevement(url):
    results = []
    kobo = requests.get(url, headers=HEADER_TOKEN)
    if kobo.status_code == 200:
        api_data = json.loads(kobo.content)
        data = api_data.get('results', [])
        for result in data:
            validation_status = result.get('_validation_status', {}).get('uid')
            if validation_status == 'validation_status_approved':
                result['identifiant'] = result.get('_id', None)
                result['submitted_by'] = result.get('_submitted_by',None)
                result['point'] = result.get('labeled_select_group2/point', None)
                result['coordonnees'] = result.get('labeled_select_group2/coordonnees', None)
                result['coordonnees_manu'] = result.get('labeled_select_group2/coordonnees_manu', None)
                result['lieu'] = result.get('labeled_select_group2/lieu', None)
                result['motif'] = result.get('labeled_select_group2/motif', None)
                result['quantite'] = result.get('labeled_select_group2/quantite', None)
                result['nb_facons_v'] = result.get('labeled_select_group2/nb_facons_v', None)
                result['nb_facons_p'] = result.get('labeled_select_group2/nb_facons_p', None)
                result['type_nature_echantillon'] = result.get('labeled_select_group2/type_nature_echantillon', None)
                result['mis_conductivite'] = result.pop('labeled_select_group2/mis_conductivite', None)
                result['mis_ph'] = result.get('labeled_select_group2/mis_ph', None)
                result['mis_tds'] = result.get('labeled_select_group2/mis_tds', None)
                result['mis_oxigene_dissous'] = result.get('labeled_select_group2/mis_oxigene_dissous', None)
                result['mis_turbidite'] = result.get('labeled_select_group2/mis_turbidite', None)
                #result['mis_bruits'] = result.pop('labeled_select_group2/mis_bruits')
                #result['mis_odeur'] = result.pop('labeled_select_group2/mis_odeur')
                #result['mis_lumiere'] = result.pop('labeled_select_group2/mis_lumiere')
                result['nom_personne1'] = result.get('labeled_select_group2/nom_personne1', None)
                result['nom_personne2'] = result.get('labeled_select_group2/nom_personne2', None)
                result['adresse'] = result.get('labeled_select_group2/adresse', None)
                result['statut'] = result.get('_validation_status', None)
                results.append(result)
    return results




def get_api_data_id_prelevement(url, identifiant):
    
    results = get_data_by_api_prelevement(url)
    # Utilisation de filter et lambda pour rechercher l'ID
    desired_result = next(filter(lambda result: result['identifiant'] == identifiant, results), None)
    # Si un élément correspondant est trouvé
    return desired_result