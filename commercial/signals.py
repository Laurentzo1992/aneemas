from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import AppConfig

@receiver(pre_save, sender='commercial.FicheTarification')
def fichetarification_pre_save(sender, instance, **kwargs):
    # Your pre-save logic here
    # if not instance.numero and instance.created:
    #     year = instance.created.year
    #     last_two_digits_of_year = str(year)[-2:]
    #     instance.numero = f"FTR{str(instance.id).zfill(6)}-{last_two_digits_of_year}3"
    pass