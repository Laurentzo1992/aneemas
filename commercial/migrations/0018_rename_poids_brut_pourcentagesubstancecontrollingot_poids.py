# Generated by Django 4.2.4 on 2023-12-06 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0017_pourcentagesubstancecontrollingot_poids_brut_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pourcentagesubstancecontrollingot',
            old_name='poids_brut',
            new_name='poids',
        ),
    ]
