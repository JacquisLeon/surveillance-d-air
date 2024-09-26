from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Client

admin.site.site_header = _("Mon Administration")
admin.site.site_title = _("Surveillance de l'air")
admin.site.index_title = _("Bienvenue au Admi")
"""
@admin.register(DHTData)
class DHTDataAdmin(admin.ModelAdmin):
    list_display = ('temperature', 'humidity', 'timestamp')
"""
@admin.register(Client)
class ListeUtilisateur(admin.ModelAdmin):
    list_display = ('nom', 'email', 'password')
    

    
