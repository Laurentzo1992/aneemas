# Generated by Django 4.2.4 on 2023-11-12 18:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commercial', '0037_paiement_delete_transaction'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Paiement',
            new_name='Payement',
        ),
    ]
