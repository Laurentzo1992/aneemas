# Generated by Django 4.2.4 on 2023-12-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0098_smsclient_smsfournisseur_sms_type_de_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms',
            name='non_envoye',
            field=models.TextField(blank=True, max_length=60, null=True),
        ),
    ]