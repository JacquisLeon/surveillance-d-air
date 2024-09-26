from django.urls import path
from . import views
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
 
    path('acceul_admin/', views.acceil_admin, name='acceil_admin'),
    path('ajouter/', views.ajouter_utilisateur, name='ajouter'), 
    path('login/', views.login_admin, name='login_admin'),
    path('liste_util/', views.liste_util, name='liste'),
    path('courbe_admin/<int:esp_id>/', views.courbe_admin, name='courbe_admin'),
    path('bar_admin/<int:esp_id>/', views.bar_admin, name='bar_admin'),
    path('jauge_admin/<int:esp_id>/', views.jauge_admin, name='jauge_admin'),
    path('suprimer/<int:user_id>/', views.supre_util, name='suprimer'),
    path('supre_esp/<int:esp_id>/', views.supre_esp, name='supre_esp'),
    path('modifier/<int:user_id>/', views.modifier_utilisateur, name='modifier'),
    path('modifier-admin/', views.modifier_profil_admin, name='profil_admin'),
    path('delete_selected/', views.delete_selected, name='delete_selected'),
    path('set_language/', views.set_language, name='set_language'),
    path('histo_esp/<int:esp_id>/', views.historique_esp, name='histo_esp'),
    path('modifier_esp/<int:esp_id>/', views.modifier_esp, name='modifier_esp'),
    path('liste_esp/', views.liste_ESP, name='liste_esp'),
   
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)