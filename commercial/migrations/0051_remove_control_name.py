# Generated by Django 4.2.4 on 2023-12-08 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0050_alter_control_observation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='control',
            name='name',
        ),
    ]