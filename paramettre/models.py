from django.db import models


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
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

   


class Burencadrements(models.Model):
    libelle = models.CharField(max_length=2000, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


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
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

   


class Categories(models.Model):
    nom_categorie = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


class Communes(models.Model):
    nomcom = models.CharField(max_length=1000, blank=True, null=True)
    province_id = models.IntegerField(blank=True, null=True)
    id_2 = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    


class Comptoires(models.Model):
    nom_comptoire = models.CharField(max_length=1000)
    created = models.DateField()
    modified = models.DateField()

    


class Comsites(models.Model):
    code_site = models.CharField(max_length=1000, blank=True, null=True)
    nom_site = models.CharField(max_length=2500, blank=True, null=True)
    latitude = models.CharField(max_length=1000, blank=True, null=True)
    longitude = models.CharField(max_length=1000, blank=True, null=True)
    date_deb_expl = models.DateField(blank=True, null=True)
    date_fin_exp = models.DateField(blank=True, null=True)
    cat_site = models.IntegerField(blank=True, null=True)
    statut = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

   


class Comzones(models.Model):
    code_zone = models.CharField(max_length=1000, blank=True, null=True)
    nom_zone = models.CharField(max_length=1500, blank=True, null=True)
    cat_zone = models.CharField(max_length=1500, blank=True, null=True)

   


class Demandeconventions(models.Model):
    num_ordre = models.BigIntegerField(blank=True, null=True)
    q1 = models.CharField(max_length=400, blank=True, null=True)
    q2 = models.CharField(max_length=400, blank=True, null=True)
    nom_localite1 = models.CharField(max_length=400, blank=True, null=True)
    region_id = models.CharField(max_length=400, blank=True, null=True)
    province_id = models.CharField(max_length=400, blank=True, null=True)
    commune_id = models.CharField(max_length=400, blank=True, null=True)
    q4 = models.CharField(max_length=400, blank=True, null=True)
    q5 = models.CharField(max_length=400, blank=True, null=True)
    nom_personne = models.CharField(max_length=400, blank=True, null=True)
    ref = models.CharField(max_length=400, blank=True, null=True)
    q8 = models.CharField(max_length=400, blank=True, null=True)
    q9 = models.CharField(max_length=400, blank=True, null=True)
    q10 = models.CharField(max_length=400, blank=True, null=True)
    q11 = models.CharField(max_length=400, blank=True, null=True)
    q12 = models.CharField(max_length=350, blank=True, null=True)
    nom_localite2 = models.CharField(max_length=350, blank=True, null=True)
    region2_id = models.CharField(max_length=400, blank=True, null=True)
    province2_id = models.CharField(max_length=400, blank=True, null=True)
    commune2_id = models.CharField(max_length=400, blank=True, null=True)
    pays = models.CharField(max_length=350, blank=True, null=True)
    telephone1 = models.CharField(max_length=150, blank=True, null=True)
    telephone2 = models.CharField(max_length=350, blank=True, null=True)
    fax = models.CharField(max_length=350, blank=True, null=True)
    gsm = models.CharField(max_length=350, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    siteweb = models.CharField(max_length=300, blank=True, null=True)
    substance1 = models.CharField(max_length=400, blank=True, null=True)
    substance2 = models.CharField(max_length=400, blank=True, null=True)
    substance3 = models.CharField(max_length=400, blank=True, null=True)
    substance4 = models.CharField(max_length=400, blank=True, null=True)
    substance5 = models.CharField(max_length=400, blank=True, null=True)
    substance6 = models.CharField(max_length=400, blank=True, null=True)
    fichier1 = models.CharField(max_length=400, blank=True, null=True)
    fichier2 = models.CharField(max_length=400, blank=True, null=True)
    fichier3 = models.CharField(max_length=400, blank=True, null=True)
    fichier4 = models.CharField(max_length=400, blank=True, null=True)
    fichier5 = models.CharField(max_length=400, blank=True, null=True)
    fichier6 = models.CharField(max_length=400, blank=True, null=True)
    fichier7 = models.CharField(max_length=400, blank=True, null=True)
    fichier8 = models.CharField(max_length=400, blank=True, null=True)
    fichier9 = models.CharField(max_length=500, blank=True, null=True)
    fichier10 = models.CharField(max_length=500, blank=True, null=True)
    fichier11 = models.CharField(max_length=500, blank=True, null=True)
    ax = models.CharField(max_length=50, blank=True, null=True)
    ay = models.CharField(max_length=50, blank=True, null=True)
    bx = models.CharField(max_length=50, blank=True, null=True)
    by = models.CharField(max_length=50, blank=True, null=True)
    cx = models.CharField(max_length=50, blank=True, null=True)
    cy = models.CharField(max_length=50, blank=True, null=True)
    dx = models.CharField(max_length=50, blank=True, null=True)
    dy = models.CharField(max_length=50, blank=True, null=True)
    nom_conv = models.CharField(max_length=1000, blank=True, null=True)
    date_dep = models.DateField(blank=True, null=True)
    heure_dep = models.CharField(max_length=150, blank=True, null=True)
    deposant = models.CharField(max_length=400, blank=True, null=True)
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
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


class Fichenrolements(models.Model):
    agent = models.CharField(max_length=1500, blank=True, null=True)
    typzone_id = models.IntegerField(blank=True, null=True)
    nom = models.CharField(max_length=1000, blank=True, null=True)
    prenom = models.CharField(max_length=1000, blank=True, null=True)
    type_carte = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    localite = models.CharField(max_length=1000, blank=True, null=True)
    telephone = models.CharField(max_length=500, blank=True, null=True)
    telephone2 = models.CharField(max_length=150, blank=True, null=True)
    quittance = models.CharField(max_length=500, blank=True, null=True)
    engagement = models.CharField(max_length=500, blank=True, null=True)
    num_carte = models.IntegerField(blank=True, null=True)
    observation = models.CharField(max_length=1000, blank=True, null=True)
    ref_piece = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


class Ficheprelevements(models.Model):
    date_prelev = models.DateField(blank=True, null=True)
    commune_id = models.CharField(max_length=1000, blank=True, null=True)
    point = models.CharField(max_length=1000, blank=True, null=True)
    coord_gps = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=1000, blank=True, null=True)
    longitude = models.CharField(max_length=1000, blank=True, null=True)
    altitude = models.CharField(max_length=1000, blank=True, null=True)
    precision = models.CharField(max_length=1000, blank=True, null=True)
    coord_man_x = models.CharField(max_length=500, blank=True, null=True)
    coord_man_y = models.CharField(max_length=500, blank=True, null=True)
    lieu = models.CharField(max_length=1500, blank=True, null=True)
    motif = models.TextField(blank=True, null=True)
    quantite = models.FloatField(blank=True, null=True)
    nb_flacons_v = models.IntegerField(blank=True, null=True)
    nb_flacons_p = models.IntegerField(blank=True, null=True)
    type_nature_echant = models.CharField(max_length=1000, blank=True, null=True)
    conductivite = models.FloatField(blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    tds = models.FloatField(blank=True, null=True)
    oxigene_dissous = models.FloatField(blank=True, null=True)
    turbidite = models.FloatField(blank=True, null=True)
    bruit = models.CharField(max_length=1000, blank=True, null=True)
    odeur = models.CharField(max_length=1000, blank=True, null=True)
    lumiere = models.CharField(max_length=1000, blank=True, null=True)
    nom_personne1 = models.CharField(max_length=1500, blank=True, null=True)
    nom_personne2 = models.CharField(max_length=1500, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)



class Fichevisites(models.Model):
    mission = models.CharField(max_length=1500, blank=True, null=True)
    date_visite = models.DateField(blank=True, null=True)
    date_miss = models.DateField(blank=True, null=True)
    fichier = models.CharField(max_length=1000, blank=True, null=True)
    personne1 = models.CharField(max_length=2000, blank=True, null=True)
    qualite = models.CharField(max_length=1500, blank=True, null=True)
    service = models.CharField(max_length=1500, blank=True, null=True)
    com_site = models.CharField(max_length=500, blank=True, null=True)
    com_region = models.CharField(max_length=500, blank=True, null=True)
    com_province = models.CharField(max_length=500, blank=True, null=True)
    commune = models.CharField(max_length=500, blank=True, null=True)
    point1 = models.CharField(max_length=2000, blank=True, null=True)
    point2 = models.CharField(max_length=2000, blank=True, null=True)
    point3 = models.CharField(max_length=2000, blank=True, null=True)
    point4 = models.CharField(max_length=2000, blank=True, null=True)
    nbr_hom = models.BigIntegerField(blank=True, null=True)
    nbr_fem = models.BigIntegerField(blank=True, null=True)
    nbr_enfant = models.BigIntegerField(blank=True, null=True)

   


class Fichexpminieres(models.Model):
    nom_site = models.IntegerField(blank=True, null=True)
    but_mission = models.TextField(blank=True, null=True)
    region1_id = models.CharField(max_length=300, blank=True, null=True)
    province1_id = models.CharField(max_length=300, blank=True, null=True)
    commune1_id = models.CharField(max_length=300, blank=True, null=True)
    site_a_cheval = models.CharField(max_length=5, blank=True, null=True)
    province2_id = models.IntegerField(blank=True, null=True)
    commune2_id = models.IntegerField(blank=True, null=True)
    village = models.CharField(max_length=300, blank=True, null=True)
    produit1 = models.CharField(max_length=300, blank=True, null=True)
    resultat1 = models.CharField(max_length=300, blank=True, null=True)
    comentaire1 = models.TextField(blank=True, null=True)
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
    created = models.DateField(blank=True, null=True)

    


class Formdsracs(models.Model):
    date_decl = models.DateField(blank=True, null=True)
    den_compt = models.CharField(max_length=2000, blank=True, null=True)
    ref_agre = models.CharField(max_length=1000, blank=True, null=True)
    ifu = models.CharField(max_length=1000, blank=True, null=True)
    declarant = models.CharField(max_length=2000, blank=True, null=True)
    quantite_or_brut = models.FloatField(blank=True, null=True)
    quantite_or_fin = models.FloatField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

  


class Formguidautorites(models.Model):
    region = models.CharField(max_length=1000, blank=True, null=True)
    province = models.CharField(max_length=1000, blank=True, null=True)
    commune = models.CharField(max_length=1000, blank=True, null=True)
    village = models.CharField(max_length=1500, blank=True, null=True)
    nom_prenom_enqueteur = models.CharField(max_length=2500, blank=True, null=True)
    nom_prenom_autorite = models.CharField(max_length=2500, blank=True, null=True)
    village_site = models.CharField(max_length=1000, blank=True, null=True)
    nom_site = models.CharField(max_length=1000, blank=True, null=True)
    nom_prenom_ressouce = models.CharField(max_length=1000, blank=True, null=True)
    statut_site = models.IntegerField(blank=True, null=True)

    


class Formincidents(models.Model):
    code_incident = models.CharField(max_length=1000, blank=True, null=True)
    nom_site = models.CharField(max_length=2500, blank=True, null=True)
    nom_localite = models.CharField(max_length=2500, blank=True, null=True)
    com_region = models.CharField(max_length=1000, blank=True, null=True)
    com_province = models.CharField(max_length=1000, blank=True, null=True)
    commune = models.CharField(max_length=1000, blank=True, null=True)
    type_nature_incident = models.CharField(max_length=1500, blank=True, null=True)
    date_incident = models.DateField(blank=True, null=True)
    vict_hom = models.IntegerField(blank=True, null=True)
    vict_fem = models.IntegerField()
    vict_enf = models.IntegerField()
    mort_hom = models.IntegerField()
    mort_fem = models.IntegerField()
    mort_enf = models.IntegerField()
    created = models.DateField()
    modified = models.DateField()

    


class Incidents(models.Model):
    libelle = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

   



class Provinces(models.Model):
    numero = models.CharField(max_length=10, blank=True, null=True)
    nomprov = models.CharField(max_length=500, blank=True, null=True)
    region_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    


class Rapaccidents(models.Model):
    date_acc = models.DateField(blank=True, null=True)
    nature_acc = models.CharField(max_length=1000, blank=True, null=True)
    heure_acc = models.CharField(max_length=250, blank=True, null=True)
    zone_acc = models.TextField(blank=True, null=True)
    lieu_acc = models.CharField(max_length=1500, blank=True, null=True)
    deg_grav = models.CharField(max_length=1500, blank=True, null=True)
    partie_imp = models.TextField(blank=True, null=True)
    personne_imp = models.TextField(blank=True, null=True)
    equipe_imp = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cause = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    mesure = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


class Rapactivites(models.Model):
    burencadrement_id = models.IntegerField(blank=True, null=True)
    numero = models.CharField(max_length=1000, blank=True, null=True)
    periode = models.DateField(blank=True, null=True)
    nbr_conv = models.IntegerField(blank=True, null=True)
    nbr_cart_art = models.IntegerField(blank=True, null=True)
    type_cart_art = models.CharField(max_length=2000, blank=True, null=True)
    autre1 = models.TextField(blank=True, null=True)
    observation1 = models.TextField(blank=True, null=True)
    acte = models.CharField(max_length=1000, blank=True, null=True)
    autre2 = models.TextField(blank=True, null=True)
    observation2 = models.TextField(blank=True, null=True)
    nbr_site = models.IntegerField(blank=True, null=True)
    nbr_commite = models.IntegerField(blank=True, null=True)
    nbr_site_org = models.IntegerField(blank=True, null=True)
    nbr_coop = models.IntegerField(blank=True, null=True)
    travail_enf = models.CharField(max_length=25, blank=True, null=True)
    nbr_enf = models.IntegerField(blank=True, null=True)
    observation3 = models.TextField(blank=True, null=True)
    mercure = models.CharField(max_length=25, blank=True, null=True)
    cyanure = models.CharField(max_length=25, blank=True, null=True)
    acide = models.CharField(max_length=25, blank=True, null=True)
    borate = models.CharField(max_length=25, blank=True, null=True)
    chaux = models.CharField(max_length=25, blank=True, null=True)
    explosif = models.CharField(max_length=25, blank=True, null=True)
    autre = models.TextField(blank=True, null=True)
    observation4 = models.TextField(blank=True, null=True)
    nouveau_site = models.IntegerField(blank=True, null=True)
    site_ferme = models.IntegerField(blank=True, null=True)
    site_reactive = models.IntegerField(blank=True, null=True)
    site_rehabilite = models.IntegerField(blank=True, null=True)
    observation5 = models.TextField(blank=True, null=True)
    minerai = models.CharField(max_length=1000, blank=True, null=True)
    type_com = models.CharField(max_length=1000, blank=True, null=True)
    quantite = models.BigIntegerField(blank=True, null=True)

   


class Regions(models.Model):
    numero = models.CharField(unique=True, max_length=2, blank=True, null=True)
    nomreg = models.CharField(max_length=1000, blank=True, null=True)
    cheflieu = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    


class Statutsites(models.Model):
    libelle = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

   


class Typaccidents(models.Model):
    libelle = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

   


class Typautorisations(models.Model):
    libelle = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


class Typdemandeurs(models.Model):
    libelle = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


class Typenatureminerais(models.Model):
    libelle_type_nature_minerais = models.CharField(max_length=254, blank=True, null=True)
    flag_actif = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


class Typenatureterrains(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    flag_actif = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

  


class Typeorganisations(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    flag_actif = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

   

class Typeproduitchimiques(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    flag_actif = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


class Typequipements(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    flag_actif = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    


class Typesites(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    flag_actif = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

   


class Typetaterrains(models.Model):
    libelle = models.CharField(max_length=1000, blank=True, null=True)
    flag_actif = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)

    

   
