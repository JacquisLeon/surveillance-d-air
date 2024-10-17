from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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
#from Administrateur.models import ESP
"""
class DHTData(models.Model):
    esp = models.ForeignKey('ESP', on_delete=models.CASCADE, null=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    gaz = models.FloatField(null=True, default=0.0)
    feux = models.CharField(max_length=10, default="N/A")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"Temp: {self.temperature}°C, Hum: {self.humidity}%, Time: {self.timestamp}, Gaz: {self.gaz}, Feux: {self.feux}"
"""

class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=10)
 
    """  
class ESP(models.Model):
    lieu = models.CharField(max_length=100)
    """
