# Generated by Django 4.2.4 on 2023-12-06 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commercial', '0019_controllingot_date_control'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrixDesSubstancesFactureFactureDefinitive',
            fields=[
            ],
            options={
                'verbose_name_plural': 'PRIX DES SUBSTANCES',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('commercial.lingot',),
        ),
        migrations.CreateModel(
            name='PrixDesSubstancesFactureProforma',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('commercial.lingot',),
        ),
        migrations.CreateModel(
            name='PrixDesSubstances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('observation', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('type_de_prix', models.CharField(choices=[('proforma', 'Control BUMIGEB'), ('definitive', 'Rapport affinage')], default='proforma', max_length=20)),
                ('facture_definitive', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.facturedefinitive')),
                ('facture_proforma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.factureproforma')),
                ('substance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.pourcentagesubstancecontrollingot')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
