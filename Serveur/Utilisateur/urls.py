from django.urls import path
from . import views

urlpatterns = [
   path('get/',views.get_data, name='get_data'),  # Nouvelle URL pour les données JSON
   path('receive/', views.receive_data, name='sensor_data'),
   path('', views.login_util, name='login_util'),
   path('data/', views.show_data, name='show_data'),
   path('display/', views.display_data, name='historique'),
   path('logout/', views.logout_util, name='logout_util'),
   path('modifier_P/', views.modifier_profil, name='P_modifier'),
#*****************androi*******************************
   #path('sse/', views.sse_view, name='sse'),
   path('app/login/', views.login_app, name='android'),
   path('random-data/', views.apk_data, name='random_data'),
   path('app/user_info/', views.user_profile_view, name='user_profile'),
   path('app/dht-data/', views.dht_data_view, name='dht-data'),
]