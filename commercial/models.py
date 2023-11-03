from decimal import Decimal
from django.db.models.signals import post_save, post_delete
from django.db import models
from datetime import date

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from paramettre.models import Typecarte, Comptoires, Cartartisants
from authentication.models import User

from django.utils import timezone

#Type client
class TypeClient(models.Model):
    libelle = models.CharField(max_length=60)
    description = models.CharField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Types de clients"

    def __str__(self):
        return self.libelle if self.libelle is not None else "N/A"

class Client(models.Model):
    nom = models.CharField(blank=True, null=True, max_length=60)
    prenom = models.CharField(blank=True, null=True, max_length=60)
    description = models.CharField(blank=True, null=True, max_length=256)
    type_client = models.ForeignKey(TypeClient,  on_delete=models.CASCADE, null=False, blank=False)
    cartartisan = models.ForeignKey(Cartartisants, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.nom
    

class Fichecontrol(models.Model):
    id = models.AutoField(primary_key=True)
    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    observation = models.CharField(max_length=256)
    date_control = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Fiches de Control"

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

    class Meta:
        verbose_name_plural = "Fiches de Tarification"

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def numero(self):
        if self.id:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            return f"FAC{str(self.id).zfill(4)}-{last_two_digits_of_year}"
        return None

    def __str__(self):
        return self.numero

class TypeLingot(models.Model):
    libelle = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Types de Lingots"

    def __str__(self):
        return self.libelle

class EmplacementLingot(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.CharField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Emplacements Lingots"

    def __str__(self):
        return self.nom if self.nom is not None else "N/A"

class Fonte(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    etat = models.CharField(max_length=10, choices=[
        ('debut', 'Début'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé')
    ])
    observation = models.CharField(blank=True, null=True, max_length=256)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def numero(self):
        if self.id:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            return f"FT{str(self.id).zfill(4)}-{last_two_digits_of_year}"
        return None
    
    def __str__(self):
        return f"Debut {self.date_debut} fin: {self.date_fin}"

class Lingot(models.Model):
    id = models.AutoField(primary_key=True)
    poids_brut = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2,)
    poids_immerge = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    ecart = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    densite = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    titre = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    or_fin = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    date_reception = models.DateTimeField(blank=True)
    observation = models.CharField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    emplacement = models.ForeignKey(EmplacementLingot, on_delete=models.SET_NULL, null=True, blank=True)
    type_lingot = models.ForeignKey(TypeLingot, on_delete=models.SET_NULL, null=True, blank=True)


    # Lien vers la fiche de contrôle
    fiche_control = models.ForeignKey(Fichecontrol, on_delete=models.SET_NULL, null=True, blank=True)

    # Lien vers la fiche de contrôle
    fiche_tarification = models.ForeignKey(FicheTarification, on_delete=models.SET_NULL, null=True, blank=True)

    # Fonte à laquelle ce lingot est associé
    fonte = models.ForeignKey(Fonte, null=True, blank=True, on_delete=models.CASCADE)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Lingots"

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
                self.titre = sum(psee.titre for psee in pesees) / len(pesees)
            else:
                self.ecart = 0
                self.poids_brut = 0
                self.poids_immerge = 0
                self.titre = 0

            self.save()

    def __str__(self):
        return self.numero
    
class Pesee(models.Model):
    poids_brut = models.DecimalField(max_digits=10, decimal_places=2)
    poids_immerge = models.DecimalField(max_digits=10, decimal_places=2)
    date_pesee = models.DateField(blank=True, null=True, )
    observation = models.CharField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    lingot = models.ForeignKey('Lingot', on_delete=models.CASCADE)  # Chaque pesée est liée à un lingot

    # Les caractristique du lingot est la moyenne des resultat pour chaque pesé
    # Indique si ce pesé est utilisé dans le calcul de caracteristique du lingot
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Pesees"

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
        return 1 if self.ecart == 0 else self.poids_brut / self.ecart

    @property
    def titre(self):
        return Decimal('20.6')
        

    @property
    def or_fin(self):
        return "{:.2f}".format(self.titre * self.poids_brut/24)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.actif:
            # If pricing is enabled, update Livraison fields
            self.lingot.poids_brut = self.poids_brut
            self.lingot.poids_immerge = self.poids_immerge
            self.lingot.ecart = self.ecart
            self.lingot.densite = self.densite
            self.lingot.titre = self.titre
            self.lingot.or_fin = self.or_fin
            self.lingot.save()
    
    def delete(self, *args, **kwargs):
        was_active = self.active
        super().delete(*args, **kwargs)
        
        if was_active:
            # If deleted pricing was enabled, update Livraison fields
            self.lingot.poids_brut = 0
            self.lingot.poids_immerge = 0
            self.lingot.ecart = 0
            self.lingot.densite = 0
            self.lingot.titre = 0
            self.lingot.or_fin = 0
            self.lingot.save()


class Factures(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    fiche_tarification = models.ForeignKey(Lingot,  on_delete=models.SET_NULL, null=True)

    # Generer un numero de Facture
    def generate_numero_facture(self):
        last_two_digits_of_year = str(self.date_reception.year)[-2:]
        self.numero_lingo = f"{self.id}.zfill(4)-{last_two_digits_of_year}"
    
    # Surcharge de la méthode save pour appeler la fonction generate_numero_fiche_control
    def save(self, *args, **kwargs):
        if not self.id:
            # Si la fiche n'a pas encore d'ID, il n'est pas encore enregistré dans la base de données
            temp_facture = Factures.objects.create()  # Créer un Lingot non enregistré pour obtenir un ID
            self.id = temp_facture.id  # Assigner l'ID généré a la fiche actuel
            self.generate_numero_facture()

        super().save(*args, **kwargs)
    
    # stocker le numéro de la facture
    numero_facture = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Factures"

    def __str__(self):
        return self.generate_numero_facture




class MouvementLingot(models.Model):
    type_lingot = models.ForeignKey(TypeLingot, on_delete=models.CASCADE) 
    origin = models.ForeignKey(EmplacementLingot, related_name='mouvements_origin', on_delete=models.CASCADE)
    destination = models.ForeignKey(EmplacementLingot, related_name='mouvements_destination', on_delete=models.CASCADE)
    ETAT_CHOICES = [
        ('debut', 'Début'),
        ('encours', 'En cours'),
        ('arrive', 'Arrivé'),
    ]
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_arrive = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Mouvements Lingots"

class DirectionLingot(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type_lingot = models.ForeignKey(TypeLingot, on_delete=models.CASCADE, blank=True, null=True)
    origin = models.ForeignKey(EmplacementLingot, related_name='directions_origin', on_delete=models.CASCADE)
    destination = models.ForeignKey(EmplacementLingot, related_name='directions_destination', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Directions Lingots"

    def __str__(self):
        return self.name
    

class StragieTarification(models.Model):
    nom = models.CharField(max_length=100)
    priority = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    actif = models.BooleanField(default=True)
    application_auto = models.BooleanField(default=False)
    marge = models.DecimalField(max_digits=10, decimal_places=2)
    marge_auto = models.BooleanField(default=True)
    cours = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    cours_auto = models.BooleanField(default=True)
    globale = models.BooleanField(default=False)
    type_client = models.ForeignKey(TypeClient,  on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Strategies de tarifications"

    def has_expired(self):
        today = date.today()
        return self.start_date <= today and (self.end_date is None or self.end_date >= today)

    def __str__(self):
        return self.name



class ModePayement(models.Model):
    libelle = models.CharField(max_length=60)
    actif = models.BooleanField(default=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Modes de paiements"


class Paiements(models.Model):
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Lien vers la fiche de contrôle
    fiche_tarification = models.ForeignKey(FicheTarification, on_delete=models.SET_NULL, null=True, blank=True)


    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Modes de paiements"

@receiver(pre_save, sender=Pesee)
def ensure_single_enabled_pesee(sender, instance, **kwargs):
    if instance.actif:
        # Disable all other Pricing objects related to the same Lingot
        Pesee.objects.filter(lingot=instance.lingot, actif=True).exclude(pk=instance.pk).update(actif=False)