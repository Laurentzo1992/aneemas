from paramettre.models import *
import json
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand




class Command(BaseCommand):
    help = 'Migrate data from JSON file to Comsites model'

    def handle(self, *args, **options):
        datafile = settings.BASE_DIR / 'data' / 'site3.json'

        with open(datafile, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for entry in data:
            region_id = entry.get("region")
            province_id = entry.get("province")
            commune_id = entry.get("commune")
            typesite_id = entry.get("typesite")
            statut_id = entry.get("statut")

            # Check for None or empty string values
            if (
                region_id is None or not str(region_id).isdigit() or
                province_id is None or not str(province_id).isdigit() or
                commune_id is None or not str(commune_id).isdigit() or
                typesite_id is None or not str(typesite_id).isdigit() or
                statut_id is not None and not str(statut_id).isdigit()
            ):
                self.stderr.write(self.style.ERROR('Invalid ID(s). Skipping entry.'))
                continue

            region_id = int(region_id)
            province_id = int(province_id)
            commune_id = int(commune_id)
            typesite_id = int(typesite_id)
            statut_id = int(statut_id) if statut_id is not None else None

            try:
                region = Regions.objects.get(id=region_id)
                province = Provinces.objects.get(id=province_id)
                commune = Communes.objects.get(id=commune_id)
                typesite = Typesites.objects.get(id=typesite_id)
                statut = Statutsites.objects.get(id=statut_id) if statut_id is not None else None
                # ... (rest of your code remains unchanged)
            except (Regions.DoesNotExist, Provinces.DoesNotExist, Communes.DoesNotExist, Typesites.DoesNotExist, Statutsites.DoesNotExist):
                self.stderr.write(self.style.ERROR(f'Invalid IDs. Skipping entry.'))
                continue
            
            
            #Génération du code du site
            region_prefix = region.nomreg[:2].upper()
            province_prefix = province.nomprov[:2].upper()
            commune_prefix = commune.nom_commune[:2].upper()

            # Numéro incrémental unique pour chaque combinaison de région, province et commune
            num_incremental = Comsites.objects.filter(region=region, province=province, commune=commune).count() + 1

            # Formatage du code du site avec un numéro incrémental de 4 chiffres
            code_site = f"{region_prefix}{province_prefix}{commune_prefix}{num_incremental:04d}"

            # Création ou mise à jour de l'objet Comsites
            comsite, created = Comsites.objects.update_or_create(code_site=code_site)

            # Affectation des valeurs
            comsite.date_creation = datetime.strptime(entry.get('date_creation', ''), '%d/%m/%Y').strftime('%Y-%m-%d') if entry.get('date_creation') else None
            comsite.nom_site = entry.get('nom_site') if entry.get('nom_site') else 'Site Anonyme'
            comsite.region = region
            comsite.province = province
            comsite.commune = commune
            comsite.village = entry.get('village')
            comsite.typesite = typesite
            comsite.statut = statut
            comsite.nbre_puit_actif = entry.get('nbre_puit_actif')
            comsite.nbre_puit_total = entry.get('nbre_puit_total')
            comsite.annee_exploitation = entry.get('annee_exploitation')
            comsite.poulation = entry.get('poulation')
            comsite.nom_detenteur = entry.get('nom_detenteur')
            comsite.personne_resource1 = entry.get('personne_resource1')
            comsite.contact_resource1 = entry.get('contact_resource1')
            comsite.personne_resource2 = entry.get('personne_resource2')
            comsite.contact_resource2 = entry.get('contact_resource2')
            comsite.zone = entry.get('zone', 30)
            comsite.longitude = float(entry.get('X', 0.0))
            comsite.latitude = float(entry.get('Y', 0.0))
            comsite.etendu = entry.get('etendu')
            comsite.p_chimique = bool(entry.get('p_chimique'))
            comsite.p_explosif = bool(entry.get('p_explosif'))
            comsite.machine = entry.get('machine')
            comsite.conflit = bool(entry.get('conflit'))
            comsite.obs_geo = entry.get('obs_geo')

            #Sauvegarde de l'objet Comsites
            comsite.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Comsite created: {comsite.nom_site} Code : {comsite.code_site}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Comsite updated:  {comsite.nom_site} Code : {comsite.code_site}'))



            
