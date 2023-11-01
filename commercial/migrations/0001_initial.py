# Generated by Django 4.2.4 on 2023-11-01 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fichecontrol',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('observation', models.CharField(max_length=256)),
                ('date_control', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FicheTarification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('observation', models.CharField(max_length=256)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_tarification', models.DateTimeField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('fiche_control', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.fichecontrol')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lingot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('poids_brut', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('poids_immerge', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ecart', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('densite', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('titre_carat', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quantite_or_fin', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date_reception', models.DateTimeField(blank=True)),
                ('observation', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('fiche_control', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.fichecontrol')),
                ('fiche_tarification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.fichetarification')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pesee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poids_brut', models.DecimalField(decimal_places=2, max_digits=10)),
                ('poids_immerge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('titre_carat', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('quantite_or_fin', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('date_pesee', models.DateField(blank=True, null=True)),
                ('observation', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('valide', models.BooleanField(default=True)),
                ('lingot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commercial.lingot')),
            ],
        ),
    ]
