# Generated by Django 4.2.4 on 2023-12-10 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0084_remove_prixdessubstances_type_de_facture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='vente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commercial.vente'),
        ),
    ]
