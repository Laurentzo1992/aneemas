# Generated by Django 4.2.4 on 2023-12-10 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0083_alter_prixdessubstances_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prixdessubstances',
            name='type_de_facture',
        ),
    ]
