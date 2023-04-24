from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Warranty, Phone

@receiver(post_save, sender=Warranty)
def update_phone(sender, instance, created, **kwargs):
    if created:
        phone = instance.phone
        phone.serial = instance.serial
        phone.name = instance.name
        phone.start_date = instance.start_date
        phone.end_date = instance.end_date
        phone.save()