# Generated by Django 4.2.4 on 2023-12-10 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0066_alter_structuredecontrol_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='control_client',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]