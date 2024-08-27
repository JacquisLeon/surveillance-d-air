from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('ajouter/', views.ajouteUtil, name='ajouter'), 
   path('login/', views.login_admin, name='login_admin'),
   path('liste_util/', views.liste_util, name='liste'),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)