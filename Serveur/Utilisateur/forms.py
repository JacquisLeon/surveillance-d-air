#ajouter donner au interface web
from django import forms
from Administrateur import models
class DHTDataForm(forms.ModelForm):
    class Meta:
        model = models.DHTData
        fields = ['temperature', 'humidity', 'gaz', 'feux']
        widgets = {
            'feux': forms.TextInput(attrs={'placeholder': 'N/A'}),
            'gaz': forms.NumberInput(attrs={'placeholder': 'Optional'}),
        }