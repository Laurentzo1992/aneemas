from decimal import Decimal
from django.db.models.signals import post_save, post_delete
from django.db import models
from datetime import date

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from django.forms import ValidationError

from paramettre.models import Typecarte, Comptoires, Cartartisants
from authentication.models import User

from django.utils import timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models as djangomodels
from django.core.validators import MinValueValidator

#Type client
class TypeFournisseur(models.Model):
    libelle = models.CharField(max_length=60)
    description = models.CharField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Types fournisseurs"

    def __str__(self):
        return self.libelle if self.libelle is not None else "N/A"

class Fournisseur(models.Model):
    prenom = models.CharField(blank=True, null=True, max_length=60)
    nom = models.CharField(blank=True, null=True, max_length=60)
    email = models.EmailField(max_length=60)
    telephone = models.CharField(blank=True, null=True, max_length=15)
    cartartisan = models.ForeignKey(Cartartisants, blank=True, null=True, on_delete=models.CASCADE)
    description = models.CharField(blank=True, null=True, max_length=256)
    type_fournisseur = models.ForeignKey(TypeFournisseur,  on_delete=models.CASCADE, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Fournisseurs"

    def __str__(self):
        return self.nom




class TypeSubstance(models.Model):
    libelle = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Types Substances"

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
    
       

class Fichecontrol(models.Model):
    # id = models.AutoField(primary_key=True)
    # Association avec le modèle User (Celui qui enregistre le lingot)
    observation = models.CharField(max_length=256, null=True, blank=True)
    date_control = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # fiche_tarification = models.ForeignKey(FicheTarification, on_delete=models.SET_NULL, null=True, blank=True)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)

    numero = models.CharField(max_length=16, blank=True, null=True, unique=True)
    archived = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "Fiches de Control"

    # @property
    # def numero(self):
    #     if self.id:
    #         year = self.created.year
    #         last_two_digits_of_year = str(year)[-2:]
    #         return f"CTL{str(self.id).zfill(4)}-{last_two_digits_of_year}"
    #     return None

        
    def __str__(self):
        return self.numero
    
    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user

        # if not self.id and not self.numero:
        #     super().save(*args, **kwargs)  # Save the model to get an ID
        #     # Format the ID and save it to the 'formatted_id' field
        #     year = self.created.year
        #     last_two_digits_of_year = str(year)[-2:]
        #     self.numero = f"CTL{str(self.id).zfill(5)}-{last_two_digits_of_year}"
        #     super().save(update_fields=['numero']) 

        if self.created and self.id and not self.numero:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            self.numero = f"CTL{str(self.id).zfill(6)}-{last_two_digits_of_year}"
        
        super().save(*args, **kwargs)

class FicheTarification(models.Model):
    # id = models.AutoField(primary_key=True)
     # Association avec le modèle User (Celui qui creer la fiche)
    cours = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    date_tarification = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    observation = models.CharField(max_length=256, null=True, blank=True)


    # Association avec le modèle User (Celui qui enregistre le lingot)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)

    fichecontrol = models.ForeignKey(Fichecontrol, on_delete=models.SET_NULL, null=True, blank=True)

    numero = models.CharField(max_length=16, blank=True, null=True, unique=True)

    transferer = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)


    

    class Meta:
        verbose_name_plural = "Fiches de Tarification"
    
    def __str__(self):
        return self.numero if self.numero else "N/A"
    
    # @property
    # def numero(self):
    #     if self.id:
    #         year = self.created.year
    #         last_two_digits_of_year = str(year)[-2:]
    #         return f"FAC{str(self.id).zfill(4)}-{last_two_digits_of_year}"
    #     return None

    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user

        if not self.id and not self.numero:
            super().save(*args, **kwargs)  # Save the model to get an ID
            # Format the ID and save it to the 'formatted_id' field
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            self.numero = f"FTR{str(self.id).zfill(5)}-{last_two_digits_of_year}"
            super().save(update_fields=['numero'])
        else:
            super().save(*args, **kwargs)


class TransferedFicheTarificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transferer=True)

class TransferedFicheTarification(FicheTarification):
    objects = TransferedFicheTarificationManager()
    
    class Meta:
        proxy = True
        verbose_name_plural = "Paiements en attentes"

class Fonte(models.Model):
    date_sortie = models.DateTimeField(auto_now_add=True, editable=False)
    date_retour = models.DateTimeField(null=True, blank=True)
    etat = models.CharField(max_length=10, choices=[
        ('out', 'En cours'),
        ('in', 'Fondu')
    ], default='out')
    observation = models.CharField(blank=True, null=True, max_length=256)

    # Association avec le modèle User (Celui qui enregistre la fonte)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    valider_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='valider_par')
    
    fondu = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    
    @property
    def numero(self):
        if self.id:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            return f"FT{str(self.id).zfill(4)}-{last_two_digits_of_year}"
        return "-"
    
    def __str__(self):
        return self.numero if self.numero else "-"

class ControlBUMIGEB(models.Model):
    date_sortie = models.DateTimeField(auto_now_add=True, editable=False)
    date_retour = models.DateTimeField(null=True, blank=True)
    etat = models.CharField(max_length=10, choices=[
        ('out', 'En cours'),
        ('in', 'Terminé')
    ], default='out')
    observation = models.CharField(blank=True, null=True, max_length=256)

    # Association avec le modèle User (Celui qui enregistre la fonte)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reintegrer_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reintegrer_par')
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    
    @property
    def numero(self):
        if self.id:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            return f"CTB{str(self.id).zfill(4)}-{last_two_digits_of_year}"
        return "-"
    
    def __str__(self):
        return self.numero if self.numero else "-"

class Vente(models.Model):
    date_sortie = models.DateTimeField(auto_now_add=True, editable=False)
    date_retour = models.DateTimeField(null=True, blank=True)
    etat = models.CharField(max_length=10, choices=[
        ('out', 'En cours'),
        ('in', 'Terminé')
    ], default='out')
    observation = models.CharField(blank=True, null=True, max_length=256)

    # Association avec le modèle User (Celui creer la vente)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    
    @property
    def numero(self):
        if self.id:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            return f"CTB{str(self.id).zfill(4)}-{last_two_digits_of_year}"
        return "-"
    
    def __str__(self):
        return self.numero if self.numero else "-"
    
class Lingot(models.Model):
    id = models.AutoField(primary_key=True)
    poids_brut = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4,)
    poids_immerge = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    ecart = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    densite = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=10)
    titre = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    or_fin = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    date_reception = models.DateTimeField(null=True, blank=True)
    observation = models.TextField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    numero = models.CharField(max_length=16, blank=True, null=True, unique=True)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)

    fonte = models.ForeignKey(Fonte, on_delete=models.SET_NULL, null=True, blank=True)
    control_bumigeb = models.ForeignKey(ControlBUMIGEB, on_delete=models.SET_NULL, null=True, blank=True)

    fichecontrol = models.ForeignKey(Fichecontrol, on_delete=models.SET_NULL, null=True, blank=True)
    archived = models.BooleanField(default=False)
    is_fonte = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Lingots"
        ordering = ['created']

    
    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user
        

        if not self.numero:
            if not self.id:
                super(Lingot, self).save(*args, **kwargs)
            if not self.created:
                year = timezone.now().year
            else:
                year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            self.numero = f"L{str(self.id).zfill(5)}-{last_two_digits_of_year}"
        
        super(Lingot, self).save(*args, **kwargs)

    def __str__(self):
        return self.numero if self.numero else '-'

class LingotFondus(models.Model):
    fonte =  models.OneToOneField(Fonte, on_delete=models.CASCADE)
    lingot =  models.OneToOneField(Lingot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def clean(self):
        # Ensure that model_b.is_fonte is True
        if self.lingot and not self.lingot.is_fonte:
            raise ValidationError("ModelB must have is_fonte set to True.")
    
    def __str__(self):
        return f"LFT-{self.id}" if self.id else "-"

    
class Pesee(models.Model):
    poids_brut = models.DecimalField(max_digits=10, decimal_places=4)
    poids_immerge = models.DecimalField(max_digits=10, decimal_places=4)
    observation = models.CharField(blank=True, null=True, max_length=256)
    date_pesee = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    lingot = models.ForeignKey('Lingot', on_delete=models.CASCADE)  # Chaque pesée est liée à un lingot

    # Les caractristique du lingot est la moyenne des resultat pour chaque pesé
    # Indique si ce pesé est utilisé dans le calcul de caracteristique du lingot
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Pesees"
        ordering = ['created']

    def get_numero_pesee(self):
        return 1

    def __str__(self):
        pesees_precedentes = Pesee.objects.filter(lingot=self.lingot, created__lte=self.created).order_by('created').order_by('id')
        for i, obj in enumerate(pesees_precedentes):
            if obj.id == self.pk:
                position = i+1
            else:
                position = 1
        if position:
            return f"Pesee #{position}{'(actif)' if self.actif else ''}"
        else:
            "Pesee #-"

    # Ajout de la méthode pour le champ virtuel "Ecart"
    @property
    def numero(self):
        if self.lingot is not None and self.pk:
            return f"Pesee #{self.get_numero_pesee()}{' (actif)' if self.actif else ''}"
        else:
            return "-"

    # Ajout de la méthode pour le champ virtuel "Ecart"
    @property
    def ecart(self):
        return self.poids_brut - self.poids_immerge

    @property
    def densite(self):
        return 1 if (self.poids_brut == self.poids_immerge) else self.poids_brut / (self.poids_brut - self.poids_immerge)

    @property
    def titre(self):
        return Decimal(round(((self.densite - Decimal(10.6))/self.densite)*(Decimal(19.3)/(Decimal(19.3)-Decimal(10.6)))*24, 4))
        

    @property
    def or_fin(self):
        return Decimal(round(self.titre * self.poids_brut/24, 4))

    def save(self, *args, **kwargs):
        if self.pk:  # Check if this is not the initial save
            self.date_pesee = self.modified
        super(Pesee, self).save(*args, **kwargs)

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
    archived = models.BooleanField(default=False)


    # Generer un numero de Facture
    def generate_numero_facture(self):
        last_two_digits_of_year = str(self.created.year)[-2:]
        return f"{str(self.id).zfill(4)}-{last_two_digits_of_year}"
    
    # Surcharge de la méthode save pour appeler la fonction generate_numero_fiche_control
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         # Si la fiche n'a pas encore d'ID, il n'est pas encore enregistré dans la base de données
    #         temp_facture = Factures.objects.create()  # Créer un Lingot non enregistré pour obtenir un ID
    #         self.id = temp_facture.id  # Assigner l'ID généré a la fiche actuel
    #         self.generate_numero_facture()

    #     super().save(*args, **kwargs)
    
    # stocker le numéro de la facture
    # numero_facture = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Factures"

    def __str__(self):
        return self.generate_numero_facture()




class MouvementLingot(models.Model):
    type_substance = models.ForeignKey(TypeSubstance, on_delete=models.CASCADE) 
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
    archived = models.BooleanField(default=False)

    
    class Meta:
        verbose_name_plural = "Mouvements Lingots"

class DirectionLingot(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type_substance = models.ForeignKey(TypeSubstance, on_delete=models.CASCADE, blank=True, null=True)
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
    marge = models.DecimalField(max_digits=10, decimal_places=4)
    marge_auto = models.BooleanField(default=True)
    cours = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    cours_auto = models.BooleanField(default=True)
    globale = models.BooleanField(default=False)
    type_fournisseur = models.ForeignKey(TypeFournisseur,  on_delete=models.CASCADE, null=True, blank=True)
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
    readonly = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Modes de payements"

    def __str__(self):
        return self.libelle

class PieceJointe(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    file = models.FileField(upload_to='media/attachments/commercial/')
    description = models.TextField()

    def __str__(self):
        return self.file.name
    
class Payement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Lien vers la fiche de contrôle
    fichetarification = models.ForeignKey(FicheTarification, on_delete=models.SET_NULL, null=True, blank=True)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)

    montant = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    reference = models.CharField(max_length=16, blank=True, null=True, unique=True)
    archived = models.BooleanField(default=False)


    CHOICES = [
        ('in', 'ENTREE'),
        ('out', 'SORTIE'),
    ]

    piecejointe = models.FileField(upload_to='uploads/commercial', null=True, unique=True)

    direction = models.CharField(max_length=6, choices=CHOICES, default='ENTREE')

    observation = models.TextField(blank=True, null=True,)
    archived = models.BooleanField(default=False)
    confirme = models.BooleanField(default=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Transactions"
    

    def __str__(self):
        if self.id:
            year = self.created.year
            last_two_digits_of_year = str(year)[-2:]
            return f"PY{str(self.id).zfill(5)}-{last_two_digits_of_year}"
        else:
            return "_"

@receiver(pre_save, sender=FicheTarification)
def fichetarification_pre_save(sender, instance, **kwargs):
    # Your pre-save logic here
    print(f"Performing pre-save actions for {instance}")

@receiver(pre_save, sender=Pesee)
def ensure_single_enabled_pesee(sender, instance, **kwargs):
    if instance.actif:
        # Disable all other Pricing objects related to the same Lingot
        Pesee.objects.filter(lingot=instance.lingot, actif=True).exclude(pk=instance.pk).update(actif=False)