# Generated by Django 4.2.4 on 2023-12-07 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0036_client_societe'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='addresse',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
