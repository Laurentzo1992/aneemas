# Generated by Django 4.2.4 on 2023-10-24 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "paramettre",
            "0006_remove_fichenrolements_type_carte_lignetypecarte_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lignetypecarte",
            name="quantite",
        ),
        migrations.AddField(
            model_name="lignetypecarte",
            name="modified",
            field=models.DateField(auto_created=True, auto_now_add=True, null=True),
        ),
    ]
