# Generated by Django 4.2.4 on 2023-10-25 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("paramettre", "0016_alter_demandeconventions_commune_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="demandeconventions",
            name="fichier1",
        ),
    ]