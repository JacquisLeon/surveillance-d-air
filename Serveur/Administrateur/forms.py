"""
from django import forms
from django.forms import fields, widgets
from .models import client

class regitreClient(forms.ModelForm):
    class Meta:
        model = client
        fields = ['nom','prenom','email','motdepasse']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control' }),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'motdepasse': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
"""