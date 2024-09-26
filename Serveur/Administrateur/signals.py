from django.db.models.signals import post_save
from django.dispatch import receiver

from Administrateur.models import DHTData

def create_dht_data_for_new_esp(sender, instance, created, **kwargs):
    if created:
        DHTData.objects.create(
            esp=instance,  # Assurez-vous de spécifier l'instance ESP
            temperature=0.0,  # Ou une autre valeur par défaut
            humidity=0.0,
            gaz=0.0,
            feux="N/A"
        )

