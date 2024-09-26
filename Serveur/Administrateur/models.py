# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class ESP(models.Model):
    lieu = models.CharField(max_length=100)
    
class DHTData(models.Model):
    esp = models.ForeignKey('ESP', on_delete=models.CASCADE, null=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    gaz = models.FloatField(null=True, default=0.0)
    feux = models.CharField(max_length=10, default="N/A")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"Temp: {self.temperature}°C, Hum: {self.humidity}%, Time: {self.timestamp}, Gaz: {self.gaz}, Feux: {self.feux}"
