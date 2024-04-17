# Generated by Django 4.2.4 on 2023-12-10 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paramettre', '0011_remove_comsites_point'),
        ('commercial', '0063_alter_fournisseur_cartartisan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fournisseur',
            name='cartartisan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='paramettre.cartartisants'),
            preserve_default=False,
        ),
    ]