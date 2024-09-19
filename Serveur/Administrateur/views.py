
#from gettext import translation
from django.conf import settings
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
# Create your views here.
from django.utils.translation import gettext as _

def is_admin(user):
    return user.is_staff  # Vérifie si l'utilisateur est un administrateur

@user_passes_test(is_admin, login_url='login_admin')
def ajouteUtil(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
        
    if request.method == 'POST':
        uname = request.POST.get('name')
        uemail = request.POST.get('email')
        upass = request.POST.get('pass')
        image = request.FILES.get('image')  # Récupérer le fichier image
        
        if not uname or not uemail or not upass: #verification si le champ est vide
            messages.error(request, _("Veuillez remplir tous les champs!"))
            return redirect('ajouter')
        else:
            if not User.objects.filter(username=uname).exists(): 
                utilisateur = User.objects.create_user(uname, uemail, upass)
                utilisateur.save()

                # Créer un profil utilisateur avec l'image
                UserProfile.objects.create(user=utilisateur, image=image)

                messages.success(request, _("Utilisateur créé avec succès!"))
                return redirect('ajouter')
            else:
                messages.error(request, _("Nom d'utilisateur existe déjà!"))
    return render(request, 'admini/Ajoute.html',{'admin_profile': admin_profile,
                                                  'administrateur': user})
    
    
@user_passes_test(is_admin, login_url='login_admin')
def liste_util(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    # Récupérer toutes les données de la base de données, y compris le profil utilisateur
    all_data = User.objects.filter(is_superuser=False).select_related('userprofile').order_by('-id')
    return render(request, 'admini/liste_util.html', {'all_data': all_data,
                                                    'admin_profile': admin_profile,
                                                  'administrateur': user})

@user_passes_test(is_admin, login_url='login_admin')
def courbe_admin(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    return render(request, 'admini/courbe.html', {'admin_profile': admin_profile,
                                                  'administrateur': user})


@user_passes_test(is_admin, login_url='login_admin')
def jauge_admin(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    return render(request, 'admini/jauge.html', {'admin_profile': admin_profile,
                                                  'administrateur': user})

@user_passes_test(is_admin, login_url='login_admin')
def bar_admin(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    return render(request, 'admini/Bar.html', {'admin_profile': admin_profile,
                                                  'administrateur': user})

def historique_admin(request):
    user = request.user  # Utilisateur actuellement connecté
    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        admin_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si aucun profil n'existe, définir sur None
    # Récupérer toutes les données de la base de données
    all_data = models.DHTData.objects.all().order_by('-timestamp')
  
    return render(request, 'admini/historique.html', {'all_data': all_data,
                                                    'admin_profile': admin_profile,
                                                    'administrateur': user})

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
                    return redirect('courbe_admin') #ouvrir la paged'admin
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

@user_passes_test(is_admin, login_url='login_admin')
def modifier_util(request, user_id):
    # Récupérer l'utilisateur sélectionné pour la modification
    util = get_object_or_404(User, id=user_id)
    
    # Récupérer ou créer un profil pour l'utilisateur sélectionné
    user_profile, created = UserProfile.objects.get_or_create(user=util)

    # Récupérer l'image de profil de l'administrateur connecté
    admin = request.user
    try:
        admin_profile = admin.userprofile  # Profil de l'administrateur
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si l'administrateur n'a pas de profil

    if request.method == 'POST':
        nom_util = request.POST.get('username')
        email_util = request.POST.get('email')
        pass_util = request.POST.get('password')
        nv_img = request.FILES.get('new_image')  # Récupérer la nouvelle image

        # Mettre à jour les informations de l'utilisateur sélectionné
        util.username = nom_util
        util.email = email_util

        # Vérifier si le mot de passe est fourni
        if pass_util:
            util.set_password(pass_util)

        # Vérifier si une nouvelle image est téléchargée
        if nv_img:
            user_profile.image = nv_img
            user_profile.save()

        util.save()
        messages.success(request, "L'utilisateur a été modifié avec succès!")
        return redirect('liste')

    return render(request, 'admini/modifier.html', {
        'utilisateur': util,
        'user_profile': user_profile,  # Profil de l'utilisateur sélectionné
        'admin_profile': admin_profile  # Profil de l'administrateur
    })


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
        return redirect('profil_admin')  # Redirige vers la page d'accueil après modification

    return render(request, 'admini/modifier_profil.html', {'user': user,
                                                           'administrateur': user,
                                                           'user_profile': admin_profile,})


#suprimer données selectionner de l'historique
#@login_required(login_url='login_util')
def delete_selected(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('items_to_delete')
        models.DHTData.objects.filter(id__in=item_ids).delete()
        messages.success(request, "Données sélectionnées supprimées avec succès!")
        return redirect('histo')  # Redirige vers la vue d'affichage des données
    return redirect('histo')

from django.shortcuts import redirect
from django.utils import translation

def set_language(request):
    user_language = request.POST.get('language', 'en')
    translation.activate(user_language)
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    return response

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile  # Assurez-vous que UserProfile est importé correctement

"""
def modifier_util(request, user_id):
    util = get_object_or_404(User, id=user_id)
    user_profile = UserProfile.objects.filter(user=util).first()  # Récupérer le profil de l'utilisateur
    if request.method == 'POST':
        nom_util = request.POST.get('username')
        email_util = request.POST.get('email')
        pass_util = request.POST.get('password')
        nv_img = request.FILES.get('new_image')  # Récupérer la nouvelle image
        util.username = nom_util  # Mettre à jour le nom
        util.email = email_util  # Mettre à jour l'email

        # Vérifier si le mot de passe est fourni
        if pass_util:
            util.set_password(pass_util)

        # Vérifier si une nouvelle image est téléchargée
        if nv_img:
            if user_profile:
                user_profile.image = nv_img
            else:
                user_profile = UserProfile(user=util, image=nv_img)
            user_profile.save()

        util.save()
        messages.success(request, "L'utilisateur a été modifié avec succès!")
        return redirect('liste')
    return render(request, 'admini/modifier.html', {'utilisateur': util,
                                                    'user_profile': user_profile})
"""

@user_passes_test(is_admin, login_url='login_admin')
def historique_utilisateur(request, user_id):
        # Récupérer l'image de profil de l'administrateur connecté
    admin = request.user
    try:
        admin_profile = admin.userprofile  # Profil de l'administrateur
    except UserProfile.DoesNotExist:
        admin_profile = None  # Si l'administrateur n'a pas de profil
    # Récupérer l'utilisateur sélectionné
    utilisateur = get_object_or_404(User, id=user_id)

    # Récupérer les données DHTData de l'utilisateur sélectionné
    user_data = models.DHTData.objects.filter(user=utilisateur).order_by('-timestamp')

    return render(request, 'admini/historique_utilisateur.html', {
        'utilisateur': utilisateur,
        'user_data': user_data,
        'admin_profile': admin_profile  # Profil de l'administrateur
    
    })
