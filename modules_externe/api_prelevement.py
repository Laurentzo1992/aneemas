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
                result['identifiant'] = result.pop('_id')
                result['submitted_by'] = result.pop('_submitted_by')
                #result['point'] = result.pop('labeled_select_group2/point')
                result['coordonnees'] = result.pop('labeled_select_group2/coordonnees')
                result['coordonnees_manu'] = result.pop('labeled_select_group2/coordonnees_manu')
                result['lieu'] = result.pop('labeled_select_group2/lieu')
                result['motif'] = result.pop('labeled_select_group2/motif')
                result['quantite'] = result.pop('labeled_select_group2/quantite')
                result['nb_facons_v'] = result.pop('labeled_select_group2/nb_facons_v')
                result['nb_facons_p'] = result.pop('labeled_select_group2/nb_facons_p')
                result['type_nature_echantillon'] = result.pop('labeled_select_group2/type_nature_echantillon')
                result['mis_conductivite'] = result.pop('labeled_select_group2/mis_conductivite')
                result['mis_ph'] = result.pop('labeled_select_group2/mis_ph')
                result['mis_tds'] = result.pop('labeled_select_group2/mis_tds')
                result['mis_oxigene_dissous'] = result.pop('labeled_select_group2/mis_oxigene_dissous')
                result['mis_turbidite'] = result.pop('labeled_select_group2/mis_turbidite')
                #result['mis_bruits'] = result.pop('labeled_select_group2/mis_bruits')
                #result['mis_odeur'] = result.pop('labeled_select_group2/mis_odeur')
                #result['mis_lumiere'] = result.pop('labeled_select_group2/mis_lumiere')
                result['nom_personne1'] = result.pop('labeled_select_group2/nom_personne1')
                result['nom_personne2'] = result.pop('labeled_select_group2/nom_personne2')
                result['adresse'] = result.pop('labeled_select_group2/adresse')
                result['statut'] = result.pop('_validation_status')
                results.append(result)
    return results




def get_api_data_id_prelevement(url, identifiant):
    
    results = get_data_by_api_prelevement(url)
    # Utilisation de filter et lambda pour rechercher l'ID
    desired_result = next(filter(lambda result: result['identifiant'] == identifiant, results), None)
    # Si un élément correspondant est trouvé
    return desired_result