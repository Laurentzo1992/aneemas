# Generated by Django 4.2.4 on 2023-12-10 10:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0070_control_control_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='date_control',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 10, 52, 52, 560061, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
