
#from gettext import translation
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
#from .decorators import superuser_required # type: ignore
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import UserProfile  # Importer le modèle UserProfile
from django.contrib.auth import update_session_auth_hash  # Import supplémentaire pour garder la session active
from django.contrib.auth.decorators import user_passes_test
from Utilisateur import models
import json
# Create your views here.
from django.utils.translation import gettext as _

def is_admin(user):
    return user.is_staff  # Vérifie si l'utilisateur est un administrateur
@user_passes_test(is_admin, login_url='login_admin')
def acceil_admin(request):
         # Récupérer l'image de profil de l'administrateur connecté
    admin = request.user
    try:
        admin_profile = admin.userprofile  # Profil de l'administrateur
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si l'administrateur n'a pas de profil
        
    esp_list = models.ESP.objects.all()
    esp_data = [{'id':esp.id,'latitude': esp.latitude, 'longitude': esp.longitude, 'lieu': esp.lieu} for esp in esp_list]
    return render(request, 'admini/Acceil.html',{'admin_profile': admin_profile,  # Profil de l'administrateur
                                                 'administrateur':request.user,
                                                 'esp_list': json.dumps(esp_data)})


#@user_passes_test(is_admin, login_url='login_admin')
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
    
@user_passes_test(is_admin, login_url='login_admin')
def liste_util(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    # Récupérer toutes les données de la base de données, y compris le profil utilisateur
    all_data = User.objects.select_related('userprofile').order_by('-id')
    return render(request, 'admini/liste_util.html', {'all_data': all_data,
                                                    'admin_profile': admin_profile,
                                                  'administrateur': user})

@user_passes_test(is_admin, login_url='login_admin')
def courbe_admin(request, esp_id):
    user = request.user  # Utilisateur actuellement connecté
     # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    # Récupérez les données de DHTData sans utiliser le champ esp
    data = models.DHTData.objects.last()  # Ou appliquez d'autres filtres si nécessaire
    esp = get_object_or_404(models.ESP, id=esp_id)
    # Préparez les données pour votre template
    context = {
        'admin_profile': admin_profile,
        'administrateur': user,
        'data': data,
        'esp_id': esp_id,  # Ajoutez esp_id ici
         'esp': esp,
    }
    return render(request, 'admini/courbe.html', context)


@user_passes_test(is_admin, login_url='login_admin')
def jauge_admin(request, esp_id):
    user = request.user  # Utilisateur actuellement connecté
     # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    # Récupérez les données de DHTData sans utiliser le champ esp
    data = models.DHTData.objects.last()  # Ou appliquez d'autres filtres si nécessaire
    esp = get_object_or_404(models.ESP, id=esp_id)
    # Préparez les données pour votre template
    context = {
        'admin_profile': admin_profile,
        'administrateur': user,
        'data': data,
        'esp_id': esp_id,  # Ajoutez esp_id ici
        'esp': esp,
    }
    return render(request, 'admini/jauge.html', context)

@user_passes_test(is_admin, login_url='login_admin')
def bar_admin(request, esp_id):
    user = request.user  # Utilisateur actuellement connecté
     # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    # Récupérez les données de DHTData sans utiliser le champ esp
    data = models.DHTData.objects.last()  # Ou appliquez d'autres filtres si nécessaire
    esp = get_object_or_404(models.ESP, id=esp_id)
    # Préparez les données pour votre template
    context = {
        'admin_profile': admin_profile,
        'administrateur': user,
        'data': data,
        'esp_id': esp_id,  # Ajoutez esp_id ici
        'esp': esp,
    }
    return render(request, 'admini/bar.html', context)


def login_admin(request):
    if request.method == 'POST':
        nam = request.POST.get('admname')
        ps = request.POST.get('admpass')
        if not nam or not ps:
            messages.error(request,"Veuillez remplir tous les champs!")
        else:
            adm = authenticate(request,username=nam,password=ps)
            if adm is not None:
                if adm.is_superuser: 
                    login(request,adm)
                    return redirect('acceil_admin') #ouvrir la paged'admin
                else:
                    messages.error(request,"Vous n'avez pas les droits administratifs!")
            else:
                messages.error(request,"Nom d'utilisateur ou mot de passe incorrect!")
    return render(request, 'admini/login.html')

@user_passes_test(is_admin, login_url='login_admin')
def logout_admin(request):
    logout(request)
    return redirect('login_admin')

@user_passes_test(is_admin, login_url='login_admin')
def supre_util(request, user_id):
    util = get_object_or_404(User, id=user_id)
    util.delete()
    messages.success(request, "L'utilisateur a été supprimé avec succès!")
    return redirect('liste')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile

# Vue pour ajouter un nouvel utilisateur
@user_passes_test(is_admin, login_url='login_admin')
def ajouter_utilisateur(request):
    if request.method == 'POST':
        nom_util = request.POST.get('name')
        email_util = request.POST.get('email')
        pass_util = request.POST.get('pass')
        img = request.FILES.get('image')
        role_util = request.POST.get('role')  # Récupérer le rôle de l'utilisateur

        # Vérifier si un utilisateur avec cet email ou ce nom d'utilisateur existe déjà
        if User.objects.filter(username=nom_util).exists() or User.objects.filter(email=email_util).exists():
            messages.error(request, "Cet utilisateur existe déjà.")
            return redirect('liste')

        # Créer un nouvel utilisateur
        utilisateur = User.objects.create_user(username=nom_util, email=email_util, password=pass_util)

        # Vérifier le rôle et définir is_superuser
        if role_util == 'admin':
            utilisateur.is_superuser = True
            utilisateur.is_staff = True  # Assurez-vous que l'utilisateur peut accéder à l'admin
        else:
            # Si le rôle est 'utilisateur', vous pouvez ajouter des paramètres par défaut
            utilisateur.is_superuser = False
            utilisateur.is_staff = False

        utilisateur.save()  # Sauvegarder les changements

        # Ajouter une image de profil si elle est fournie
        UserProfile.objects.create(user=utilisateur, image=img, role=role_util)

        messages.success(request, "Utilisateur ajouté avec succès!")
        return redirect('liste')

    return render(request, 'admini/liste_util.html')

# Vue pour modifier un utilisateur existant
@user_passes_test(is_admin, login_url='login_admin')
def modifier_utilisateur(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=utilisateur)

    if request.method == 'POST':
        nom_util = request.POST.get('name')
        email_util = request.POST.get('email')
        pass_util = request.POST.get('pass')
        img = request.FILES.get('image')
        role = request.POST.get('role')  # Récupération du rôle depuis le formulaire

        # Mettre à jour les informations de l'utilisateur
        utilisateur.username = nom_util
        utilisateur.email = email_util

        if pass_util:
            utilisateur.set_password(pass_util)  # Mise à jour du mot de passe

        if img:
            user_profile.image = img
            user_profile.save()

        # Mise à jour du rôle de l'utilisateur
        if role == 'admin':
            utilisateur.is_superuser = True
            utilisateur.is_staff = True  # Optionnel : si vous souhaitez que l'admin soit aussi staff
        else:
            utilisateur.is_superuser = False
            utilisateur.is_staff = False

        utilisateur.save()

        messages.success(request, "Utilisateur modifié avec succès!")
        return redirect('liste')

    return render(request, 'admini/liste_util.html', {'utilisateur': utilisateur})

@user_passes_test(is_admin, login_url='login_admin')
def modifier_profil_admin(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    # Vérifier si l'utilisateur a un profil
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        pass_admin = request.POST.get('password')
        # Mettre à jour les informations de l'administrateur
        user.username = username
        user.email = email
        
           #verifier si le mot de pass est forni
        if pass_admin:
            user.set_password(pass_admin)
        user.save()

        # Mettre à jour l'image de profil de l'administrateur
        admin_profile = user.userprofile
        if image:
            admin_profile.image = image
        admin_profile.save()
        # Mettre à jour la session pour éviter la déconnexion après le changement de mot de passe
        update_session_auth_hash(request, user)
        messages.success(request, "Profil administrateur mis à jour avec succès!")
        #return redirect(None)  # Redirige vers la page d'accueil après modification

  # Vous pouvez retourner une réponse HTTP 204 No Content pour indiquer que tout s'est bien passé
        return HttpResponse(status=204)

    # Si la méthode n'est pas POST, vous n'avez pas besoin de faire quoi que ce soit.
    return HttpResponse(status=400)  # Ou un autre statut si nécessaire


#suprimer données selectionner de l'historique
#@login_required(login_url='login_util')
def delete_selected(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('items_to_delete')
        models.DHTData.objects.filter(id__in=item_ids).delete()
        messages.success(request, "Données sélectionnées supprimées avec succès!")
        return redirect('histo')  # Redirige vers la vue d'affichage des données
    return redirect('histo')

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile  # Assurez-vous que UserProfile est importé correctement


@user_passes_test(is_admin, login_url='login_admin')
def historique_esp(request, esp_id):
        # Récupérer l'image de profil de l'administrateur connecté
    admin = request.user
    try:
        admin_profile = admin.userprofile  # Profil de l'administrateur
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si l'administrateur n'a pas de profil
    # Récupérer l'utilisateur sélectionné
    esp = get_object_or_404(models.ESP, id=esp_id)

    # Récupérer les données DHTData de l'utilisateur sélectionné
    esp_data = models.DHTData.objects.filter(esp=esp).order_by('-timestamp')

    return render(request, 'admini/historique_esp.html', {
        'esp':esp,
        'esp_data': esp_data,
        'admin_profile': admin_profile,  # Profil de l'administrateur
        'administrateur':request.user
    })
from Administrateur.forms import Esp_forms


from Administrateur import models
def liste_ESP(request):
    # Récupérer l'image de profil de l'administrateur connecté
    admin = request.user
    try:
        admin_profile = admin.userprofile  # Profil de l'administrateur
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si l'administrateur n'a pas de profil
        
    if request.method == 'POST':
        form = Esp_forms(request.POST)
        if form.is_valid():
            dht_data = form.save(commit=False)
            #dht_data.user = request.user
            dht_data.save()
            return redirect('liste_esp')  # Redirige vers une page où les données sont affichées
    else:
        form = Esp_forms()
    # Récupérer toutes les données de la base de données
    all_esp = models.ESP.objects.all().order_by('-id')
  
    #profil = models.UserProfile.objects.get(user=request.user)
    return render(request, 'admini/liste_esp.html', {'all_esp': all_esp,
                                                     'form': form,
                                                    'admin_profile': admin_profile,  # Profil de l'administrateur
                                                    'administrateur':request.user})

def modifier_esp(request, esp_id):
        # Récupérer l'image de profil de l'administrateur connecté
    admin = request.user
    try:
        admin_profile = admin.userprofile  # Profil de l'administrateur
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si l'administrateur n'a pas de profil
    esp = get_object_or_404(models.ESP, id=esp_id)  # Récupère l'appareil
    if request.method == 'POST':
        form = Esp_forms(request.POST, instance=esp)  # Pré-remplit le formulaire avec l'appareil
        if form.is_valid():
            form.save()
            return redirect('liste_esp')  # Redirige après modification
    else:
        form = Esp_forms(instance=esp)  # Affiche le formulaire pré-rempli
    
    all_esp = models.ESP.objects.all().order_by('-id')
    
    return render(request, 'admini/liste_esp.html', {'all_esp': all_esp, 'form': form, 'admin_profile': admin_profile,  # Profil de l'administrateur
                                                    'administrateur':request.user})


def supre_esp(request, esp_id):
    esp = get_object_or_404(models.ESP, id=esp_id)
    esp.delete()
    messages.success(request, "Suppression succès!")
    return redirect('liste_esp')

from django.shortcuts import redirect
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import redirect
from django.utils import translation
from .models import UserProfile

def set_langue(request):
    if request.method == 'POST':
        langue = request.POST.get('language', 'fr')
        translation.activate(langue)
        request.session['django_language'] = langue
        
        # Mettre à jour la langue préférée de l'utilisateur
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.langue_preferée = langue
            user_profile.save()

        next_url = request.POST.get('next', '/')
        return redirect(next_url)
    return redirect('/')

from weasyprint import HTML
def download_pdf(request, esp_id):
    esp = get_object_or_404(models.ESP, id=esp_id)
    esp_data = models.DHTData.objects.filter(esp=esp)

    # Créez le contenu HTML pour le PDF
    html_string = render(request, 'admini/pdf_template.html', {'esp': esp, 'esp_data': esp_data}).content.decode('utf-8')

    # Générer le PDF
    pdf_file = HTML(string=html_string).write_pdf()

    # Envoyer le PDF comme réponse HTTP avec l'en-tête Content-Disposition pour forcer le téléchargement
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historique_{esp.lieu}.pdf"'
    return response