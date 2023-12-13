from decimal import Decimal
from django import forms
from django.db.models.signals import post_save, post_delete
from django.db import models
from datetime import date

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from django.forms import ValidationError
from django.urls import reverse

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

from django.db.models import Q

from django_countries.fields import CountryField

from django.template.defaultfilters import escape
from decimal import Decimal, ROUND_DOWN

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
    prenom = models.CharField(max_length=60)
    nom = models.CharField(max_length=60)
    type_fournisseur = models.ForeignKey(TypeFournisseur,  on_delete=models.CASCADE, null=False, blank=False)
    numero_carte = models.CharField(blank=True, null=True, max_length=15)
    email = models.EmailField(blank=True, null=True, max_length=60)
    pays = CountryField(default='BF')
    telephone = models.CharField(blank=True, null=True, max_length=15)
    document_identite = models.FileField(upload_to='uploads/commercial/fournisseur/', null=True, blank=True)
    reference_document_identite = models.CharField(max_length=16, blank=True, null=True)
    autre_document = models.FileField(upload_to='uploads/commercial/fournisseur', null=True, blank=True)
    description = models.TextField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Fournisseurs"

    def __str__(self):
        return self.prenom + ' ' + self.nom

class RepresentantFournisseur(models.Model):
    prenom = models.CharField(max_length=60)
    nom = models.CharField(max_length=60)
    email = models.EmailField(blank=True, null=True, max_length=60)
    telephone = models.CharField(blank=True, null=True, max_length=15)
    description = models.TextField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    Fournisseur = models.ForeignKey(Fournisseur, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Representants fournisseurs"

    def __str__(self):
        return self.prenom + ' ' + self.nom


class TypeDeClient(models.Model):
    libelle = models.CharField(max_length=60)
    description = models.CharField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Types clients"

    def __str__(self):
        return self.libelle if self.libelle is not None else "N/A"
    
class Telephone(models.Model):
    nom = models.CharField(max_length=60)
    tel = models.CharField(null=True, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Telephones"

    def __str__(self):
        return self.numero if self.numero is not None else self.tel


class Client(models.Model):
    societe = models.CharField(max_length=60)
    nom = models.CharField(blank=True, null=True, max_length=60)
    type_de_client = models.ForeignKey(TypeDeClient,  on_delete=models.CASCADE, null=False, blank=False)
    reference_societe = models.CharField(blank=True, null=True, max_length=1024)
    email = models.EmailField(blank=True, null=True, max_length=60)
    telephone = models.CharField(blank=True, null=True, max_length=15)
    addresse = models.CharField(blank=True, null=True, max_length=120)
    pays = CountryField(default='BF')
    document_identite = models.FileField(upload_to='uploads/commercial/client/', null=True, blank=True)
    reference_document_identite = models.CharField(max_length=16, blank=True, null=True)
    autre_document = models.FileField(upload_to='uploads/commercial/client', null=True, blank=True)
    description = models.TextField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.societe if self.societe else '-'


class SMS(models.Model):
    TYPES_MESSAGE = [
        ('f', 'Fournisseur'),
        ('c', 'Client'),
    ]
    message = models.TextField(max_length=256)
    libelle = models.CharField(null=True, max_length=60, blank=True)
    fournisseurs = models.ManyToManyField(Fournisseur, blank=True)
    clients = models.ManyToManyField(Client, blank=True)
    type_de_message = models.CharField(max_length=20, choices=TYPES_MESSAGE, default='f')
    list_non_envoye = models.TextField(null=True, max_length=60, blank=True)
    envoye = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.libelle if self.libelle else self.message
    
class SMSFournisseurManager(models.Manager):
    def get_queryset(self):
        transfered_queryset = super().get_queryset().filter(type_de_message='f')
        return transfered_queryset
    
class SMSFournisseur(SMS):
    objects = SMSFournisseurManager()
    
    class Meta:
        proxy = True
        verbose_name_plural = "SMS Fournisseurs"

class SMSClientManager(models.Manager):
    def get_queryset(self):
        transfered_queryset = super().get_queryset().filter(type_de_message='c')
        return transfered_queryset
    
class SMSClient(SMS):
    objects = SMSClientManager()
    
    class Meta:
        proxy = True
        verbose_name_plural = "SMS Clients"
        

class TypeSubstance(models.Model):
    libelle = models.CharField(max_length=60, unique=True, blank=True, null=True)
    symbole = models.CharField(max_length=10, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Types Substances"

    def __str__(self):
        return self.symbole

class EmplacementLingot(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    TYPES_EMPLACEMENT = [
        ('in', 'Interne'),
        ('out', 'Externe'),
    ]
    type_emplacement = models.CharField(max_length=20, choices=TYPES_EMPLACEMENT, default='out')
    pays = CountryField(default='BF')
    description = models.TextField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = "Emplacements Lingots"

    def __str__(self):
        name = self.nom if self.nom else '-' 
        country = self.pays.name if self.pays else '-'
        return f'{name} ({country})'
    
       

class Fichecontrol(models.Model):
    # id = models.AutoField(primary_key=True)
    # Association avec le modèle User (Celui qui enregistre le lingot)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # fiche_tarification = models.ForeignKey(FicheTarification, on_delete=models.SET_NULL, null=True, blank=True)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True)
    date_control = models.DateTimeField()
    document_signe = models.FileField(upload_to='uploads/commercial/fichecontrol/', null=True, blank=True)
    observation = models.CharField(max_length=256, null=True, blank=True)

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
    cours = models.DecimalField(max_digits=20, decimal_places=4, null=True, default=0)
    marge = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    date_tarification = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)

    fichecontrol = models.OneToOneField(Fichecontrol, on_delete=models.SET_NULL, null=True, blank=True)
    representant = models.ForeignKey(RepresentantFournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    observation = models.CharField(max_length=256, null=True, blank=True)
    document_signe = models.FileField(upload_to='uploads/commercial/fichecontrol/', null=True, blank=True)

    numero = models.CharField(max_length=16, blank=True, null=True, unique=True)

    transferer = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    @property
    def price_anemas(self):
        marge = Decimal(0) if self.marge is None else self.marge
        cours = self.cours

        if cours is not None:
            price = Decimal(cours) / 24 - marge
            return Decimal(round(price, 4)).quantize(Decimal("0.0000"), rounding=ROUND_DOWN)
        else:
            return None

    @property
    def total_price(self):
        total_product = sum(lingot.price for lingot in self.fichecontrol.lingot_set.all())
        return Decimal(round(total_product,4))

    @property
    def reste_a_payer(self):
        ps = Payement.objects.filter(fichetarification=self)
        val = self.total_price - sum(p.montant for p in ps)
        return Decimal(round(val,0))
    
    @property
    def poids_kilograms(self):
        total_poids = sum(lingot.or_fin for lingot in self.fichecontrol.lingot_set.all())
        return Decimal(round(total_poids,0))

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
        transfered_queryset = super().get_queryset().filter(transferer=True)
        return transfered_queryset
    
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
    numero_lot = models.CharField(blank=True, null=True, max_length=20, unique=True)
    observation = models.TextField(blank=True, null=True, max_length=256)

    # Association avec le modèle User (Celui qui enregistre la fonte)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reintegrer_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reintegrer_par')
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user
        
        super(ControlBUMIGEB, self).save(*args, **kwargs)  # Save the object to get the id

        if not self.numero_lot:
            if not self.created:
                year = timezone.now().year
            else:
                year = self.created.year

            last_two_digits_of_year = str(year)[-2:]
            self.numero_lot = f"CTB{str(self.id).zfill(4)}-{last_two_digits_of_year}"

            # Call self.save without update_fields for the second time
            self.save(update_fields=['numero_lot'])
    
    def __str__(self):
        return self.numero_lot if self.numero_lot else "-"
TYPE_CONTROL = [
        ('bumigeb', 'Control BUMIGEB'),
        ('affinage', 'Rapport affinage'),
        ('sonasp', 'Control SONASP'),
    ]

TYPES_FACTURE = [
        ('proforma', 'Facture Proforma'),
        ('definitive', 'Facture definitive'),
        ('autre', 'Autre'),
    ]

class Vente(models.Model):
    # id = models.AutoField(primary_key=True)
    # Association avec le modèle User (Celui qui enregistre le lingot)
    vendre_selon = models.CharField(max_length=20, choices=TYPE_CONTROL, default='bumigeb')
    objet = models.TextField(null=True, blank=True)
    date_conclusion = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    numero = models.CharField(max_length=16, blank=True, null=True, unique=True)

    control_choisi = models.ForeignKey('Control', on_delete=models.SET_NULL, null=True, blank=True, related_name='control_choisi')
    observation = models.TextField(null=True, blank=True)

    conclu = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Ventes"

        
    def __str__(self):
        return self.numero if self.numero else '-'
    
    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user
        
        super(Vente, self).save(*args, **kwargs)  # Save the object to get the id

        if not self.numero:
            if not self.created:
                year = timezone.now().year
            else:
                year = self.created.year

            last_two_digits_of_year = str(year)[-2:]
            self.numero = f"VNT{str(self.id).zfill(4)}-{last_two_digits_of_year}"

            # Call self.save without update_fields for the second time
            self.save(update_fields=['numero'])



class CustomFileInput(forms.ClearableFileInput):
    def get_template_substitution_values(self, value):
        # Customize the display text of the link
        return {
            'initial': '%(initial_text)s <a href="%s" target="_blank">%s</a>' % (value.url, self.numero),
        }
class Facture(models.Model):
    numero = models.CharField(max_length=16, blank=True, null=True, unique=True)
    cours_du_dollar = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True, default=0, validators=[MinValueValidator(Decimal('0'))])
    cours_en_euro = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True, validators=[MinValueValidator(Decimal('0'))])
    reduction_commercial = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True, validators=[MinValueValidator(Decimal('0'))])
    pourcentage_tva = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True, validators=[MinValueValidator(Decimal('0'))])
    date = models.DateTimeField()
    type_de_facture=models.CharField(max_length=20, choices=TYPES_FACTURE, default='proforma', editable=False)
    vente = models.ForeignKey(Vente, null=True, on_delete=models.CASCADE)
    facture_signe = models.FileField(upload_to='uploads/commercial/vente/facture', null=True, blank=True)
    observation = models.TextField(blank=True, null=True, max_length=256)

    # Association avec le modèle User (Celui creer la vente)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

     # If you want to customize the display text of the link
    def get_your_file_display_text(self):
        # Customize the display text as needed
        return self.numero

    class Meta:
        verbose_name_plural = "Factures"

    def __str__(self):
        return self.numero if self.numero else '-'

    def montant(self):
        return 78000

    class Meta:
        verbose_name_plural = "Facture proforma"
        unique_together = ('vente', 'type_de_facture')
    
    def __str__(self):
        return self.numero if self.numero else '-'

    
    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user
        
        super(Facture, self).save(*args, **kwargs)  # Save the object to get the id

        if not self.numero:
            if not self.created:
                year = timezone.now().year
            else:
                year = self.created.year
            
            def switch_case(case_value):
                match case_value:
                    case 'proforma':
                        return "FAC-PRO"
                    case 'definitive':
                        return "FAC-DEF"
                    case _:
                        return "FAC"

            last_two_digits_of_year = str(year)[-2:]
            self.numero = f"{switch_case(self.type_de_facture)}{str(self.id).zfill(4)}-{last_two_digits_of_year}"

            # Call self.save without update_fields for the second time
            self.save(update_fields=['numero'])

class FactureProformaManager(models.Manager):
    def get_queryset(self):
        prix_definitive = super().get_queryset().filter(type_de_facture='proforma')
        return prix_definitive
    
class FactureProforma(Facture):
    objects = FactureProformaManager()
    class Meta:
        proxy = True
        verbose_name_plural = "Factures Proforma"

class FactureDefinitiveManager(models.Manager):
    def get_queryset(self):
        prix_definitive = super().get_queryset().filter(type_de_facture='definitive')
        return prix_definitive
    
class FactureDefinitive(Facture):
    objects = FactureDefinitiveManager()
    class Meta:
        proxy = True
        verbose_name_plural = "Factures Defintives"


class VentesConluManager(models.Manager):
    def get_queryset(self):
        concluded_queryset = super().get_queryset().filter(conclu=True)
        return concluded_queryset
    
class VentesConclu(Vente):
    objects = VentesConluManager()
    
    class Meta:
        proxy = True
        verbose_name_plural = "Ventes conclu"
    
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

    numero = models.CharField(max_length=20, blank=True, null=True, unique=True)

    # Association avec le modèle User (Celui qui enregistre le lingot)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True)

    fonte = models.ForeignKey(Fonte, on_delete=models.SET_NULL, null=True, blank=True)
    control_bumigeb = models.ForeignKey(ControlBUMIGEB, on_delete=models.SET_NULL, null=True, blank=True)

    numero_bumigeb = models.CharField(max_length=20, blank=True, null=True, unique=True)
    poids_brut_bumigeb = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4,)
    poids_immerge_bumigeb = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    ecart_bumigeb = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    or_fin_bumigeb = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    densite_bumigeb = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=10)
    titre_bumigeb = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    observation_bumigeb = models.TextField(blank=True, null=True, max_length=256)

    fichecontrol = models.ForeignKey(Fichecontrol, on_delete=models.SET_NULL, null=True)
    vente = models.ForeignKey(Vente, on_delete=models.SET_NULL, null=True, blank=True)
    
    archived = models.BooleanField(default=False)
    is_fonte = models.BooleanField(default=False)
    avendre = models.BooleanField(default=False)

    @property
    def price(self):
        price = 0
        if self.fichecontrol is not None:
            ft = self.fichecontrol.fichetarification
            if ft is not None:
                prix_anemas = ft.price_anemas
                return Decimal(round(Decimal(self.titre) * Decimal(self.or_fin) * Decimal(prix_anemas)))
        return Decimal(price)
        
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

class TransferedLingotManager(models.Manager):
    def get_queryset(self):
        transfered_lingot_ids = MouvementLingot.objects.values_list('lingots__id', flat=True)
        transfered_queryset = super().get_queryset().filter(id__in=transfered_lingot_ids)
        return transfered_queryset
    
class TransferedLingot(Lingot):
    objects = TransferedLingotManager()
    
    class Meta:
        proxy = True
        verbose_name_plural = "Lingots transférés"

class StructureDeControl(models.Model):
    societe = models.CharField(max_length=120)
    reference_societe = models.CharField(blank=True, null=True, max_length=1024)
    email = models.EmailField(blank=True, null=True, max_length=60)
    telephone = models.CharField(blank=True, null=True, max_length=15)
    addresse = models.CharField(blank=True, null=True, max_length=120)
    pays = CountryField(default='BF')
    description = models.TextField(blank=True, null=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Structures de control"

    def __str__(self):
        return self.nom if self.nom else '-'

class Control(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    type_de_control = models.CharField(max_length=20, choices=TYPE_CONTROL, default='bumigeb')
    control_client = models.BooleanField(blank=True, null=True, default=True)
    structure_de_control = models.ForeignKey(StructureDeControl, blank=True, null=True, on_delete=models.CASCADE)
    date_control = models.DateTimeField()
    vente = models.ForeignKey(Vente, blank=True, null=True, on_delete=models.CASCADE)
    observation = models.TextField(blank=True, null=True, max_length=256)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    document_signe = models.FileField(upload_to='uploads/commercial/control/', null=True, blank=True)

    numero_de_control = models.CharField(blank=True, null=True, max_length=20, unique=True)
    

    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user
        
        super(Control, self).save(*args, **kwargs)  # Save the object to get the id

        if not self.numero_de_control:
            if not self.created:
                year = timezone.now().year
            else:
                year = self.created.year

            last_two_digits_of_year = str(year)[-2:]
            def switch_case(case_value):
                match case_value:
                    case 'sonasp':
                        return "CTLS"
                    case 'affinage':
                        return "RAFF"
                    case 'bumigeb':
                        return "CTLB"
                    case _:
                        return "CTLG"
            self.numero_de_control = f"{switch_case(self.type_de_control)}{str(self.id).zfill(4)}-{last_two_digits_of_year}"

            # Call self.save without update_fields for the second time
            self.save(update_fields=['numero_de_control'])
    def clean(self):
        if self.type_de_control == "affinage" and not self.control_client and not self.structure_de_control:
            raise ValidationError("Vous dever definir la structure d'affinage ou preciser qu'il s'agit du client de la vente.")
    
    def __str__(self):
        return self.numero_de_control if self.numero_de_control else "-"

    class Meta:
        verbose_name_plural = "Controls"

class RapportAffinageManager(models.Manager):
    def get_queryset(self):
        transfered_queryset = super().get_queryset().filter(type_de_control='affinage')
        return transfered_queryset
    
class RapportAffinage(Control):
    objects = RapportAffinageManager()
    
    class Meta:
        proxy = True
        verbose_name_plural = "Rapports d'affinages"
    
class ControlLingot(models.Model):
    numero = models.CharField(max_length=16, blank=True, null=True, unique=True)
    lingot = models.ForeignKey('Lingot', blank=True, null=True, on_delete=models.CASCADE)
    type_de_control = models.CharField(max_length=20, choices=TYPE_CONTROL, default='bumigeb')
    control = models.ForeignKey(Control, blank=True, null=True, on_delete=models.CASCADE)
    observation = models.TextField(blank=True, null=True, max_length=256)
    date_control = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    numero_lingot_control = models.CharField(max_length=16, blank=True, null=True, unique=True)
    poids_brut = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4,)
    poids_immerge = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    ecart = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    or_fin = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    densite = models.DecimalField(blank=True, null=True, max_digits=25, decimal_places=10)
    titre_carat = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    observation = models.TextField(blank=True, null=True, max_length=256)


    class Meta:
        verbose_name_plural = "Control Lingots"
        unique_together = [
            ('control', 'lingot'),
            ('lingot', 'type_de_control'),
        ]

    def __str__(self):
        return self.numero if self.numero else '-'
    
    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user
        
        super(ControlLingot, self).save(*args, **kwargs)  # Save the object to get the id

        if not self.numero:
            if not self.created:
                year = timezone.now().year
            else:
                year = self.created.year

            last_two_digits_of_year = str(year)[-2:]
            self.numero = f"CTRL{str(self.id).zfill(4)}-{last_two_digits_of_year}"

            # Call self.save without update_fields for the second time
            self.save(update_fields=['numero'])


class PourcentageSubstanceLingot(models.Model):
    lingot = models.ForeignKey(Lingot, on_delete=models.CASCADE)
    type_substance = models.ForeignKey(TypeSubstance, on_delete=models.CASCADE)
    pourcentage = models.DecimalField(max_digits=7, decimal_places=4, default=0, validators=[MinValueValidator(Decimal('0'))])
    reste = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('lingot', 'type_substance')
        verbose_name = 'Pourcentage des substance'
        verbose_name_plural = 'Pourcentage des substances'
    
    def __str__(self):
        if not self.type_substance:
            prefix = '-'
        else:
            prefix = str(self.type_substance)
        return prefix + ' ' + str(self.pourcentage) + '%'
 
class PourcentageSubstanceControlLingot(models.Model):
    control_lingot = models.ForeignKey(ControlLingot, on_delete=models.CASCADE)
    lingot = models.ForeignKey(Lingot, on_delete=models.CASCADE)
    type_de_substance = models.ForeignKey(TypeSubstance, on_delete=models.CASCADE)
    pourcentage = models.DecimalField(max_digits=7, decimal_places=4, default=0, validators=[MinValueValidator(Decimal('0'))])
    poids = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=4, default=0)
    reste = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('lingot', 'type_de_substance')
        verbose_name = 'Pourcentage des substance'
        verbose_name_plural = 'Pourcentage des substances'
    
    def __str__(self):
        if not self.type_de_substance:
            prefix = '-'
        else:
            prefix = str(self.type_de_substance)
        return prefix + ' ' + str(self.pourcentage) + '%'
    
class PrixDesSubstancesFactureProformaManager(models.Manager):
    def get_queryset(self):
        prix_proforma = super().get_queryset()
        return prix_proforma
    
class PrixDesSubstancesFactureProforma(Lingot):
    objects = PrixDesSubstancesFactureProformaManager()
    
    class Meta:
        proxy = True

class PrixDesSubstancesFactureDefinitiveManager(models.Manager):
    def get_queryset(self):
        prix_definitive = super().get_queryset()
        return prix_definitive
    
class PrixDesSubstancesFactureDefinitive(Lingot):
    objects = PrixDesSubstancesFactureDefinitiveManager()
    class Meta:
        proxy = True
        verbose_name_plural = "PRIX DES SUBSTANCES"

class PrixDesSubstances(models.Model):
    type_de_substance = models.ForeignKey(TypeSubstance, on_delete=models.CASCADE)
    poids = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=4, default=0)
    cours_de_substance = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, default=0)
    reduction_commercial = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True, default=0)
    prix = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, default=0)
    observation = models.TextField(blank=True, null=True, max_length=256)
    facture = models.ForeignKey(Facture, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "PRIX DES SUBSTANCES"
        unique_together = [
            ('facture', 'type_de_substance')
        ]
    
    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user
        if self.reduction_commercial and self.reduction_commercial > 0:
            factor = self.cours_de_substance - self.reduction_commercial
        else:
            factor = self.cours_de_substance
        self.prix = factor * self.poids
        super(PrixDesSubstances, self).save(*args, **kwargs)  # Save the object to get the id

    
    def __str__(self):
        if self.prix and self.type_de_substance:
            return f'{self.type_de_substance.symbole} ({self.prix} FCFA)'
        else:
            return '-'
    
    
 
class PourcentageSubstanceControlBUMIGEB(models.Model):
    control_bumigeb = models.ForeignKey(ControlBUMIGEB, on_delete=models.CASCADE)
    type_substance = models.ForeignKey(TypeSubstance, on_delete=models.CASCADE)
    pourcentage = models.DecimalField(max_digits=7, decimal_places=4)
    reste = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('control_bumigeb', 'type_substance')
        verbose_name = 'Pourcentage des substance'
        verbose_name_plural = 'Pourcentage des substances'
    
    def __str__(self):
        if not self.type_substance:
            prefix = '-'
        else:
            prefix = str(self.type_substance)
        return prefix + ' ' + str(self.pourcentage) + '%'

class PourcentageSubstanceRapportAffinage(models.Model):
    rapport_affinage = models.ForeignKey(RapportAffinage, on_delete=models.CASCADE)
    type_substance = models.ForeignKey(TypeSubstance, on_delete=models.CASCADE)
    pourcentage = models.DecimalField(max_digits=7, decimal_places=4)
    reste = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('rapport_affinage', 'type_substance')
        verbose_name = 'Pourcentage des substance'
        verbose_name_plural = 'Pourcentage des substances'
    
    def __str__(self):
        if not self.type_substance:
            prefix = '-'
        else:
            prefix = str(self.type_substance)
        return prefix + ' ' + str(self.pourcentage) + '%'

class LingotsDisponiblesPourVenteManager(models.Manager):
    def get_queryset(self):
        # Choisir les lingots qui ne sont pas encore associé a une vente
        # Et ayant fait l'objet d'un control BUMIGEB et qui est revenu
        # Ou ayant explicitement disigné comme disponible pour la vente
        from commercial.querysets import vente_queryset
        return vente_queryset(super().get_queryset())
    
class LingotsDisponiblesPourVente(Lingot):
    objects = LingotsDisponiblesPourVenteManager()
    
    class Meta:
        proxy = True
        verbose_name_plural = "Lingots disponibles vente"

class LingotFondus(models.Model):
    fonte =  models.OneToOneField(Fonte, on_delete=models.CASCADE)
    lingot =  models.OneToOneField(Lingot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def clean(self):
        # Ensure that model_b.is_fonte is True
        if self.lingot and not self.lingot.is_fonte:
            raise ValidationError("Internal system error!")
    
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
        if self is not None and self.lingot is not None and self.id is not None:
            pesees_precedentes = Pesee.objects.filter(lingot=self.lingot, id__lt=self.id)
            position = len(pesees_precedentes) + 1
            str_val = f"Pesee #{position}{'(actif)' if self.actif else ''}"
        return str_val

    def __str__(self):
        str_val = "Pesee #"
        if self is not None and self.lingot is not None and self.id is not None:
            pesees_precedentes = Pesee.objects.filter(lingot=self.lingot, id__lt=self.id)
            position = len(pesees_precedentes) + 1
            str_val = f"Pesee #{position}{'(actif)' if self.actif else ''}"
        return str_val

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
        was_active = self.actif
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


class MouvementLingot(models.Model):
    destination = models.ForeignKey(EmplacementLingot, on_delete=models.CASCADE)
    ETAT_CHOICES = [
        ('start', 'En cours'),
        ('end', 'Terminé'),
    ]
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='start')
    numero_mouvement = models.CharField(blank=True, null=True, max_length=20, unique=True)
    date_deplacement = models.DateTimeField(auto_now_add=True)
    date_arrive = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    archived = models.BooleanField(blank=True, null=True, default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    lingots = models.ManyToManyField(Lingot, through='MouvementLingotLingot')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Mouvements Lingots"
    
    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user
        
        super(MouvementLingot, self).save(*args, **kwargs)  # Save the object to get the id

        # Mark old movements as moved to new localtions
        MouvementLingotLingot.objects.filter(lingot__in=self.lingots.all())\
            .exclude(mouvement_lingot=self).update(moved=True)

        if not self.numero_mouvement:
            if not self.created:
                year = timezone.now().year
            else:
                year = self.created.year

            last_two_digits_of_year = str(year)[-2:]
            self.numero_mouvement = f"MOV{str(self.id).zfill(4)}-{last_two_digits_of_year}"

            # Call self.save without update_fields for the second time
            self.save(update_fields=['numero_mouvement'])
    
    def __str__(self):
        return self.numero_mouvement if self.numero_mouvement else "-"

class MouvementLingotLingot(models.Model):
    mouvement_lingot =  models.ForeignKey(MouvementLingot, on_delete=models.CASCADE)
    lingot =  models.ForeignKey(Lingot, on_delete=models.CASCADE)
    moved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"({self.mouvement_lingot.pk}<->{self.lingot.pk})"
    
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

    file = models.FileField(upload_to='uploads/commercial/')
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
    observation = models.TextField(blank=True, null=True, max_length=256)

    montant = models.DecimalField(max_digits=20, decimal_places=4, validators=[MinValueValidator(0)])
    archived = models.BooleanField(default=False)


    CHOICES = [
        ('in', 'ENTREE'),
        ('out', 'SORTIE'),
    ]

    mode_payement = models.ForeignKey(ModePayement, on_delete=models.SET_NULL, null=True, blank=True)
    reference_payement = models.CharField(max_length=16, null=True, unique=True)
    document_payement = models.FileField(upload_to='uploads/commercial/achat/doc_payement', null=True)
    recu_payement = models.FileField(upload_to='uploads/commercial/commercial/achat/recu', null=True, blank=True)
    document_identite = models.FileField(upload_to='uploads/commercial/commercial/achat/doc_identites', null=True)
    autre_document = models.FileField(upload_to='uploads/commercial/achat/autres', null=True, blank=True)
    reference_document_identite = models.CharField(max_length=16, null=True)

    direction = models.CharField(max_length=6, choices=CHOICES, default='ENTREE')

    observation = models.TextField(blank=True, null=True,)
    numero = models.CharField(blank=True, null=True, max_length=20, unique=True)
    archived = models.BooleanField(default=False)
    confirme = models.BooleanField(default=True)
    actif = models.BooleanField(default=True)

    @property
    def reste_a_payer(self):
        ps = Payement.objects.filter(fichetarification=self.fichetarification, id__lt=self.id)
        substract = 0
        if len(ps) > 0:
            substract = sum(p.montant for p in ps)
        print("len(ps):", ps)
        val = self.fichetarification.total_price - substract - self.montant
        return Decimal(round(val,0))

    class Meta:
        verbose_name_plural = "Transactions"
    
    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created (not updated)
            user = kwargs.pop('user', None)  # Get the user from kwargs
            if user:
                self.user = user
        
        super(Payement, self).save(*args, **kwargs)  # Save the object to get the id

        if not self.numero:
            if not self.created:
                year = timezone.now().year
            else:
                year = self.created.year

            last_two_digits_of_year = str(year)[-2:]
            self.numero = f"PY{str(self.id).zfill(5)}-{last_two_digits_of_year}"

            # Call self.save without update_fields for the second time
            self.save(update_fields=['numero'])
    
    def __str__(self):
        return self.numero if self.numero else "-"

@receiver(pre_save, sender=FicheTarification)
def fichetarification_pre_save(sender, instance, **kwargs):
    # Your pre-save logic here
    pass

@receiver(pre_save, sender=Pesee)
def ensure_single_enabled_pesee(sender, instance, **kwargs):
    if instance.actif:
        # Disable all other Pricing objects related to the same Lingot
        Pesee.objects.filter(lingot=instance.lingot, actif=True).exclude(pk=instance.pk).update(actif=False)