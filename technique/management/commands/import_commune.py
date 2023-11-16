from django.shortcuts import render
from modules_externe.cours_or import get_data_by_url
from django.http import JsonResponse
from paramettre.models import Provinces, Communes
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
        
        datafile = settings.BASE_DIR / 'data' / 'communes.json'
        
        with open(datafile, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            for item in data:
                province_id = int(item["province_id"])
                try:
                    province = Provinces.objects.get(id=province_id)
                except Provinces.DoesNotExist:
            # Gérer le cas où la région n'existe pas
                    continue
                commune, created = Communes.objects.get_or_create(nom_commune=item['nomcom'])
                commune.province = province
                commune.save()
          
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Comsite created: {commune.nom_commune}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Comsite updated: {commune.nom_commune}'))



   

