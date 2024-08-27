"""
from django.contrib import admin
from .models import client

# Register your models here.
@admin.register(client)
class ajouteClient(admin.ModelAdmin):
    list_display = ('id','nom','prenom','email','motdepasse')
    """