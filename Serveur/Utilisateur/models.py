from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
"""
class DHTData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    gaz = models.FloatField(null=True)
    feux = models.CharField(max_length=10, default="N/A")
    timestamp = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return f"Temp: {self.temperature}°C, Hum: {self.humidity}%, Time: {self.timestamp}, Gaz: {self.gaz}, Feux: {self.feux}"
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class DHTData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    gaz = models.FloatField(null=True, default=0.0)
    feux = models.CharField(max_length=10, default="N/A")
    timestamp = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"User: {self.user.username}, Temp: {self.temperature}°C, Hum: {self.humidity}%, Time: {self.timestamp}, Gaz: {self.gaz}, Feux: {self.feux}"
    
#ajouter donner au interface web
from django import forms
class DHTDataForm(forms.ModelForm):
    class Meta:
        model = DHTData
        fields = ['temperature', 'humidity', 'gaz', 'feux']
        widgets = {
            'feux': forms.TextInput(attrs={'placeholder': 'N/A'}),
            'gaz': forms.NumberInput(attrs={'placeholder': 'Optional'}),
        }

class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=10)
    
