# Generated by Django 4.2.4 on 2023-12-06 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0029_rename_type_substance_pourcentagesubstancecontrollingot_type_de_substance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prixdessubstances',
            name='poids',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True),
        ),
    ]
