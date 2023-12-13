# Generated by Django 4.2.4 on 2023-12-06 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0023_remove_facture_cours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='poids_selon',
            field=models.CharField(choices=[('bumigeb', 'Control BUMIGEB'), ('affinage', 'Rapport affinage'), ('sonasp', 'Control SONASP')], default='bumigeb', max_length=20),
        ),
        migrations.AlterField(
            model_name='facture',
            name='type_de_facture',
            field=models.CharField(choices=[('proforma', 'Facture Proforma'), ('definitive', 'Facture definitive'), ('autre', 'Autre')], default='proforma', max_length=20),
        ),
        migrations.AlterField(
            model_name='prixdessubstances',
            name='type_de_prix',
            field=models.CharField(choices=[('proforma', 'Facture Proforma'), ('definitive', 'Facture definitive'), ('autre', 'Autre')], default='proforma', max_length=20),
        ),
        migrations.AlterField(
            model_name='vente',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.client'),
        ),
    ]