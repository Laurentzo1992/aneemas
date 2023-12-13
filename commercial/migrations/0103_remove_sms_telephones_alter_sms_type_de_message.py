# Generated by Django 4.2.4 on 2023-12-13 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0102_rename_sent_sms_envoye'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sms',
            name='Telephones',
        ),
        migrations.AlterField(
            model_name='sms',
            name='type_de_message',
            field=models.CharField(choices=[('f', 'Fournisseur'), ('c', 'Client')], default='f', max_length=20),
        ),
    ]