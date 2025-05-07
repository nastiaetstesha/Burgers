from django.db.models.signals import pre_save
from django.dispatch import receiver
from foodcartapp.models import Order


@receiver(pre_save, sender=Order)
def set_status_cooking(sender, instance, **kwargs):
    if instance.cooking_restaurant and instance.status == 'unprocessed':
        instance.status = 'cooking'
