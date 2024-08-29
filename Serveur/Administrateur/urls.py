from django.urls import path
from .views import ajouteUtil,login_admin,liste_util,acceil_admin,supre_util,modifier_util
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
   path('ajouter/', ajouteUtil, name='ajouter'), 
   path('login/', login_admin, name='login_admin'),
   path('liste_util/', liste_util, name='liste'),
   path('acceil_admin/', acceil_admin, name='acceil'),
   path('suprimer/<int:user_id>/', supre_util, name='suprimer'),
   path('modifier/<int:user_id>/', modifier_util, name='modifier'),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)