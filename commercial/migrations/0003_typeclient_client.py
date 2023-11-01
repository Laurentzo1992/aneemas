# Generated by Django 4.2.4 on 2023-11-01 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paramettre', '0019_rename_comentaire1_fichexpminieres_comentaire_and_more'),
        ('commercial', '0002_factures'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=60)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=60, null=True)),
                ('prenom', models.CharField(blank=True, max_length=60, null=True)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cartartisan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paramettre.cartartisants')),
                ('type_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commercial.typeclient')),
            ],
        ),
    ]
