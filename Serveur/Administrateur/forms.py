#ajouter donner au interface web
from django import forms
from Administrateur import models
class Esp_forms(forms.ModelForm):
    class Meta:
        model = models.ESP
        fields = ['lieu']
        widgets = {
            'lieu': forms.TextInput(attrs={'placeholder': 'lieu d\'aplacement', 'class': 'form-control'}),
        }