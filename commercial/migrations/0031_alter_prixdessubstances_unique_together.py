# Generated by Django 4.2.4 on 2023-12-06 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0030_prixdessubstances_poids'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='prixdessubstances',
            unique_together={('facture', 'type_de_substance', 'type_de_prix'), ('facture', 'control_lingot')},
        ),
    ]
