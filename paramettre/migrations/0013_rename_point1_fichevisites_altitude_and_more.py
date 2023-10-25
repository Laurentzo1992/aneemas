# Generated by Django 4.2.4 on 2023-10-25 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("paramettre", "0012_formguidautorites_date_visite"),
    ]

    operations = [
        migrations.RenameField(
            model_name="fichevisites",
            old_name="point1",
            new_name="altitude",
        ),
        migrations.RenameField(
            model_name="fichevisites",
            old_name="point2",
            new_name="latitude",
        ),
        migrations.RenameField(
            model_name="fichevisites",
            old_name="point3",
            new_name="longitude",
        ),
        migrations.RenameField(
            model_name="fichevisites",
            old_name="point4",
            new_name="precision",
        ),
        migrations.RemoveField(
            model_name="fichevisites",
            name="fichier",
        ),
        migrations.RemoveField(
            model_name="fichevisites",
            name="mission",
        ),
        migrations.RemoveField(
            model_name="fichevisites",
            name="personne1",
        ),
        migrations.AddField(
            model_name="fichevisites",
            name="bureau",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="paramettre.burencadrements",
            ),
        ),
        migrations.AddField(
            model_name="fichevisites",
            name="nom_des_visiteurs",
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
