from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Stone


# @receiver(post_save, sender=Stone)
# def generate_qr_on_create(sender, instance, created, **kwargs):
#     if created:
#         instance.generate_qr_code()
#         instance.save()
