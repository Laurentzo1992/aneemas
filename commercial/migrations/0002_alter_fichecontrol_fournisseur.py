# Generated by Django 4.2.4 on 2023-12-05 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichecontrol',
            name='fournisseur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.fournisseur'),
        ),
    ]
