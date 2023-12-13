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
        datafile = settings.BASE_DIR / 'data' / 'regions.json'
        #json_file_path = options['json_file']

        with open(datafile, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            for item in data:
                region, created = Regions.objects.get_or_create(numero=item['numero']) 
                region.nomreg = item.get('nomreg')
                region.cheflieu = item.get('cheflieu')
                region.save()
          
            if created:
                self.stdout.write(self.style.SUCCESS(f'Comsite created: {region.nomreg}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Comsite updated: {region.nomreg}'))
