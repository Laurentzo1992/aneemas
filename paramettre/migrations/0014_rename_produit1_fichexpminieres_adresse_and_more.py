# Generated by Django 4.2.4 on 2023-11-08 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paramettre', '0013_fichevisites_identifiant_fichexpminieres_identifiant_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fichexpminieres',
            old_name='produit1',
            new_name='adresse',
        ),
        migrations.RenameField(
            model_name='fichexpminieres',
            old_name='produit10',
            new_name='departement',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire10',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire11',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire12',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire13',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire14',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire15',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire16',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire17',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire18',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire19',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire2',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire20',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire21',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire22',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire23',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire24',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire25',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire26',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire27',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire28',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire3',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire4',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire5',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire6',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire7',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire8',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='comentaire9',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='commune2_id',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit11',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit12',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit13',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit14',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit15',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit16',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit17',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit18',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit19',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit2',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit20',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit21',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit22',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit23',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit24',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit25',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit26',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit27',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit28',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit3',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit4',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit5',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit6',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit7',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit8',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='produit9',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='province2_id',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat10',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat11',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat12',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat13',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat14',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat15',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat16',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat17',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat18',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat19',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat2',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat20',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat21',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat22',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat23',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat24',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat25',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat26',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat27',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat28',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat3',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat4',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat5',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat6',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat7',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat8',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='resultat9',
        ),
        migrations.RemoveField(
            model_name='fichexpminieres',
            name='site_a_cheval',
        ),
        migrations.AddField(
            model_name='fichevisites',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paramettre.comsites'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='Flag_Exhaure',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name="Presence d'exhaure"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='activites_promoteur',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Activité méné par le promoteur'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='cause_conflit',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Cause'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='d_fin',
            field=models.DateTimeField(blank=True, max_length=300, null=True, verbose_name='Date de fin'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='d_octroi',
            field=models.DateField(blank=True, max_length=300, null=True, verbose_name="Date d'octroi"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='d_renouv',
            field=models.DateTimeField(blank=True, max_length=300, null=True, verbose_name='Date de renouvelmenet'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='difficultes_promoteur',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Difficulté rencontré par le promoteur'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='distance1',
            field=models.FloatField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='distance10',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='distance2',
            field=models.FloatField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='distance7',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='distance8',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='distance9',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='duree_moy_pompage',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name="Durée moyenne de pommpage d'eaux  de la nappe par puits par semaine"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_arbre_coupe',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_arbre_reboise',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_arbre_survecu',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_collecteurs',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de collecteur'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_e_site',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'enfant de moin de 18 ANS"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_es_site',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'elèves rencontrés"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_exploitant',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'exploiatant"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_puits2',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_puits3',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='nb_puits_exhaure',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name="Nombre de puit faisant l'obejt d'exhaure"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='paiement',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='processus_traitement',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Process de traitement'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='prod_mensuelle_or',
            field=models.FloatField(blank=True, null=True, verbose_name="Date d'entré en produit"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='provenance8',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Provenance du minerai'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q12',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Situation administrative'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q13',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Si en instance precisez son auteur et son etape'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q131',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q132',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q142',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q149',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q150',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q151',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q152',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q153',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q154',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q155',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q156',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q157',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q158',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q159',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q160',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q161',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q163',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q167',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q168',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q169',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q170',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q171',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q172',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q173',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q174',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q175',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q176',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q177',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q178',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q179',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q180',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q181',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q182',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q183',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q19',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Membre de commité rencontré'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q21',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Personne rencontré'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q25',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de site artisanal environnant officiel (rayon de 30km)'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q26',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre de site d'exloiation environnant (rayon de 30km)"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q27',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de site artisanal environnant non organisés (rayon de 30km)'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q28',
            field=models.IntegerField(blank=True, null=True, verbose_name='Population'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q33',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de fournisseur de service'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q34',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de detenteur de carte'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q35',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'intermediares"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q36',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'emplois directe générés"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q37',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'emplois indirect générés"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q38',
            field=models.IntegerField(blank=True, null=True, verbose_name="Superficie du site(zone d'extration plus zone de traitement)"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q39',
            field=models.IntegerField(blank=True, null=True, verbose_name="Repartition de l'espace en zone"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q40',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'association"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q50',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'association non organisées"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q51',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de copperative'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q52',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de PEA'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q53',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de puit à grand diametre'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q54',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de AEPS'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q55',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de barrage'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q57',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de paille'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q58',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de semi dure(banco)'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q60',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de parpaings'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q61',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de csps'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q62',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de cm'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q63',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de cma'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q65',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'ecole primaire"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q66',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de CEG'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q67',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de qantine'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q69',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de bibliotheque'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q71',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'Autre insfrasctures(moqués)"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q72',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre 'Autre insfrasctures(eglise)"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q78',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Appréciation des populations /Autorités'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q85',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name="Type d'Aeration"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q86',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name="Type d'Eclairage"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q87',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de trous aerés'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q9',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Presence de champs ou culture?'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q96',
            field=models.TextField(blank=True, null=True, verbose_name="Equipement utilisés pour l'etrationdu minerai (nom quantité, qualité, provenance)"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q97',
            field=models.TextField(blank=True, null=True, verbose_name='Equipement utilisés pour la remonté du minerai (nom quantité, qualité, provenance)'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q98',
            field=models.TextField(blank=True, null=True, verbose_name='Equipement utilisés pour la remonté du steril (nom quantité, qualité, provenance)'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='q99',
            field=models.TextField(blank=True, null=True, verbose_name="Produi chimique (nom provencance, procédé d'utilisation)"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='qe130',
            field=models.DateField(blank=True, null=True, verbose_name="Date d'entré en produit"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='qe166',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='quantite_moy_eau_pompee_heure',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name="Durée moyenne de pommpage d'eaux par heure"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='rapport_promoteur_orpailleurs',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Rapport promoteur/Artisan'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='rapport_promoteur_population',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Rapport promoteur/Population'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='taxe_annuel',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name="Destination de l'or"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='type_conflit',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Type conflit'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='type_equipement',
            field=models.TextField(blank=True, null=True, verbose_name='Equipement utilisés (quantité, qualité, provenance)'),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='type_equipement_aeration',
            field=models.TextField(blank=True, null=True, verbose_name="Equipement utilisés pour l'aeration (nom quantité, qualité, provenance)"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='type_equipement_eclairage',
            field=models.TextField(blank=True, null=True, verbose_name="Equipement utilisés pour l'aeration (nom quantité, qualité, provenance)"),
        ),
        migrations.AddField(
            model_name='fichexpminieres',
            name='type_nature_minerais',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='type de minerais'),
        ),
        migrations.AlterField(
            model_name='fichexpminieres',
            name='nom_site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paramettre.comsites'),
        ),
        migrations.AlterField(
            model_name='fichexpminieres',
            name='province',
            field=models.ForeignKey(blank=True, max_length=300, null=True, on_delete=django.db.models.deletion.CASCADE, to='paramettre.provinces'),
        ),
        migrations.AlterField(
            model_name='fichexpminieres',
            name='region',
            field=models.ForeignKey(blank=True, max_length=300, null=True, on_delete=django.db.models.deletion.CASCADE, to='paramettre.regions'),
        ),
    ]