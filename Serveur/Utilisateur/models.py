from django.db import models
from datetime import datetime

# Create your models here.

class DHTData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temp: {self.temperature}°C, Hum: {self.humidity}%, Time: {self.timestamp}"
    
class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=10)