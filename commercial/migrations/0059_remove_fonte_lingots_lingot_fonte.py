# Generated by Django 4.2.4 on 2023-11-18 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0058_lingot_numero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fonte',
            name='lingots',
        ),
        migrations.AddField(
            model_name='lingot',
            name='fonte',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commercial.fonte'),
        ),
    ]
