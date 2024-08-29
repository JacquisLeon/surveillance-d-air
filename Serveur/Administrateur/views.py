
from django.shortcuts import render, redirect, get_object_or_404
#from .decorators import superuser_required # type: ignore
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import UserProfile  # Importer le modèle UserProfile
# Create your views here.

def ajouteUtil(request):
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
    return render(request, 'admini/Ajoute.html')

def liste_util(request):
    # Récupérer toutes les données de la base de données, y compris le profil utilisateur
    all_data = User.objects.all().select_related('userprofile').order_by('-id')
    return render(request, 'admini/liste_util.html', {'all_data': all_data})

def acceil_admin(request):
    return render(request, 'admini/Acceil.html', {'administrateur':request.user})

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

def logout_admin(request):
    logout(request)
    return redirect('login_admin')

def supre_util(request, user_id):
    util = get_object_or_404(User, id=user_id)
    util.delete()
    messages.success(request, "L'utilisateur a été supprimé avec succès!")
    return redirect('liste')

def modifier_util(request, user_id):
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
    return render(request, 'admini/modifier.html',{'utilisateur': util})