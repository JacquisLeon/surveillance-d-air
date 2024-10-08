
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

def is_admin(user):
    return user.is_staff  # Vérifie si l'utilisateur est un administrateur

@user_passes_test(is_admin, login_url='login_admin')
def ajouteUtil(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        user_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        user_profile = None  # Si aucun profil n'existe, définir sur None
        
    if request.method == 'POST':
        uname = request.POST.get('name')
        uemail = request.POST.get('email')
        upass = request.POST.get('pass')
        image = request.FILES.get('image')  # Récupérer le fichier image

        if not User.objects.filter(username=uname).exists(): 
            utilisateur = User.objects.create_user(uname, uemail, upass)
            utilisateur.save()

            # Créer un profil utilisateur avec l'image
            UserProfile.objects.create(user=utilisateur, image=image)

            messages.success(request, "Utilisateur créé avec succès!")
            return redirect('ajouter')
        else:
            messages.error(request, "Nom d'utilisateur existe déjà!")
    return render(request, 'admini/Ajoute.html',{'user_profile': user_profile,
                                                  'administrateur': user})
    
    
@user_passes_test(is_admin, login_url='login_admin')
def liste_util(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        user_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        user_profile = None  # Si aucun profil n'existe, définir sur None
    # Récupérer toutes les données de la base de données, y compris le profil utilisateur
    all_data = User.objects.filter(is_superuser=False).select_related('userprofile').order_by('-id')
    return render(request, 'admini/liste_util.html', {'all_data': all_data,
                                                    'user_profile': user_profile,
                                                  'administrateur': user})

@user_passes_test(is_admin, login_url='login_admin')
def acceil_admin(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        user_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        user_profile = None  # Si aucun profil n'existe, définir sur None
    return render(request, 'admini/Acceil.html', {'user_profile': user_profile,
                                                  'administrateur': user})


def historique_admin(request):
    user = request.user  # Utilisateur actuellement connecté
    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        user_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        user_profile = None  # Si aucun profil n'existe, définir sur None
    # Récupérer toutes les données de la base de données
    all_data = models.DHTData.objects.all().order_by('-timestamp')
  
    return render(request, 'admini/historique.html', {'all_data': all_data,
                                                    'user_profile': user_profile,
                                                    'administrateur': user})

def login_admin(request):
    if request.method == 'POST':
        nam = request.POST.get('admname')
        ps = request.POST.get('admpass')
        adm = authenticate(request,username=nam,password=ps)
        if adm is not None:
            if adm.is_superuser:
                login(request,adm)
                return redirect('acceil') #ouvrir la paged'admin
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
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        user_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        user_profile = None  # Si aucun profil n'existe, définir sur None
        
    util = get_object_or_404(User, id=user_id)
    if request.method =='POST':
        nom_util = request.POST.get('username')
        email_util = request.POST.get('email')
        pass_util = request.POST.get('password')
        nv_img = request.FILES.get('new_image') #recuperer la nouvelle image
        util.username = nom_util #mettre a jour le nom
        util.email = email_util #mettre a jour l'email
        
         #verifier si le mot de pass est forni
        if pass_util:
            util.set_password(pass_util)
        
        #verifier si une nouvelle image telecharger
        if nv_img:
            user_profile, created = UserProfile.objects.get_or_create(user=util)
            user_profile.image = nv_img
            user_profile.save()
            
        util.save()
        messages.success(request, "L'utilisateur a été modifié avec succès!")
        return redirect('liste')
    return render(request, 'admini/modifier.html',{'utilisateur': util,
                                                 'user_profile': user_profile,
                                                  'administrateur': user})


@user_passes_test(is_admin, login_url='login_admin')
def modifier_profil_admin(request):
    user = request.user  # Utilisateur actuellement connecté

    # Vérifier si l'utilisateur a un profil et récupérer l'image
    try:
        user_profile = user.userprofile  # Récupérer le profil associé
    except UserProfile.DoesNotExist:
        user_profile = None  # Si aucun profil n'existe, définir sur None
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
        user_profile = user.userprofile
        if image:
            user_profile.image = image
        user_profile.save()
        # Mettre à jour la session pour éviter la déconnexion après le changement de mot de passe
        update_session_auth_hash(request, user)
        messages.success(request, "Profil administrateur mis à jour avec succès!")
        return redirect('profil_admin')  # Redirige vers la page d'accueil après modification

    return render(request, 'admini/modifier_profil.html', {'user': user,
                                                           'administrateur': user,
                                                           'user_profile': user_profile,})
