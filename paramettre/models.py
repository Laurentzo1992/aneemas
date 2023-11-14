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
    code_site = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Code du site")
    date_creation = models.DateField( blank=True, null=True, verbose_name="date creation")
    nom_site = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Nom du site")
    region = models.ForeignKey(Regions, on_delete=models.CASCADE , blank=True, null=True, verbose_name='Region')
    province = models.ForeignKey(Provinces, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Province')
    commune = models.CharField(max_length=2500, blank=True, null=True)
    village = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Village")
    typesite = models.ForeignKey(Typesites, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Type de site')
    statut = models.ForeignKey(Statutsites, blank=True, null=True,  on_delete=models.CASCADE, verbose_name="Stut de site")
    nbre_puit_actif = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Nombre de puits actif")
    nbre_puit_total = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Nombre de puits total", default=0)
    annee_exploitation = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Nombre d'année d'exploitation")
    poulation = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Nombre de population approximative")
    nom_detenteur = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Nom du detenteur")
    personne_resource1 = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Personne resource 1(Nom et prenom)")
    contact_resource1 = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Personne resource 1(Contact)")
    personne_resource2 = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Personne resource 2 (Nom et prenom)")
    contact_resource2 = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Personne resource 1(Contact)")
    zone = models.IntegerField(blank=True, null=True, verbose_name="Zone de projection")
    longitude = models.CharField(max_length=2500, blank=True, null=True, verbose_name="X")
    latitude = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Y")
    longitude1 = models.CharField(max_length=2500, blank=True, null=True, verbose_name="X2")
    latitude1 = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Y2")
    etendu = models.CharField(max_length=2500, blank=True, null=True, verbose_name="Etendu du site en (m)")
    p_chimique = models.BooleanField(blank=True, null=True, verbose_name="Presence de produit chimique")
    p_explosif = models.BooleanField(blank=True, null=True, verbose_name="Presence d'explosif")
    machine = models.TextField(blank=True, null=True, verbose_name="Machine")
    conflit = models.BooleanField(blank=True, null=True, verbose_name="Conflit")
    obs_geo = models.TextField(blank=True, null=True, verbose_name="Observation geologique")
    #date_deb_expl = models.DateField(blank=True, null=True,verbose_name="Date debut d'exploitation")
    #date_fin_exp = models.DateField(blank=True, null=True, verbose_name="Date de fin d'exploitation")
    #cat_site = models.ForeignKey(Categories, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Categorie de site")
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
    
    # Demande
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
    
    #instruction
    reconnaissance = models.BooleanField(default=False, blank=True, null=True)
    concertation = models.BooleanField(default=False, blank=True, null=True)
    organisation = models.BooleanField(default=False, blank=True, null=True)
    plan_masse = models.BooleanField(default=False, blank=True, null=True)
    pv_constat = models.BooleanField(default=False, blank=True, null=True)
    
    nbr_puit = models.BigIntegerField(blank=True, null=True)
    nbr_puit_actif = models.BigIntegerField(blank=True, null=True)
    nbr_collecteur = models.BigIntegerField(blank=True, null=True)
    qte_or_puit = models.BigIntegerField(blank=True, null=True)
    qte_or_collecteur = models.BigIntegerField(blank=True, null=True)
    fournisseur = models.BooleanField(default=False, blank=True, null=True)
    exploitant = models.BooleanField(default=False, blank=True, null=True)
    fichier = models.FileField(upload_to='uploads', blank=True, null=True, verbose_name="Document Annexes à l'instruction")
   
    #Signature
    date_signature = models.DateField(blank=True, null=True)
    date_effet_sign = models.DateField(blank=True, null=True)
   
    date_exp = models.DateField(blank=True, null=True)
    date_premier_vers = models.DateField(blank=True, null=True)
    date_relance = models.DateField(blank=True, null=True)
    
    dossiers = models.FileField(upload_to='uploads', blank=True, null=True, verbose_name="Document Annexes à l'instruction")
   
    statut = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    
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
    
    eaux = "eaux"
    sol = "sol"
    
    nature = [(eaux, "eaux"),
              (sol, "sol"),]
    
    
    surface = "surface"
    souterrain = "souterrain"
    
    nature_eau = [(surface, "surface"),
              (souterrain, "souterrain"),]
    
    identifiant = models.IntegerField(blank=True, null=True)
    date_prelevement = models.DateField(blank=True, null=True)
    commune = models.CharField(max_length=2000, blank=True, null=True)
    point_prelevement = models.CharField(max_length=1000, blank=True, null=True)
    coordonnees = models.CharField(max_length=2000, blank=True, null=True)
    coordonnees_manu = models.CharField(max_length=2000, blank=True, null=True)
    lieu = models.CharField(max_length=1500, blank=True, null=True)
    motif = models.TextField(blank=True, null=True)
    quantite = models.FloatField(blank=True, null=True)
    nombre_flacons_verre = models.IntegerField(blank=True, null=True)
    nombre_flacons_plastique = models.IntegerField(blank=True, null=True)
    type_nature_echant = models.CharField(max_length=1000, blank=True, null=True, choices=nature, verbose_name="Nature echantillon")
    nat_eau = models.CharField(max_length=1000, blank=True, null=True, choices=nature_eau, verbose_name="Nature eaux")
    conductivite = models.FloatField(blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    tds = models.FloatField(blank=True, null=True)
    oxigene_dissous = models.FloatField(blank=True, null=True)
    turbidite = models.FloatField(blank=True, null=True)
    bruit = models.CharField(max_length=1000, blank=True, null=True)
    odeur = models.CharField(max_length=1000, blank=True, null=True)
    lumiere = models.CharField(max_length=1000, blank=True, null=True)
    nom_preleveur = models.TextField(max_length=1500, blank=True, null=True, verbose_name='Nom et Prenom du preleveur')
    nom_personnes_commandiaire = models.TextField(max_length=1500, blank=True, null=True, verbose_name='Nom et Prenom du commanditaire')
    adresse_personnes_commandiaire = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)



class Analyse(models.Model):
    prelevement = models.ForeignKey(Ficheprelevements, null=True, blank=True, on_delete=models.CASCADE)
    conductivite = models.FloatField(blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    tds = models.FloatField(blank=True, null=True)
    oxigene_dissous = models.FloatField(blank=True, null=True)
    turbidite = models.FloatField(blank=True, null=True)
    bruit = models.CharField(max_length=1000, blank=True, null=True)
    odeur = models.CharField(max_length=1000, blank=True, null=True)
    lumiere = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)

    
    
    
class Norme(models.Model):
    paramettre = models.CharField(max_length=100, null=True, blank=True)
    valeur = models.FloatField(null=True, blank=True)
    unites = models.CharField(max_length=10, null=True, blank=True)
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)



class Fichevisites(models.Model):
    identifiant = models.IntegerField(blank=True, null=True)
    bureau = models.ForeignKey(Burencadrements, blank=True, null=True, on_delete=models.CASCADE)
    date_visite = models.DateField(blank=True, null=True)
    date_miss = models.DateField(blank=True, null=True)
    nom_des_visiteurs = models.TextField(max_length=2000, blank=True, null=True)
    qualite = models.CharField(max_length=1500, blank=True, null=True)
    service = models.CharField(max_length=1500, blank=True, null=True)
    com_site = models.ForeignKey(Typesites, null=True, blank=True, on_delete=models.CASCADE)
    site = models.ForeignKey(Comsites, null=True, blank=True, on_delete=models.CASCADE)
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
    
    OUI = "OUI"
    NON = "NON"
    
    CHOIX = [
        (OUI, "oui"),
        (NON, "non"),
    ]
    
    BON = "BON"
    TENSION = "TENSION"
    
    RAPPORT = [
        (BON, "BON"),
        (TENSION, "TENSION"),
    ]
    
    tres_faible = "tres_faible"
    faible = "faible"
    moyen = "moyen"
    assez_eleve = "assez_eleve"
    eleve = "eleve"
    tres_eleve = "tres_eleve"
    
    op = [
        (tres_faible, "Très faible"),
        (faible, "faible"),
        (moyen, "moyen"),
        (assez_eleve, " Assez élevé"),
        (eleve, "élevé"),
        (tres_eleve, "  Très élevé"),
         
    ]
    
    nouveau = "nouveau"
    ancien = "ancien"
    reconnu = "reconnu"
    organise = "organise"
    insatnce = "insatnce"
    
    admi = [
        (nouveau, "Nouveau"),
        (ancien, "Ancien"),
        (reconnu, "Reconnu ou non"),
        (organise, "Organisé ou non"),
        (insatnce, "Dossier en instance"),
    ]
    
    identifiant = models.IntegerField(blank=True, null=True)
    nom_site = models.ForeignKey(Comsites, blank=True, null=True, on_delete=models.CASCADE)
    but_mission = models.TextField(blank=True, null=True)
    date_la_mission = models.DateField(null=True, blank=True)
    region = models.ForeignKey(Regions, max_length=300, blank=True, null=True, on_delete=models.CASCADE)
    province = models.ForeignKey(Provinces, max_length=300, blank=True, null=True, on_delete=models.CASCADE)
    commune = models.CharField(max_length=300, blank=True, null=True)
    departement = models.CharField(max_length=300, blank=True, null=True)
    village = models.CharField(max_length=300, blank=True, null=True)
    distance1 = models.FloatField(max_length=300, blank=True, null=True, verbose_name="Distence entre le site et les habitations")
    distance2 = models.FloatField(max_length=300, blank=True, null=True, verbose_name="Distence entre le site et les cours d'eaux")
    q9 = models.CharField(max_length=300, blank=True, null=True, verbose_name='Presence de champs ou culture?', choices=CHOIX)
    q12 = models.CharField(max_length=300, blank=True, null=True, verbose_name='Situation administrative', choices=admi)
    q13 = models.CharField(max_length=300, blank=True, null=True, verbose_name='Si en instance precisez son auteur et son etape')
    d_octroi = models.DateField(max_length=300, blank=True, null=True, verbose_name="Date d'octroi")
    d_renouv = models.DateField(max_length=300, blank=True, null=True, verbose_name="Date de renouvelmenet")
    d_fin = models.DateField(max_length=300, blank=True, null=True, verbose_name="Date de fin")
    adresse = models.CharField(max_length=300, blank=True, null=True)
    q19 = models.TextField(max_length=300, blank=True, null=True, verbose_name='Membre de commité rencontré')
    q21 = models.TextField(max_length=300, blank=True, null=True, verbose_name='Personne rencontré')
    q25 = models.IntegerField(blank=True, null=True, verbose_name='Nombre de site artisanal environnant officiel (rayon de 30km)')
    q26 = models.IntegerField(blank=True, null=True, verbose_name="Nombre de site d'exloiation environnant (rayon de 30km)")
    q27 = models.IntegerField(blank=True, null=True, verbose_name='Nombre de site artisanal environnant non organisés (rayon de 30km)')
    q28 = models.IntegerField(blank=True, null=True, verbose_name="Population")
    nb_e_site = models.IntegerField(blank=True, null=True, verbose_name="Nombre d'enfant de moin de 18 ANS")
    nb_es_site = models.IntegerField(blank=True, null=True, verbose_name="Nombre d'elèves rencontrés")
    nb_exploitant = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'exploiatant")
    nb_collecteurs = models.IntegerField(blank=True, null=True,verbose_name="Nombre de collecteur")
    q33 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de fournisseur de service")
    q34 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de detenteur de carte")
    q35 = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'intermediares")
    q36 = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'emplois directe générés")
    q37 = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'emplois indirect générés")
    q38 = models.IntegerField(blank=True, null=True,verbose_name="Superficie du site(zone d'extration plus zone de traitement)")
    q39 = models.IntegerField(blank=True, null=True,verbose_name="Repartition de l'espace en zone")
    q40 = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'association")
    q50 = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'association non organisées")
    q51 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de copperative")
    q52 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de PEA")
    q53 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de puit à grand diametre")
    q54 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de AEPS")
    q55 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de barrage")
    q57 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de paille")
    q58 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de semi dure(banco)")
    q60 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de parpaings")
    q61 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de csps")
    q62 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de cm")
    q63 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de cma")
    q65 = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'ecole primaire")
    q66 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de CEG")
    q67 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de qantine")
    q69 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de bibliotheque")
    q71 = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'Autre insfrasctures(moqués)")
    q72 = models.IntegerField(blank=True, null=True,verbose_name="Nombre 'Autre insfrasctures(eglise)")
    type_conflit = models.CharField(max_length=2000, blank=True, null=True,verbose_name="Type conflit")
    cause_conflit = models.CharField(max_length=2000, blank=True, null=True,verbose_name="Cause")
    rapport_promoteur_orpailleurs = models.CharField(max_length=2000,blank=True, null=True,verbose_name="Rapport promoteur/Artisan", choices=RAPPORT)
    rapport_promoteur_population = models.CharField(max_length=2000,blank=True, null=True,verbose_name="Rapport promoteur/Population", choices=RAPPORT)
    activites_promoteur = models.CharField(max_length=2000,blank=True, null=True,verbose_name="Activité méné par le promoteur")
    difficultes_promoteur = models.CharField(max_length=2000,blank=True, null=True,verbose_name="Difficulté rencontré par le promoteur")
    q78 = models.CharField(max_length=2000,blank=True, null=True,verbose_name="Appréciation des populations /Autorités")
    Flag_Exhaure = models.CharField(max_length=2000,blank=True, null=True,verbose_name="Presence d'exhaure")
    nb_puits_exhaure = models.CharField(max_length=2000,blank=True, null=True,verbose_name="Nombre de puit faisant l'obejt d'exhaure")
    duree_moy_pompage = models.CharField(max_length=2000,blank=True, null=True,verbose_name="Durée moyenne de pommpage d'eaux  de la nappe par puits par semaine")
    quantite_moy_eau_pompee_heure = models.CharField(max_length=2000,blank=True, null=True,verbose_name="Durée moyenne de pommpage d'eaux par heure")
    type_equipement = models.TextField(blank=True, null=True,verbose_name="Equipement utilisés (quantité, qualité, provenance)")
    q85 = models.CharField(max_length=2000, blank=True, null=True,verbose_name="Type d'Aeration")
    q86 = models.CharField(max_length=2000, blank=True, null=True,verbose_name="Type d'Eclairage")
    q87 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de trous aerés")
    type_equipement_aeration = models.TextField(blank=True, null=True,verbose_name="Equipement utilisés pour l'aeration (nom quantité, qualité, provenance)")
    type_equipement_eclairage = models.TextField(blank=True, null=True,verbose_name="Equipement utilisés pour l'aeration (nom quantité, qualité, provenance)")
    q96 = models.TextField(blank=True, null=True,verbose_name="Equipement utilisés pour l'etrationdu minerai (nom quantité, qualité, provenance)")
    q97 = models.TextField(blank=True, null=True,verbose_name="Equipement utilisés pour la remonté du minerai (nom quantité, qualité, provenance)")
    q98 = models.TextField(blank=True, null=True,verbose_name="Equipement utilisés pour la remonté du steril (nom quantité, qualité, provenance)")
    q99 = models.TextField(blank=True, null=True,verbose_name="Produi chimique (nom provencance, procédé d'utilisation)")
    type_nature_minerais = models.CharField(max_length=200, blank=True, null=True,verbose_name="type de minerais")
    provenance8 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Provenance du minerai")
    processus_traitement = models.CharField(max_length=200, blank=True, null=True,verbose_name="Process de traitement")
    qe130 = models.DateField(blank=True, null=True,verbose_name="Date d'entré en produit")
    prod_mensuelle_or = models.FloatField(blank=True, null=True,verbose_name="Date d'entré en produit")
    q131 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Destination de l'or")
    q132 = models.FloatField(blank=True, null=True,verbose_name="Tonage des rejet de produits")
    taxe_annuel = models.CharField(max_length=200, blank=True, null=True,verbose_name="Destination de l'or")
    paiement = models.CharField(max_length=200, blank=True, null=True,verbose_name="Taxe anuelle")
    distance7 = models.FloatField(blank=True, null=True,verbose_name="Distance moyenne des sources d'approvisonnement en eaux")
    distance8 = models.FloatField(blank=True, null=True,verbose_name="Distance moyenne des postes de santé")
    distance9 = models.FloatField(blank=True, null=True,verbose_name="Distance moyenne des postes de securité")
    distance10 = models.FloatField(blank=True, null=True,verbose_name="Distance moyenne avec les ecoles")
    nb_puits2 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de puits artisanal productif")
    nb_puits3 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de puits artisanal abandonné")
    q142 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Respect des date d'interdiction", choices=CHOIX)
    q149 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Port des ecquipement de portection", choices=CHOIX)
    q150 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Consommation de stupefiants", choices=CHOIX)
    q151 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Postitution", choices=CHOIX)
    q152 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Postitution infantile", choices=CHOIX)
    q153 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Délinquance", choices=CHOIX)
    q154 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Criminalité", choices=CHOIX)
    q155 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Utilisation d'explosif", choices=CHOIX)
    q156 = models.IntegerField(blank=True, null=True,verbose_name="Nombre de boutique d'alcool")
    q157 = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'explositifs accidentel")
    q158 = models.FloatField(blank=True, null=True,verbose_name="Superficie du site")
    q159 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Site protégé ", choices=CHOIX)
    q161 = models.CharField(max_length=200, blank=True, null=True,verbose_name="site à haute valeur de conservation",choices=CHOIX)
    q163 = models.FloatField(blank=True, null=True,verbose_name="Superficie pertubée")
    nb_arbre_coupe = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'arbre coupé")
    nb_arbre_reboise = models.IntegerField(blank=True, null=True,verbose_name="Nombre d'arbre reboisé")
    nb_arbre_survecu = models.CharField(max_length=200, blank=True, null=True,verbose_name="Nombre d'arbre reboisé ayant survecu")
    qe166 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Niveau d'utilisation du cyanure", choices=op)
    q167 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Niveau d'utilisation du mercure", choices=op)
    q168 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Niveau d'utilisation du acide", choices=op)
    q169 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Niveau d'emmission de la poussiere", choices=op)
    q170 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Presence d'hydrocarbure", choices=CHOIX)
    q171 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Presence d'Eau de l'amalgamationor-mercure", choices=CHOIX)
    q172 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Presence d'Eau de cyanure", choices=CHOIX)
    q173 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Presence de bassin de cyanure", choices=CHOIX)
    q174 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Presence d'eau usée dans les espace de traitement", choices=CHOIX)
    q175 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Presence  d'eau usée menagère", choices=CHOIX)
    q176 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Presence dordure menagère")
    q177 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Presence d'excreta")
    q178 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Bonne acceuil du promoteur", choices=CHOIX)
    q179 = models.CharField(max_length=200, blank=True, null=True,verbose_name="Qualité des informations receuilli")
    q180 = models.TextField(blank=True, null=True,verbose_name="Commentaire")
    created = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)
    modified = models.DateField(blank=True, null=True, auto_created=True, auto_now_add=True)



class Formguidautorites(models.Model):
    identifiant = models.IntegerField(blank=True, null=True)
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
    nom_site = models.ForeignKey(Comsites, max_length=2500, blank=True, null=True, on_delete=models.CASCADE)
    type_rapport = models.CharField(max_length=1500, blank=True, null=True, choices=TYPE, default='incident')
    date_incident = models.DateField(blank=True, null=True)
    heure_incident = models.TimeField(blank=True, null=True)
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


   
