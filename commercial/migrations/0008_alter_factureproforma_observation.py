# Generated by Django 4.2.4 on 2023-12-06 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0007_factureproforma_cours_alter_fichetarification_cours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factureproforma',
            name='observation',
            field=models.TextField(blank=True, max_length=256, null=True),
        ),
    ]