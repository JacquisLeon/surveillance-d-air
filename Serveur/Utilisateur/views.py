# views.py

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from .models import DHTData
from Administrateur import models
from django.contrib.auth import update_session_auth_hash  # Import supplémentaire pour garder la session active

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            
            # Afficher les données dans le terminal
            print(f"Température : {temperature}°C, Humidité : {humidity}%")
            
            # Enregistrer les données dans la base de données
            dht_data = DHTData(temperature=temperature, humidity=humidity)
            dht_data.save()

            return JsonResponse({'status': 'success', 'temperature': temperature, 'humidity': humidity})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required(login_url='login') #verroullage
def show_data(request):
    # Récupérer les dernières données de la base de données
    latest_data = DHTData.objects.last()
    # Récupérer le profil de l'utilisateur connecté
    profil = models.UserProfile.objects.get(user=request.user)
    return render(request, 'Util/graphique.html', {
        'dht_data': latest_data,
        'utilisateur': request.user,
        'profil': profil,
    })


def get_data(request):
    latest_data = DHTData.objects.last()
    if latest_data:
        data = {
            'temperature': latest_data.temperature,
            'humidity': latest_data.humidity,
            'timestamp': latest_data.timestamp
        }
    else:
        data = {
            'temperature': None,
            'humidity': None
        }
    return JsonResponse(data)

@login_required(login_url='login') #verroullage
def display_data(request):
    # Récupérer toutes les données de la base de données
    all_data = DHTData.objects.all().order_by('-timestamp')
     # Récupérer le profil de l'utilisateur connecté
    profil = models.UserProfile.objects.get(user=request.user)
    return render(request, 'Util/historique.html', {'all_data': all_data,
                                                    'profil': profil,
                                                    'utilisateur': request.user,})

def login_util(request):
    if request.method == 'POST':
        nm = request.POST.get('name')
        pwd = request.POST.get('pass')
        user = authenticate(request,username=nm,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('show_data')
        else:
            messages.error(request,"Nom d'utilisateur ou mot de passe incorrect!")
    return render(request, 'Util/login.html')

def logout_util(request):
    logout(request)
    return redirect('login_util')



@login_required(login_url='login')
def modifier_profil(request):
    utilisateur = request.user  # récupérer l'utilisateur connecté
     # Récupérer le profil de l'utilisateur connecté
    profil = models.UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        non_utilisateur = request.POST.get('username')
        email = request.POST.get('email')
        nv_pass = request.POST.get('password')
        nv_img = request.FILES.get('new_image')
        
        # Mettre à jour le nom et l'email
        utilisateur.username = non_utilisateur
        utilisateur.email = email
        
        # Mettre à jour le mot de passe
        if nv_pass:
            utilisateur.set_password(nv_pass)
        
        # Mettre à jour l'image
        if nv_img:
            user_profile, created = models.UserProfile.objects.get_or_create(user=utilisateur)
            user_profile.image = nv_img
            user_profile.save()
        
        utilisateur.save()
        
        # Mettre à jour la session pour éviter la déconnexion après le changement de mot de passe
        update_session_auth_hash(request, utilisateur)

        messages.success(request, "Votre profil a été mis à jour avec succès!")
        return redirect('P_modifier')
 
    return render(request, 'Util/modifier.html', {'utilisateur': utilisateur,
                                                    'profil': profil})
