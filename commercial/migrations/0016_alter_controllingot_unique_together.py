# Generated by Django 4.2.4 on 2023-12-06 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0015_alter_controllingot_lingot'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='controllingot',
            unique_together={('control', 'lingot')},
        ),
    ]
