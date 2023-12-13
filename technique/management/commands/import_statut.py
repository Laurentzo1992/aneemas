from paramettre.models import *
import csv
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Migrate data from CSV file to Typesites model'

    def handle(self, *args, **options):
        csvfile = settings.BASE_DIR / 'data' / 'statut_site.csv'
        with open(csvfile, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=';')
            #next(csv_reader)  # Skip the header row if it exists
            
            for row in csv_reader:
                libelle = row[0]  # Assuming libelle is in the 4th column
                type, created = Statutsites.objects.get_or_create(libelle=libelle) 
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Typesites created: {type.libelle}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Typesites updated: {type.libelle}'))