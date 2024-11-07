
from django.contrib import admin
from .models import Seuils

@admin.register(Seuils)
class SeuilsAdmin(admin.ModelAdmin):
    list_display = ('humMax', 'humMin', 'tempMax', 'tempMin', 'gazMax', 'gazMin')  # Colonnes à afficher
    search_fields = ('humMax', 'humMin', 'tempMax', 'tempMin', 'gazMax', 'gazMin')  # Champs pour la recherche
