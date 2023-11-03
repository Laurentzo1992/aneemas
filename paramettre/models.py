from django.db import models
from django.core.exceptions import ValidationError


class Typaccidents(models.Model):
    libelle = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

   
    class Meta:
        verbose_name = "Typaccidents"
        verbose_name_plural = "Type d'accident"
        
    def __str__(self):
        return self.libelle


class Typautorisations(models.Model):
    libelle = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    class Meta:
        verbose_name = "Typautorisations"
        verbose_name_plural = "Type d'autorisation"
        
    def __str__(self):
        return self.libelle


class Typdemandeurs(models.Model):
    libelle = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    class Meta:
        verbose_name = "Typdemandeurs"
        verbose_name_plural = "Type demandeur"
        
    def __str__(self):
        return self.libelle


class Typenatureminerais(models.Model):
    libelle_type_nature_minerais = models.CharField(max_length=254, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    class Meta:
        verbose_name = "Typenatureminerais"
        verbose_name_plural = "Nature du minerai"
        
    def __str__(self):
        return self.libelle_type_nature_minerais


class Typenatureterrains(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

  

    class Meta:
        verbose_name = "Typenatureterrains"
        verbose_name_plural = "Nature terrain"
        
    def __str__(self):
        return self.libelle
    
    

class Typeorganisations(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

   
    class Meta:
        verbose_name = "Typeorganisations"
        verbose_name_plural = "Type d'organisation"
        
    def __str__(self):
        return self.libelle

class Typeproduitchimiques(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    class Meta:
        verbose_name = "Typeproduitchimiques"
        verbose_name_plural = "Type de produit chimique"
        
    def __str__(self):
        return self.libelle


class Typequipements(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    class Meta:
        verbose_name = "Typequipements"
        verbose_name_plural = "Type d'equipement"
        
    def __str__(self):
        return self.libelle



class Typesites(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

   
    class Meta:
        verbose_name = "Typesites"
        verbose_name_plural = "Type de site"
        
    def __str__(self):
        return self.libelle

class Typetaterrains(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    class Meta:
        verbose_name = "Typetaterrains"
        verbose_name_plural = "Type de terrain"
        
    def __str__(self):
        return self.libelle
    
    

class Regions(models.Model):
    numero = models.CharField(max_length=1000, blank=True, null=True)
    nomreg = models.CharField(max_length=1000, blank=True, null=True)
    cheflieu = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    
    class Meta:
        verbose_name = "Regions"
        verbose_name_plural = "Region"
        
    def __str__(self):
        return self.nomreg

    


class Provinces(models.Model):
    numero = models.CharField(max_length=1000, blank=True, null=True)
    nomprov = models.CharField(max_length=500, blank=True, null=True)
    region_id = models.ForeignKey(Regions, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    class Meta:
        verbose_name = "Provinces"
        verbose_name_plural = "Province"
        
    def __str__(self):
        return self.nomprov

class Statutsites(models.Model):
    libelle = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

   
    class Meta:
        verbose_name = "Statut du sites"
        verbose_name_plural = "Statut du site"
        
    def __str__(self):
        return self.libelle
    


class Typecarte(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    class Meta:
        verbose_name = "Type de carte"
        verbose_name_plural = "Type de carte"
        
    def __str__(self):
        return self.libelle

class Accidents(models.Model):
    burencadrement_id = models.IntegerField(blank=True, null=True)
    comsite_id = models.IntegerField(blank=True, null=True)
    typaccident_id = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=500, blank=True, null=True)
    cause = models.CharField(max_length=500, blank=True, null=True)
    gravite = models.CharField(max_length=500, blank=True, null=True)
    autre_information = models.CharField(max_length=1500, blank=True, null=True)
    arret = models.CharField(max_length=1, blank=True, null=True)
    blessure = models.CharField(max_length=1, blank=True, null=True)
    mort = models.CharField(max_length=1, blank=True, null=True)
    vict_homme = models.IntegerField(blank=True, null=True)
    vict_femme = models.IntegerField(blank=True, null=True)
    vict_enfant = models.IntegerField(blank=True, null=True)
    mort_homme = models.IntegerField(blank=True, null=True)
    mort_femme = models.IntegerField(blank=True, null=True)
    mort_enfant = models.IntegerField(blank=True, null=True)
    degat = models.CharField(max_length=1, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    class Meta:
        verbose_name = "Accidents"
        verbose_name_plural = "Accident "
        
        
    
   


class Burencadrements(models.Model):
    libelle = models.CharField(max_length=2000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    class Meta:
        verbose_name = "Burencadrements"
        verbose_name_plural = "Bureau d'encadrement"
        
    def __str__(self):
        return self.libelle
    


class Cartartisants(models.Model):
    nom_prenom = models.CharField(max_length=2500, blank=True, null=True)
    type_carte = models.CharField(max_length=1500, blank=True, null=True)
    date_del = models.CharField(max_length=250, blank=True, null=True)
    date_exp = models.DateField(blank=True, null=True)
    localite = models.CharField(max_length=2500, blank=True, null=True)
    num_tel = models.CharField(max_length=1500, blank=True, null=True)
    num_quit = models.CharField(max_length=1500, blank=True, null=True)
    num_fich_eng = models.CharField(max_length=1500, blank=True, null=True)
    num_carte = models.CharField(max_length=1500, blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    nom_compt = models.CharField(max_length=2500, blank=True, null=True)
    date_heure = models.DateTimeField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

   


class Categories(models.Model):
    nom_categorie = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    
    class Meta:
        verbose_name = "Categories"
        verbose_name_plural = "Categorie"
        
    def __str__(self):
        return self.nom_categorie

    


class Communes(models.Model):
    commune = models.CharField(max_length=1000, blank=True, null=True)
    province_id = models.ForeignKey(Provinces, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    
    class Meta:
        verbose_name = "Communes"
        verbose_name_plural = "Commune"
        
    def __str__(self):
        return self.commune

    


class Comptoires(models.Model):
    nom_comptoire = models.CharField(max_length=1000)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    
    class Meta:
        verbose_name = "Comptoires"
        verbose_name_plural = "Comptoire"
        
    def __str__(self):
        return self.nom_comptoire

    


class Comsites(models.Model):
    code_site = models.ForeignKey(Typesites, blank=True, null=True, on_delete=models.CASCADE)
    nom_site = models.CharField(max_length=2500, blank=True, null=True)
    commune = models.ForeignKey(Communes, blank=True, null=True, on_delete=models.CASCADE)
    latitude = models.FloatField(max_length=1000, blank=True, null=True)
    longitude = models.FloatField(max_length=1000, blank=True, null=True)
    date_deb_expl = models.DateField(blank=True, null=True)
    date_fin_exp = models.DateField(blank=True, null=True)
    cat_site = models.ForeignKey(Categories, blank=True, null=True, on_delete=models.CASCADE)
    statut = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    class Meta:
        verbose_name = "Comsites"
        verbose_name_plural = "Site"
        
    def __str__(self):
        return self.nom_site

   


class Comzones(models.Model):
    code_zone = models.CharField(max_length=1000, blank=True, null=True)
    nom_zone = models.CharField(max_length=1500, blank=True, null=True)
    cat_zone = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    
    
    
    class Meta:
        verbose_name = "Comzones"
        verbose_name_plural = "Zone"
        
    def __str__(self):
        return self.nom_zone


class Incidents(models.Model):
    libelle = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    class Meta:
        verbose_name = "Incidents"
        verbose_name_plural = "Incident"
        
    def __str__(self):
        return self.libelle
    



class Demandeconventions(models.Model):
    OUI = "OUI"
    NON = "NON"
    
    DEMANDE = [
        (OUI, "oui"),
        (NON, "non"),
    ]
    
    
    
    PHYSIQUE = "PHYSIQUE"
    MORALE = "MORALE"
    
    TYPE = [
        (PHYSIQUE, "PERSONNE PHYSIQUE"),
        (MORALE, "PERSONNE MORALE"),
    ]
    
    identifiant = models.IntegerField(null=True, blank=True)
    num_ordre = models.CharField(max_length=400, blank=True, null=True)
    type_autorisation = models.ManyToManyField(Typautorisations, through='LigneTypeAutorisation')
    nombre_hectare = models.IntegerField(blank=True, null=True)
    localite = models.CharField(max_length=400, blank=True, null=True, verbose_name='Localité demandé')
    region = models.ForeignKey(Regions, on_delete=models.CASCADE , blank=True, null=True, related_name='region1', verbose_name='Region demandé')
    province = models.ForeignKey(Provinces, on_delete=models.CASCADE, blank=True, null=True, related_name='province1', verbose_name='Province demandé')
    #commune = models.ForeignKey(Communes, on_delete=models.CASCADE, blank=True, null=True, related_name='commune1')
    commune = models.CharField(max_length=400, blank=True, null=True)
    identifiaction = models.CharField(max_length=400, blank=True, null=True, choices=TYPE, default=PHYSIQUE)
    demande = models.CharField(max_length=10, blank=True, null=True, choices=DEMANDE, default=NON)
    nom_demandeur = models.CharField(max_length=400, blank=True, null=True)
    ref_piece = models.CharField(max_length=400, blank=True, null=True)
    localite_demandeur = models.CharField(max_length=400, blank=True, null=True, verbose_name='Localié du demandeur')
    region_demandeur = models.ForeignKey(Regions, on_delete=models.CASCADE , blank=True, null=True, related_name='region2', verbose_name='Region du demandeur')
    province_demandeur = models.ForeignKey(Provinces, on_delete=models.CASCADE, blank=True, null=True, related_name='province2', verbose_name='Province du demandeur')
    #commune_demandeur = models.ForeignKey(Communes, on_delete=models.CASCADE, blank=True, null=True,related_name='commune2')
    commune_demandeur = models.CharField(max_length=400, blank=True, null=True, verbose_name='Commune du demandeur')
    pays = models.CharField(max_length=400, blank=True, null=True)
    telephone = models.CharField(max_length=400, blank=True, null=True)
    telephone1 = models.CharField(max_length=400, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    site_web = models.CharField(max_length=350, blank=True, null=True)
    substances = models.TextField(max_length=400, blank=True, null=True)
    docs = models.FileField(upload_to='uploads', blank=True, null=True, verbose_name='Document Annexes')
    point = models.CharField(max_length=50, blank=True, null=True, verbose_name='Coordonées du site')
    pointforme = models.CharField(max_length=500, blank=True, null=True, verbose_name='Coordonées de la surface')
    nom_convntion = models.CharField(max_length=1000, blank=True, null=True)
    date_depot = models.DateField(blank=True, null=True)
    heure_depot = models.TimeField(max_length=150, blank=True, null=True)
    deposant = models.CharField(max_length=400, blank=True, null=True, verbose_name='Nom du deposant')
    
    
    reconnaissance = models.CharField(max_length=1, blank=True, null=True)
    concertation = models.CharField(max_length=1, blank=True, null=True)
    organisation = models.CharField(max_length=1, blank=True, null=True)
    plan_masse = models.CharField(max_length=1, blank=True, null=True)
    pv_constat = models.CharField(max_length=1, blank=True, null=True)
    nbr_puit = models.BigIntegerField(blank=True, null=True)
    nbr_puit_actif = models.BigIntegerField(blank=True, null=True)
    nbr_collecteur = models.BigIntegerField(blank=True, null=True)
    qte_or_puit = models.BigIntegerField(blank=True, null=True)
    qte_or_collecteur = models.BigIntegerField(blank=True, null=True)
    fournisseur = models.CharField(max_length=400, blank=True, null=True)
    exploitant = models.CharField(max_length=400, blank=True, null=True)
    date_signature = models.DateField(blank=True, null=True)
    date_effet_sign = models.DateField(blank=True, null=True)
    fichier = models.CharField(max_length=300, blank=True, null=True)
    date_exp = models.DateField(blank=True, null=True)
    date_premier_vers = models.DateField(blank=True, null=True)
    date_relance = models.DateField(blank=True, null=True)
    expire = models.CharField(max_length=1, blank=True, null=True)
    retire = models.CharField(max_length=1, blank=True, null=True)
    renonce = models.CharField(max_length=1, blank=True, null=True)
    statut = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    @property
    def fileURL(self):
        try:
            url = self.docs.url
        except:
            url = ''
        return url
    
class LigneTypeAutorisation(models.Model):
    autorisation = models.ForeignKey(Typautorisations, null=True, blank=True, on_delete=models.CASCADE)
    demande = models.ForeignKey(Demandeconventions, null=True, blank=True, on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True, null=True, blank=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)



class Fichenrolements(models.Model):
    identifiant = models.IntegerField(null=True, blank=True)
    nom = models.CharField(max_length=1000, blank=True, null=True)
    prenom = models.CharField(max_length=1000, blank=True, null=True)
    type_carte = models.ManyToManyField(Typecarte, through='LigneTypeCarte')
    date = models.DateField(blank=True, null=True)
    localite = models.CharField(max_length=1000, blank=True, null=True)
    telephone = models.CharField(max_length=500, blank=True, null=True)
    telephone2 = models.CharField(max_length=150, blank=True, null=True)
    quittance = models.CharField(max_length=500, blank=True, null=True)
    engagement = models.CharField(max_length=500, blank=True, null=True)
    num_carte = models.CharField(blank=True, null=True)
    observation = models.CharField(max_length=1000, blank=True, null=True)
    ref_piece = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.nom
    
    """
    def save(self, *args, **kwargs):
        # Vérifiez si un enregistrement avec le même identifiant existe déjà
        if Fichenrolements.objects.filter(identifiant=self.identifiant).exists():
            raise ValidationError('Un enregistrement avec le même identifiant existe déjà.')
        super(Fichenrolements, self).save(*args, **kwargs) """
    
    
class LigneTypeCarte(models.Model):
    carte = models.ForeignKey(Typecarte, null=True, blank=True, on_delete=models.CASCADE)
    fiche = models.ForeignKey(Fichenrolements, null=True, blank=True, on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True, null=True, blank=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)



class Ficheprelevements(models.Model):
    date_prelevement = models.DateField(blank=True, null=True)
    commune = models.ForeignKey(Communes, on_delete=models.CASCADE, blank=True, null=True)
    point_prelevement = models.CharField(max_length=1000, blank=True, null=True)
    longitude = models.FloatField(max_length=1000, blank=True, null=True)
    latitude = models.FloatField(max_length=1000, blank=True, null=True)
    altitude = models.FloatField(max_length=1000, blank=True, null=True)
    precision = models.FloatField(max_length=1000, blank=True, null=True)
    lieu = models.CharField(max_length=1500, blank=True, null=True)
    motif = models.TextField(blank=True, null=True)
    quantite = models.FloatField(blank=True, null=True)
    nombre_flacons_verre = models.IntegerField(blank=True, null=True)
    nombre_flacons_plastique = models.IntegerField(blank=True, null=True)
    type_nature_echant = models.CharField(max_length=1000, blank=True, null=True)
    conductivite = models.FloatField(blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    tds = models.FloatField(blank=True, null=True)
    oxigene_dissous = models.FloatField(blank=True, null=True)
    turbidite = models.FloatField(blank=True, null=True)
    bruit = models.CharField(max_length=1000, blank=True, null=True)
    odeur = models.CharField(max_length=1000, blank=True, null=True)
    lumiere = models.CharField(max_length=1000, blank=True, null=True)
    nom_personnes_commandiaire = models.TextField(max_length=1500, blank=True, null=True)
    adresse_personnes_commandiaire = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)



class Fichevisites(models.Model):
    bureau = models.ForeignKey(Burencadrements, blank=True, null=True, on_delete=models.CASCADE)
    date_visite = models.DateField(blank=True, null=True)
    date_miss = models.DateField(blank=True, null=True)
    nom_des_visiteurs = models.TextField(max_length=2000, blank=True, null=True)
    qualite = models.CharField(max_length=1500, blank=True, null=True)
    service = models.CharField(max_length=1500, blank=True, null=True)
    com_site = models.ForeignKey(Typesites, null=True, blank=True, on_delete=models.CASCADE)
    com_region = models.ForeignKey(Regions, null=True, blank=True, on_delete=models.CASCADE)
    com_province = models.ForeignKey(Provinces, null=True, blank=True, on_delete=models.CASCADE)
    commune = models.ForeignKey(Communes, blank=True, null=True, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    precision = models.FloatField(blank=True, null=True)
    nbr_hom = models.IntegerField(blank=True, null=True)
    nbr_fem = models.IntegerField(blank=True, null=True)
    nbr_enfant = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)


   


class Fichexpminieres(models.Model):
    nom_site = models.IntegerField(blank=True, null=True)
    but_mission = models.TextField(blank=True, null=True)
    date_la_mission = models.DateField(null=True, blank=True)
    region = models.CharField(max_length=300, blank=True, null=True)
    province = models.CharField(max_length=300, blank=True, null=True)
    commune = models.CharField(max_length=300, blank=True, null=True)
    site_a_cheval = models.BooleanField(blank=True, null=True)
    province2_id = models.IntegerField(blank=True, null=True)
    commune2_id = models.IntegerField(blank=True, null=True)
    village = models.CharField(max_length=300, blank=True, null=True)
    produit1 = models.CharField(max_length=300, blank=True, null=True)
    resultat = models.CharField(max_length=300, blank=True, null=True)
    comentaire = models.TextField(blank=True, null=True)
    produit2 = models.CharField(max_length=300, blank=True, null=True)
    resultat2 = models.CharField(max_length=300, blank=True, null=True)
    comentaire2 = models.TextField(blank=True, null=True)
    produit3 = models.CharField(max_length=300, blank=True, null=True)
    resultat3 = models.CharField(max_length=300, blank=True, null=True)
    comentaire3 = models.TextField(blank=True, null=True)
    produit4 = models.CharField(max_length=300, blank=True, null=True)
    resultat4 = models.CharField(max_length=300, blank=True, null=True)
    comentaire4 = models.TextField(blank=True, null=True)
    produit5 = models.CharField(max_length=300, blank=True, null=True)
    resultat5 = models.CharField(max_length=300, blank=True, null=True)
    comentaire5 = models.TextField(blank=True, null=True)
    produit6 = models.CharField(max_length=300, blank=True, null=True)
    resultat6 = models.CharField(max_length=300, blank=True, null=True)
    comentaire6 = models.TextField(blank=True, null=True)
    produit7 = models.CharField(max_length=300, blank=True, null=True)
    resultat7 = models.CharField(max_length=300, blank=True, null=True)
    comentaire7 = models.TextField(blank=True, null=True)
    produit8 = models.CharField(max_length=300, blank=True, null=True)
    resultat8 = models.CharField(max_length=300, blank=True, null=True)
    comentaire8 = models.TextField(blank=True, null=True)
    produit9 = models.CharField(max_length=300, blank=True, null=True)
    resultat9 = models.CharField(max_length=300, blank=True, null=True)
    comentaire9 = models.TextField(blank=True, null=True)
    produit10 = models.CharField(max_length=300, blank=True, null=True)
    resultat10 = models.CharField(max_length=300, blank=True, null=True)
    comentaire10 = models.TextField(blank=True, null=True)
    produit11 = models.CharField(max_length=300, blank=True, null=True)
    resultat11 = models.CharField(max_length=300, blank=True, null=True)
    comentaire11 = models.TextField(blank=True, null=True)
    produit12 = models.CharField(max_length=300, blank=True, null=True)
    resultat12 = models.CharField(max_length=300, blank=True, null=True)
    comentaire12 = models.TextField(blank=True, null=True)
    produit13 = models.CharField(max_length=300, blank=True, null=True)
    resultat13 = models.CharField(max_length=300, blank=True, null=True)
    comentaire13 = models.TextField(blank=True, null=True)
    produit14 = models.CharField(max_length=300, blank=True, null=True)
    resultat14 = models.CharField(max_length=300, blank=True, null=True)
    comentaire14 = models.TextField(blank=True, null=True)
    produit15 = models.CharField(max_length=300, blank=True, null=True)
    resultat15 = models.CharField(max_length=300, blank=True, null=True)
    comentaire15 = models.TextField(blank=True, null=True)
    produit16 = models.CharField(max_length=300, blank=True, null=True)
    resultat16 = models.CharField(max_length=300, blank=True, null=True)
    comentaire16 = models.TextField(blank=True, null=True)
    produit17 = models.CharField(max_length=300, blank=True, null=True)
    resultat17 = models.CharField(max_length=300, blank=True, null=True)
    comentaire17 = models.TextField(blank=True, null=True)
    produit18 = models.CharField(max_length=300, blank=True, null=True)
    resultat18 = models.CharField(max_length=300, blank=True, null=True)
    comentaire18 = models.TextField(blank=True, null=True)
    produit19 = models.CharField(max_length=300, blank=True, null=True)
    resultat19 = models.CharField(max_length=300, blank=True, null=True)
    comentaire19 = models.TextField(blank=True, null=True)
    produit20 = models.CharField(max_length=300, blank=True, null=True)
    resultat20 = models.CharField(max_length=300, blank=True, null=True)
    comentaire20 = models.TextField(blank=True, null=True)
    produit21 = models.CharField(max_length=300, blank=True, null=True)
    resultat21 = models.CharField(max_length=300, blank=True, null=True)
    comentaire21 = models.TextField(blank=True, null=True)
    produit22 = models.CharField(max_length=300, blank=True, null=True)
    resultat22 = models.CharField(max_length=300, blank=True, null=True)
    comentaire22 = models.TextField(blank=True, null=True)
    produit23 = models.CharField(max_length=300, blank=True, null=True)
    resultat23 = models.CharField(max_length=300, blank=True, null=True)
    comentaire23 = models.TextField(blank=True, null=True)
    produit24 = models.CharField(max_length=300, blank=True, null=True)
    resultat24 = models.CharField(max_length=300, blank=True, null=True)
    comentaire24 = models.TextField(blank=True, null=True)
    produit25 = models.CharField(max_length=300, blank=True, null=True)
    resultat25 = models.CharField(max_length=300, blank=True, null=True)
    comentaire25 = models.TextField(blank=True, null=True)
    produit26 = models.CharField(max_length=300, blank=True, null=True)
    resultat26 = models.CharField(max_length=300, blank=True, null=True)
    comentaire26 = models.TextField(blank=True, null=True)
    produit27 = models.CharField(max_length=300, blank=True, null=True)
    resultat27 = models.CharField(max_length=300, blank=True, null=True)
    comentaire27 = models.TextField(blank=True, null=True)
    produit28 = models.CharField(max_length=300, blank=True, null=True)
    resultat28 = models.CharField(max_length=300, blank=True, null=True)
    comentaire28 = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)



class Formguidautorites(models.Model):
    com_site = models.ForeignKey(Typesites, null=True, blank=True, on_delete=models.CASCADE)
    com_region = models.ForeignKey(Regions, null=True, blank=True, on_delete=models.CASCADE)
    com_province = models.ForeignKey(Provinces, null=True, blank=True, on_delete=models.CASCADE)
    commune = models.ForeignKey(Communes, blank=True, null=True, on_delete=models.CASCADE)
    nom_prenom_enqueteur = models.CharField(max_length=2500, blank=True, null=True)
    nom_prenom_autorite = models.CharField(max_length=2500, blank=True, null=True)
    village_site = models.CharField(max_length=1000, blank=True, null=True)
    nom_site = models.ForeignKey(Comsites, on_delete=models.CASCADE, blank=True, null=True)
    nom_prenom_ressouce = models.CharField(max_length=1000, blank=True, null=True)
    date_visite = models.DateField(blank=True, null=True)
    statut_site = models.ForeignKey(Statutsites, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)


    


class Formincidents(models.Model):
    
    accident = "accident"
    incident = "incident"
    
    TYPE = [
        (accident, "ACCIDENT"),
        (incident, "INCIDENT"),
    ]
    
    
    faible = "faible"
    moyen = "moyen"
    grave = "grave"
    tres_grave = "tres_grave"

    
    DEGRE = [
        (faible, "FAIBLE"),
        (moyen, "MOYEN"),
        (grave, "GRAVE"),
        (tres_grave, "TRES GRAVE"),
    ]
    
    exploitants = "exploitants"
    fournisseur = "fournisseur"
    commercants = "commercants"
    collecteurs = "collecteurs"
    visiteurs = "visiteurs"
    
    IMPLICATION = [(exploitants, "exploitants"),
                   (fournisseur, "fournisseur"),
                   (commercants, "commercants"),
                   (collecteurs, "collecteurs"),
                   (visiteurs, "visiteurs"),
                   ]
    identifiant = models.IntegerField(blank=True, null=True)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE , blank=True, null=True)
    province = models.ForeignKey(Provinces, on_delete=models.CASCADE, blank=True, null=True)
    commune = models.CharField(max_length=400, blank=True, null=True)
    nom_localite = models.CharField(max_length=2500, blank=True, null=True)
    nom_site = models.CharField(max_length=2500, blank=True, null=True)
    type_rapport = models.CharField(max_length=1500, blank=True, null=True, choices=TYPE, default='exploitants')
    date_incident = models.DateField(blank=True, null=True)
    heure_incident = models.TimeField(blank=True, null=True)
    type = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Type accident ou incident')
    zone = models.CharField(max_length=2500, blank=True, null=True)
    lieu =  models.CharField(max_length=2500, blank=True, null=True)
    degres = models.CharField(max_length=2500, blank=True, null=True, choices=DEGRE, default="MOYEN")
    implication = models.CharField(max_length=2500, blank=True, null=True, choices=IMPLICATION, default="MOYEN")
    description = models.TextField(blank=True, null=True)
    personne_implique = models.TextField(blank=True, null=True)
    equipement_implique = models.TextField(blank=True, null=True)
    cause = models.TextField(blank=True, null=True)
    action_corrective = models.TextField(blank=True, null=True)
    mesure_de_securite = models.TextField(blank=True, null=True)
    vict_hom = models.IntegerField(blank=True, null=True, verbose_name='Nombre Victime Homme', default=0)
    vict_fem = models.IntegerField(blank=True, null=True, verbose_name='Nombre Victime Femme', default=0)
    vict_enf = models.IntegerField(blank=True, null=True, verbose_name='Nombre Victime Enfant', default=0)
    mort_hom = models.IntegerField(blank=True, null=True, verbose_name='Nombre de Mort Homme', default=0)
    mort_fem = models.IntegerField(blank=True, null=True, verbose_name='Nombre de Mort Femme', default=0)
    mort_enf = models.IntegerField(blank=True, null=True, verbose_name='Nombre de Mort Enfant', default=0)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    

   

class Rapactivites(models.Model):
    
    
    achat = "achat"
    vente = "vente"
    fonte = "fonte"
               
    type_com = [(achat, "achat"),
               (vente, "vente"),
               (fonte, "fonte")]

    identifiant = models.IntegerField(blank=True, null=True)
    burencadrement_id = models.ForeignKey(Burencadrements, blank=True, null=True, verbose_name='BE', on_delete=models.CASCADE)
    periode1 = models.DateField(blank=True, null=True, verbose_name='periode du')
    periode2 = models.DateField(blank=True, null=True, verbose_name='au')
    nbr_conv = models.IntegerField(blank=True, null=True, verbose_name='nombre de convention')
    type_cart_art = models.ManyToManyField(Typecarte, through='LigneTypeRapactivitesCarte')
    nbr_cart_art = models.IntegerField(blank=True, null=True, verbose_name="nombre de carte d'artisant minier")
    autre1 = models.TextField(blank=True, null=True, verbose_name="si autre preciser")
    nbr_site = models.IntegerField(blank=True, null=True, verbose_name="nombre de site visité")
    nbr_commite = models.IntegerField(blank=True, null=True, verbose_name="nombre de commité de gestion")
    nbr_site_org = models.IntegerField(blank=True, null=True, verbose_name="nombre de site visité")
    nbr_coop = models.IntegerField(blank=True, null=True, verbose_name="nombre de cooperative")
    nbr_enf = models.IntegerField(blank=True, null=True, verbose_name="nombre d'enfant sur le site")
    mercure = models.CharField(max_length=25, blank=True, null=True, verbose_name="nombre mercure")
    cyanure = models.CharField(max_length=25, blank=True, null=True, verbose_name="nombre cyanure")
    acide = models.CharField(max_length=25, blank=True, null=True, verbose_name="nombre acide")
    borate = models.CharField(max_length=25, blank=True, null=True, verbose_name="nombre boraxe")
    chaux = models.CharField(max_length=25, blank=True, null=True, verbose_name="nombre chaux eteinte")
    explosif = models.CharField(max_length=25, blank=True, null=True, verbose_name="nombre explosif")
    autre = models.TextField(blank=True, null=True)
    nouveau_site = models.IntegerField(blank=True, null=True, verbose_name="nombre nouveaux sites")
    site_ferme = models.IntegerField(blank=True, null=True, verbose_name="nombre sites fermés")
    site_reactive = models.IntegerField(blank=True, null=True, verbose_name="nombre sites reactivés")
    site_rehabilite = models.IntegerField(blank=True, null=True, verbose_name="nombre sites réhabilité")
    minerai = models.CharField(max_length=1000, blank=True, null=True, verbose_name="minerais disponible")
    type_com = models.CharField(max_length=1000, blank=True, null=True, choices=type_com, verbose_name="Type commercial")
    quantite = models.BigIntegerField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)



    
class LigneTypeRapactivitesCarte(models.Model):
    typecarte = models.ForeignKey(Typecarte, null=True, blank=True, on_delete=models.CASCADE)
    activite = models.ForeignKey(Rapactivites, null=True, blank=True, on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True, null=True, blank=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)


   
