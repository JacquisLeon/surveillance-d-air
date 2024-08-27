
from django.shortcuts import render, redirect
#from .decorators import superuser_required # type: ignore
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
# Create your views here.

def ajouteUtil(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        uemail = request.POST.get('email')
        upass = request.POST.get('pass')
        if not User.objects.filter(username=uname).exists(): 
            utilisateur = User.objects.create_user(uname,uemail,upass)
            utilisateur.save()
            messages.success(request,"Utilisateur créé avec succès!")
            return redirect('ajouter')
        else:
            messages.error(request,"Nom d'utilisateur existe déjà!")
    else:
        messages.warning(request,"Veuillez vérifier le mot de passe!")
    return render(request, 'admini\Ajoute.html')

def liste_util(request):
    # Récupérer toutes les données de la base de données
    all_data = User.objects.all().order_by('-id')
    return render(request, 'admini\liste_util.html', {'all_data': all_data})

def login_admin(request):
    if request.method == 'POST':
        nam = request.POST.get('admname')
        ps = request.POST.get('admpass')
        adm = authenticate(request,username=nam,password=ps)
        if adm is not None:
            if adm.is_superuser:
                login(request,adm)
                return redirect('ajouter') #ouvrir la paged'admin
            else:
                messages.error(request,"Vous n'avez pas les droits administratifs!")
        else:
            messages.error(request,"Nom d'utilisateur ou mot de passe incorrect!")
    return render(request, 'admini\login.html')

def logout_admin(request):
    logout(request)
    return redirect('login_admin')