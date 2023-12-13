# Generated by Django 4.2.4 on 2023-12-10 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0074_alter_representantfournisseur_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='autre_document',
            field=models.FileField(blank=True, null=True, upload_to='uploads/commercial/client'),
        ),
        migrations.AddField(
            model_name='client',
            name='document_identite',
            field=models.FileField(blank=True, null=True, upload_to='uploads/commercial/client/'),
        ),
        migrations.AddField(
            model_name='client',
            name='reference_document_identite',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
