# Generated by Django 4.2.4 on 2023-12-06 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0034_alter_prixdessubstances_observation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prixdessubstances',
            name='poids',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='prixdessubstances',
            name='prix',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=20, null=True),
        ),
    ]
