from django.urls import path
from . import views

urlpatterns = [
   path('get/',views.get_data, name='get_data'),  # Nouvelle URL pour les données JSON
   path('receive/', views.receive_data, name='sensor_data'),
   path('', views.login_util, name='login_util'),
   path('courbe_data/', views.courbe_data, name='courbe_data'),
   path('bar_data/', views.bar_data, name='bar_data'),
   path('jauge_data/', views.jauge_data, name='jauge_data'),
   path('display/', views.display_data, name='historique'),
   path('logout/', views.logout_util, name='logout_util'),
   path('modifier_P/', views.modifier_profil, name='P_modifier'),
   path('add-dht-data/', views.add_dht_data, name='add_dht_data'),#ajouter donnée au interface
#*****************androi*******************************
   #path('sse/', views.sse_view, name='sse'),
   path('app/login/', views.login_app, name='android'),
   path('random-data/', views.apk_data, name='random_data'),
   path('app/user_info/', views.user_profile_view, name='user_profile'),
   path('app/dht-data/', views.dht_data_view, name='dht-data'),
   path('app/update_profile/', views.update_profile, name='update_profile'),
   
]