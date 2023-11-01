from django.db.models.signals import post_save, post_delete
from django.db import models
from datetime import date

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from paramettre.models import Typecarte, Comptoires, Cartartisants
from authentication.models import User

from django.utils import timezone


# Create your models here.

class Fichecontrol(models.Model):
    id = models.AutoField(primary_key=True)
    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    observation = models.CharField(max_length=256)
    date_control = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def numero(self):
        if self.id:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            return f"CTL{str(self.id).zfill(4)}-{last_two_digits_of_year}"
        return None
        
    def __str__(self):
        return self.numero

class FicheTarification(models.Model):
    id = models.AutoField(primary_key=True)
     # Association avec le modèle User (Celui qui creer la fiche)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    observation = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    date_tarification = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)

    fiche_control = models.ForeignKey(Fichecontrol, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def numero(self):
        if self.id:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            return f"FAC{str(self.id).zfill(4)}-{last_two_digits_of_year}"
        return None

    def __str__(self):
        return self.numero

class Lingot(models.Model):
    id = models.AutoField(primary_key=True)
    poids_brut = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2,)
    poids_immerge = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    ecart = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    densite = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    titre_carat = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    quantite_or_fin = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    date_reception = models.DateTimeField(blank=True)
    observation = models.CharField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Lien vers la fiche de contrôle
    fiche_control = models.ForeignKey(Fichecontrol, on_delete=models.SET_NULL, null=True, blank=True)

    # Lien vers la fiche de contrôle
    fiche_tarification = models.ForeignKey(FicheTarification, on_delete=models.SET_NULL, null=True, blank=True)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    @property
    def numero(self):
        if self.id:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            return f"{str(self.id).zfill(4)}-{last_two_digits_of_year}"
        return None

    def update_properties(self):
            # Récupérer toutes les pesées associées à ce lingot
            pesees = Pesee.objects.filter(lingot=self, active=True)

            # Calculer les moyennes des propriétés
            if pesees.exists():
                self.ecart = sum(psee.ecart for psee in pesees) / len(pesees)
                self.poids_brut = sum(psee.poids_brut for psee in pesees) / len(pesees)
                self.poids_immerge = sum(psee.poids_immerge for psee in pesees) / len(pesees)
                self.titre_carats = sum(psee.titre_carat for psee in pesees) / len(pesees)
            else:
                self.ecart = 0
                self.poids_brut = 0
                self.poids_immerge = 0
                self.titre_carats = 0

            self.save()

    def __str__(self):
        return self.numero
    
class Pesee(models.Model):
    poids_brut = models.DecimalField(max_digits=10, decimal_places=2)
    poids_immerge = models.DecimalField(max_digits=10, decimal_places=2)
    ecart = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    densite = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    titre_carat = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)  # Modifié en champ décimal
    quantite_or_fin = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    date_pesee = models.DateField(blank=True, null=True, )
    observation = models.CharField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    lingot = models.ForeignKey('Lingot', on_delete=models.CASCADE)  # Chaque pesée est liée à un lingot

    # Les caractristique du lingot est la moyenne des resultat pour chaque pesé
    # Indique si ce pesé est utilisé dans le calcul de caracteristique du lingot
    valide = models.BooleanField(default=True)

    def get_numero_pesee(self):
        pesees_precedentes = Pesee.objects.filter(lingot=self.lingot, date_pesee__lte=self.date_pesee)
        numero_pesee = pesees_precedentes.count() + 1
        return numero_pesee

    def __str__(self):
        if self.lingot is not None:
            numero_pesee = self.get_numero_pesee()
            return f"P{numero_pesee}"
        else:
            return 'N/A'

    # Ajout de la méthode pour le champ virtuel "Ecart"
    @property
    def numero(self):
        return self.get_numero_pesee()

    # Ajout de la méthode pour le champ virtuel "Ecart"
    @property
    def ecart(self):
        return self.poids_brut - self.poids_immerge

    @property
    def densite(self):
        return self.poids_brut / (self.poids_brut - self.poids_immerge)
