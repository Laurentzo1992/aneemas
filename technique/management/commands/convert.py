from django.core.management.base import BaseCommand
from pyproj import Proj, transform
from paramettre.models import Comsites

class Command(BaseCommand):
    help = 'Convert UTM coordinates (Zone 30) to WGS84'

    def handle(self, *args, **options):
        # UTM coordinate system (Zone 30 for Western Europe)
        utm = Proj(init='epsg:32730')

        # WGS84 coordinate system
        wgs84 = Proj(init='epsg:4326')

        # Get all objects from Comsites
        comsites = Comsites.objects.all()

        for comsite in comsites:
            # Convert UTM coordinates to WGS84
            lon, lat = transform(utm, wgs84, float(comsite.longitude), float(comsite.latitude))

            # Update the model with the new coordinates
            comsite.longitude = float(lon)
            comsite.latitude = float(lat)
            comsite.save()

            # Optionally, you may print the conversion details for each Comsite
            self.stdout.write(self.style.SUCCESS(f'Coordinates converted for Comsite {comsite.id}: '
                                                 f'Longitude: {lon}, Latitude: {lat}'))

        self.stdout.write(self.style.SUCCESS('Coordinates converted successfully for all Comsites.'))
