from django.urls import path
from . import views

urlpatterns = [
   path('get/', views.get_data, name='get_data'),  # Nouvelle URL pour les données JSON
   path('receive/', views.receive_data, name='sensor_data'),
   path('', views.login_util, name='login_util'),
   path('data/',views.show_data, name='show_data'),
   path('display/', views.display_data, name='historique'),
   path('lougout/', views.logout_util, name='logout_util'),
   
]