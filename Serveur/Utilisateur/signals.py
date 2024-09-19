from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DHTData

@receiver(post_save, sender=User)
def create_dht_data_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Crée une entrée DHTData pour le nouvel utilisateur avec des valeurs par défaut
        DHTData.objects.create(user=instance, temperature=0.0, humidity=0.0, gaz=None, feux="N/A")
