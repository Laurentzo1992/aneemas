from django.shortcuts import render
from modules_externe.cours_or import get_data_by_url
from django.http import JsonResponse
from paramettre.models import Comsites, Provinces, Regions, Typesites, Statutsites
import json
import csv
from datetime import datetime
from datetime import date
from itertools import islice
import pathlib
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Migrate data from JSON file to Comsites model'

    def handle(self, *args, **options):
        datafile = settings.BASE_DIR / 'data' / 'site.json'
        #json_file_path = options['json_file']

        with open(datafile, 'r') as file:
            data = json.load(file)

        for entry in data:
            
            region = int(entry["region"])
            try:
                region = Regions.objects.get(id=region)
            except Regions.DoesNotExist:
           
                continue
            
            province = int(entry["province"])
            try:
                province = Provinces.objects.get(id=province)
            except Provinces.DoesNotExist:
            
                continue
            
            
            typesite = int(entry["typesite"])
            try:
                typesite = Typesites.objects.get(id=typesite)
            except Typesites.DoesNotExist:
           
                continue
            
            
            
            statut = entry.get("statut")
            if statut is not None:
                statut = int(statut)
                try:
                    statut = Statutsites.objects.get(id=statut)
                except Statutsites.DoesNotExist:
                    continue
            else:
                statut = None
            
            comsite, created = Comsites.objects.get_or_create(code_site=entry['code_site'])
            date_creation_str = entry.get('date_creation', None)
            
            if date_creation_str:
                try:
                    date_creation = datetime.strptime(date_creation_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    self.stderr.write(self.style.ERROR(f'Invalid date format: {date_creation_str}'))
                    continue
                comsite.date_creation = date_creation
            #comsite.date_creation = entry.get('date_creation', None)
            comsite.nom_site = entry.get('nom_site')
            comsite.region = region
            comsite.province = province
            comsite.commune = entry.get('commune')
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
            comsite.zone = entry.get('zone')
            comsite.longitude = entry.get('longitude')
            comsite.latitude = entry.get('latitude')
            comsite.longitude1 = entry.get('longitude1')
            comsite.latitude1 = entry.get('latitude1')
            comsite.etendu = entry.get('etendu')
            comsite.p_chimique = bool(entry.get('p_chimique'))
            comsite.p_explosif = bool(entry.get('p_explosif'))
            comsite.machine = entry.get('machine')
            comsite.conflit = bool(entry.get('conflit'))
            comsite.obs_geo = entry.get('obs_geo')

            comsite.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Comsite created: {comsite.code_site}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Comsite updated: {comsite.code_site}'))
