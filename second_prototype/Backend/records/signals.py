from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MealItem

@receiver(post_save, sender=MealItem)
def recompute_on_save(sender, instance, **kwargs):
    instance.day.recompute_summary()

@receiver(post_delete, sender=MealItem)
def recompute_on_delete(sender, instance, **kwargs):
    instance.day.recompute_summary()
