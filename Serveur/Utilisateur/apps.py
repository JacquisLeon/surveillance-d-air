"""
from django.apps import AppConfig


class UtilisateurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Utilisateur'
    """

from django.apps import AppConfig

class UtilisateurConfig(AppConfig):
    name = 'Utilisateur'

    def ready(self):
        import Utilisateur.signals  # Remplacez par le nom correct de votre module signals
