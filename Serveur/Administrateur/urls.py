from django.urls import path
from . import views
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
   path('ajouter/', views.ajouteUtil, name='ajouter'), 
   path('login/', views.login_admin, name='login_admin'),
   path('liste_util/', views.liste_util, name='liste'),
   path('acceil_admin/', views.acceil_admin, name='acceil'),
   path('suprimer/<int:user_id>/', views.supre_util, name='suprimer'),
   path('modifier/<int:user_id>/', views.modifier_util, name='modifier'),
   path('modifier-admin/', views.modifier_profil_admin, name='profil_admin'),
   path('histo-admin/', views.historique_admin, name='histo'),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)