# Generated by Django 4.2.4 on 2023-12-09 20:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0059_control_vente'),
    ]

    operations = [
        migrations.AddField(
            model_name='vente',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 12, 9, 20, 31, 46, 937971, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
