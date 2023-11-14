from django.shortcuts import render
from modules_externe.cours_or import get_data_by_url
from django.http import JsonResponse
from paramettre.models import Regions
import json


def import_regions(request):
    
    data = []

    for item in data:
        region = Regions(
            numero=item["numero"],
            nomreg=item["nomreg"],
            cheflieu=item["cheflieu"],
            created=item["created"],
            modified=item["modified"]
        )
        region.save()

    return JsonResponse({"message": "Données importées avec succès"})