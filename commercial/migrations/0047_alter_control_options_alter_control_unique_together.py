# Generated by Django 4.2.4 on 2023-12-07 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0046_control_document_signe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='control',
            options={'verbose_name_plural': 'Controls'},
        ),
        migrations.AlterUniqueTogether(
            name='control',
            unique_together={('vente', 'type_de_control')},
        ),
    ]