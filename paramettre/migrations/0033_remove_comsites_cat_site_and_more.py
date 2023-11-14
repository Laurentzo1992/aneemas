# Generated by Django 4.2.4 on 2023-11-14 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paramettre', '0032_comsites_annee_exploitation_comsites_conflit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comsites',
            name='cat_site',
        ),
        migrations.RemoveField(
            model_name='comsites',
            name='date_deb_expl',
        ),
        migrations.RemoveField(
            model_name='comsites',
            name='date_fin_exp',
        ),
        migrations.RemoveField(
            model_name='comsites',
            name='nbre_puit_toatal',
        ),
        migrations.AddField(
            model_name='comsites',
            name='contact_resource2',
            field=models.CharField(blank=True, max_length=2500, null=True, verbose_name='Personne resource 1(Contact)'),
        ),
        migrations.AddField(
            model_name='comsites',
            name='latitude1',
            field=models.FloatField(blank=True, null=True, verbose_name='Y2'),
        ),
        migrations.AddField(
            model_name='comsites',
            name='longitude1',
            field=models.FloatField(blank=True, null=True, verbose_name='X2'),
        ),
        migrations.AlterField(
            model_name='comsites',
            name='etendu',
            field=models.FloatField(blank=True, null=True, verbose_name='Etendu du site en (m)'),
        ),
        migrations.AlterField(
            model_name='comsites',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Y'),
        ),
        migrations.AlterField(
            model_name='comsites',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='X'),
        ),
        migrations.AlterField(
            model_name='comsites',
            name='zone',
            field=models.IntegerField(blank=True, null=True, verbose_name='Zone de projection'),
        ),
    ]
