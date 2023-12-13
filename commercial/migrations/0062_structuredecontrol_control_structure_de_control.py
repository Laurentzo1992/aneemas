# Generated by Django 4.2.4 on 2023-12-10 09:28

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0061_remove_facture_poids_selon'),
    ]

    operations = [
        migrations.CreateModel(
            name='StructureDeControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('societe', models.CharField(blank=True, max_length=60, null=True)),
                ('reference_societe', models.CharField(blank=True, max_length=1024, null=True)),
                ('email', models.EmailField(max_length=60)),
                ('telephone', models.CharField(blank=True, max_length=15, null=True)),
                ('addresse', models.CharField(blank=True, max_length=120, null=True)),
                ('pays', django_countries.fields.CountryField(default='BF', max_length=2)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.AddField(
            model_name='control',
            name='structure_de_control',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commercial.structuredecontrol'),
        ),
    ]