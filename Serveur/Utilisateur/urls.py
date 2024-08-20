from django.urls import path
from . import views

urlpatterns = [
   path('get/', views.get_data, name='get_data'),  # Nouvelle URL pour les données JSON
   path('', views.receive_data, name='sensor_data'),
   path('data/',views.show_data, name='show_data'),
]