from django.shortcuts import render
from modules_externe.cours_or import get_data_by_url
from django.http import JsonResponse
from paramettre.models import *
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
        
        datafile = settings.BASE_DIR / 'data' / 'provinces.json'
        
        with open(datafile, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            for item in data:
                region_id = int(item["region"])
                try:
                    region = Regions.objects.get(id=region_id)
                except Regions.DoesNotExist:
            # Gérer le cas où la région n'existe pas
                    continue

                province, created = Provinces.objects.get_or_create(numero=item['numero']) 
                province.nomprov = item.get('nomprov')
                province.region = region
                province.save()
          
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Comsite created: {province.nomprov}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Comsite updated: {province.nomprov}'))
