# serializers.py

from rest_framework import serializers

from authentication.models import User
from .models import Client, Facture, FactureProforma, FicheTarification, Fichecontrol, Fournisseur, Lingot, Payement, Pesee, PrixDesSubstances, RepresentantFournisseur, TypeDeClient, TypeSubstance, Vente

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class RepresentantFournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepresentantFournisseur
        fields = ['nom', 'prenom', 'email', 'telephone', 'numero_carte']

class FournisseurSerializer(serializers.ModelSerializer):
    representants = RepresentantFournisseurSerializer(many=True, read_only=True, source="representantfournisseur_set")
    class Meta:
        model = Fournisseur
        fields = ['nom', 'prenom', 'email', 'telephone', 'representants']


class PeseeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesee
        fields = ['numero', 'poids_brut', 'poids_immerge', 'ecart', 'densite', 'titre', 'or_fin', 'actif']  # Replace with actual field names

class LingotSerializer(serializers.ModelSerializer):
    pesees = PeseeSerializer(many=True, read_only=True, source="pesee_set")
    price = serializers.SerializerMethodField()

    class Meta:
        model = Lingot
        fields = ['numero', 'poids_brut', 'price', 'poids_immerge', 'ecart', 'densite', 'titre', 'or_fin', 'pesees']  # Replace with actual field names
    
    def get_price(self, obj):
        return obj.price

class FichecontrolSerializer(serializers.ModelSerializer):
    lingots = LingotSerializer(many=True, read_only=True, source='lingot_set')
    user = UserSerializer()
    fournisseur = FournisseurSerializer()
    class Meta:
        depth = 3
        model = Fichecontrol
        fields = ['numero', 'observation', 'date_control', 'lingots', 'user', 'fournisseur']  # Replace with actual field names

class FicheTarificationSerializer(serializers.ModelSerializer):
    fichecontrol = FichecontrolSerializer()
    representant = RepresentantFournisseurSerializer()
    user = UserSerializer()
    class Meta:
        depth = 3
        model = FicheTarification
        fields = ['numero', 'cours', 'date_tarification', 'fichecontrol', 'observation', 'representant', 'user']

class PayementSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    fournisseur = FournisseurSerializer()
    class Meta:
        depth = 3
        model = Payement
        fields = ['numero', 'montant', 'mode_payement',\
                  'reference_payement', 'document_payement',
                  'recu_payement', 'document_identite',
                  'reference_document_identite', 'autre_document',
                  'direction', 'archived', 'observation', 'confirme',
                  'actif', 'created', 'modified',
                  'created', 'fournisseur', 'user']

class TypeSubstanceSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 3
        model = TypeSubstance
        fields = ['libelle', 'symbole']
        
class PrixDesSubstancesSerializer(serializers.ModelSerializer):
    type_de_substance = TypeSubstanceSerializer()
    class Meta:
        depth = 3
        model = PrixDesSubstances
        fields = ['type_de_substance', 'poids', 'cours_de_substance', 'reduction_commercial', 'prix']

class FactureSerializer(serializers.ModelSerializer):
    prix_des_substances = PrixDesSubstancesSerializer(many=True, read_only=True, source="prixdessubstances_set")
    class Meta:
        depth = 3
        model = Facture
        fields = ['id', 'numero', 'cours_du_dollar', 'cours_en_euro', 'reduction_commercial', 'pourcentage_tva', 'observation', 'prix_des_substances']

class TypeDeClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDeClient
        fields = ['libelle']

class ClientSerializer(serializers.ModelSerializer):
    type_de_client = TypeDeClientSerializer()
    class Meta:
        model = Client
        fields = ['nom', 'societe', 'reference_societe', 'pays', 'email', 'telephone', 'type_de_client']

class VenteSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    class Meta:
        depth = 3
        model = Vente
        fields = ['numero', 'objet', 'date', 'client', 'observation']