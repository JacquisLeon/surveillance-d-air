#ajouter donner au interface web
from django import forms
from Administrateur import models
class Esp_forms(forms.ModelForm):
    class Meta:
        model = models.ESP
        #fields = ['lieu']
        fields = ['lieu', 'latitude', 'longitude']
        widgets = {
            'lieu': forms.TextInput(attrs={'placeholder': 'lieu d\'aplacement', 'class': 'form-control'}),
            'latitude': forms.TextInput(attrs={'placeholder': 'latitude', 'class': 'form-control'}),
            'longitude': forms.TextInput(attrs={'placeholder': 'longitude', 'class': 'form-control'}),
        }

class SeuilsForm(forms.ModelForm):
    class Meta:
        model = models.Seuils
        fields = ['humMax', 'humMin', 'tempMax', 'tempMin', 'gazMax', 'gazMin']