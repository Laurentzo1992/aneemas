# Generated by Django 4.2.4 on 2023-11-10 06:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commercial', '0027_payement_actif_payement_archived_payement_confirme_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Payement',
            new_name='Transaction',
        ),
    ]
