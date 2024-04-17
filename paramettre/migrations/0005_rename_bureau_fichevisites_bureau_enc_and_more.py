# Generated by Django 4.2.4 on 2024-04-17 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paramettre', '0004_alter_demandeconventions_dossiers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fichevisites',
            old_name='bureau',
            new_name='bureau_enc',
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='accueil',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='adresse',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='app',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='bureau_enc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paramettre.burencadrements'),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='champ',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='cout',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='date_miss',
            field=models.DateField(blank=True, null=True, verbose_name='date de la mission'),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='date_octroi',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='datum',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='dest',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='difficultes_promoteur',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='distance1',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='distance2',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='distance4',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='distance5',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='distance6',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='ellipsoide',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='entree_prod',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='extract',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='mode_elemi',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='mode_lieu',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='nombre',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='organis',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='personne',
            field=models.TextField(blank=True, null=True, verbose_name='Membre de la mission'),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='personne2',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='point1',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='prod_mens',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='proffe',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='provenance1',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='provenance2',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='quali',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='qualification',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='qualit1',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='qualit2',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='qualite',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='quantit1',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='quantit2',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='rapport_promoteur_orpailleurs',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='rapport_promoteur_population',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='renouv',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='reserves',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='risqu',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='sante',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='securite',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='service',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='site_env',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='social',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='traitement',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='type1',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='type2',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='type_minerai',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='vegeta',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='formguidautorites',
            name='zone',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]