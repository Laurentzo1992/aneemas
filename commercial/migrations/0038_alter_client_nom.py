# Generated by Django 4.2.4 on 2023-12-07 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0037_client_addresse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='nom',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
