from django.apps import AppConfig


class AdministrateurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Administrateur'

    def ready(self):
        #import Serveur.Utilisateur.signals  # Remplacez par le nom correct de votre module signals
        import Administrateur.signals


   
