# Generated by Django 4.2.4 on 2023-11-08 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0017_rename_client_fichecontrol_fournisseur_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TypeLingot',
            new_name='TypeSubstance',
        ),
        migrations.RenameField(
            model_name='directionlingot',
            old_name='type_lingot',
            new_name='type_substance',
        ),
        migrations.RenameField(
            model_name='mouvementlingot',
            old_name='type_lingot',
            new_name='type_substance',
        ),
    ]
