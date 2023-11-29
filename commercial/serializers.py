# serializers.py

from rest_framework import serializers
from .models import Fichecontrol, Lingot, Pesee

class PeseeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesee
        fields = ['numero', 'poids_brut', 'poids_immerge', 'ecart', 'densite', 'titre', 'or_fin', 'actif']  # Replace with actual field names

class LingotSerializer(serializers.ModelSerializer):
    pesees = PeseeSerializer(many=True, read_only=True, source="pesee_set")

    class Meta:
        model = Lingot
        fields = ['numero', 'poids_brut', 'poids_immerge', 'ecart', 'densite', 'titre', 'or_fin', 'pesees']  # Replace with actual field names

class FichecontrolSerializer(serializers.ModelSerializer):
    lingots = LingotSerializer(many=True, read_only=True, source='lingot_set')

    class Meta:
        depth = 3
        model = Fichecontrol
        fields = ['numero', 'observation', 'date_control', 'lingots']  # Replace with actual field names
