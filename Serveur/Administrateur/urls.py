from django.urls import path
from . import views
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
   path('ajouter/', views.ajouteUtil, name='ajouter'), 
   path('login/', views.login_admin, name='login_admin'),
   path('liste_util/', views.liste_util, name='liste'),
   path('courbe_admin/', views.courbe_admin, name='courbe_admin'),
   path('bar_admin/', views.bar_admin, name='bar_admin'),
   path('jauge_admin/', views.jauge_admin, name='jauge_admin'),
   path('suprimer/<int:user_id>/', views.supre_util, name='suprimer'),
   path('modifier/<int:user_id>/', views.modifier_util, name='modifier'),
   path('modifier-admin/', views.modifier_profil_admin, name='profil_admin'),
   path('histo-admin/', views.historique_admin, name='histo'),
   path('delete_selected/', views.delete_selected, name='delete_selected'),
   path('set_language/', views.set_language, name='set_language'),
    path('histo_util/<int:user_id>/', views.historique_utilisateur, name='histo_util'),
   
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)