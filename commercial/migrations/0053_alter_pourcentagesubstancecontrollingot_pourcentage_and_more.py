# Generated by Django 4.2.4 on 2023-12-09 07:45

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0052_alter_pourcentagesubstancecontrollingot_pourcentage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pourcentagesubstancecontrollingot',
            name='pourcentage',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='pourcentagesubstancelingot',
            name='pourcentage',
            field=models.DecimalField(decimal_places=4, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]