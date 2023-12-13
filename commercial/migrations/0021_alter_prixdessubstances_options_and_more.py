# Generated by Django 4.2.4 on 2023-12-06 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commercial', '0020_prixdessubstancesfacturefacturedefinitive_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prixdessubstances',
            options={'verbose_name_plural': 'PRIX DES SUBSTANCES'},
        ),
        migrations.RemoveField(
            model_name='vente',
            name='facture_definitive',
        ),
        migrations.RemoveField(
            model_name='vente',
            name='facture_proforma',
        ),
        migrations.RemoveField(
            model_name='vente',
            name='rapport_affinage',
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cours', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('poids_selon', models.CharField(choices=[('bumigeb', 'Control BUMIGEB'), ('affinage', 'Rapport affinage'), ('sonasp', 'Control SONASP')], max_length=20)),
                ('observation', models.TextField(blank=True, max_length=256, null=True)),
                ('type_de_facture', models.CharField(choices=[('proforma', 'Control BUMIGEB'), ('definitive', 'Rapport affinage')], default='proforma', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('archived', models.BooleanField(default=False)),
                ('numero', models.CharField(blank=True, max_length=16, null=True, unique=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('vente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commercial.vente')),
            ],
            options={
                'verbose_name_plural': 'Facture proforma',
                'unique_together': {('vente', 'type_de_facture')},
            },
        ),
        migrations.AddField(
            model_name='prixdessubstances',
            name='facture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.facture'),
        ),
        migrations.AlterUniqueTogether(
            name='prixdessubstances',
            unique_together={('facture', 'substance')},
        ),
        migrations.RemoveField(
            model_name='prixdessubstances',
            name='facture_definitive',
        ),
        migrations.RemoveField(
            model_name='prixdessubstances',
            name='facture_proforma',
        ),
        migrations.DeleteModel(
            name='FactureProforma',
        ),
    ]