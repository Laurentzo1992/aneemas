# Generated by Django 4.2.4 on 2023-12-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0079_rename_numero_control_control_numero_de_control'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='cours_en_euro',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True),
        ),
    ]
