# Generated by Django 4.2.4 on 2023-12-13 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0100_rename_non_envoye_sms_list_non_envoye'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms',
            name='sent',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
