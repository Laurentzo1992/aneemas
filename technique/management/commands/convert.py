from django.core.management.base import BaseCommand
from pyproj import Proj, transform
from paramettre.models import Comsites

class Command(BaseCommand):
    help = 'Convert WGS84 coordinates to a different coordinate system'

    def handle(self, *args, **options):
        # WGS84 coordinate system
        wgs84 = Proj(init='epsg:4326')

        # UTM coordinate system (you can change this to your desired coordinate system)
        utm = Proj(init='epsg:32630')  # Example: UTM Zone 33N

        # Get all objects from Comsites
        comsites = Comsites.objects.all()

        for comsite in comsites:
            # Convert longitude and latitude to UTM
            utm_x, utm_y = transform(wgs84, utm, float(comsite.longitude), float(comsite.latitude))

            # Update the model with the new coordinates
            comsite.longitude = float(utm_x)
            comsite.latitude = float(utm_y)
            comsite.save()

        self.stdout.write(self.style.SUCCESS('Coordinates converted successfully for all Comsites.'))
