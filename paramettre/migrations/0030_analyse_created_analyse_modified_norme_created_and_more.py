# Generated by Django 4.2.4 on 2023-11-11 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paramettre', '0029_rename_unités_norme_unites'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyse',
            name='created',
            field=models.DateField(auto_created=True, auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='analyse',
            name='modified',
            field=models.DateField(auto_created=True, auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='norme',
            name='created',
            field=models.DateField(auto_created=True, auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='norme',
            name='modified',
            field=models.DateField(auto_created=True, auto_now_add=True, null=True),
        ),
    ]