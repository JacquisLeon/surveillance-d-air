# views.py
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from Administrateur import models
from django.contrib.auth import update_session_auth_hash  # Import supplémentaire pour garder la session active

#Identifier les donnée pour un utilisateur
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def acceil(request):
    # Récupérer le profil de l'utilisateur connecté
    profil = models.UserProfile.objects.get(user=request.user)
    return render(request, 'Util/Acceil.html',{'utilisateur': request.user,
        'profil': profil,})

from django.http import JsonResponse
import json
from Administrateur.models import DHTData
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            # Chargement des données envoyées dans la requête POST
            data = json.loads(request.body)
            esp_id = data.get('esp_id')
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            gaz = data.get('gaz')
            incendie = data.get('feux')

            # Conversion du champ 'feux' en une chaîne lisible
            feux = "Oui" if incendie == 1 else "Non"
            
            # Trouver l'ESP correspondant à l'ID
            try:
                esp = models.ESP.objects.get(id=esp_id)
            except models.ESP.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'ESP not found'}, status=400)

            # Afficher les données dans le terminal (facultatif pour debug)
            print(f"ESP : {esp_id}, Température : {temperature}°C, Humidité : {humidity}%, Gaz : {gaz}ppt, Feux : {feux}")

            # Créer un nouvel enregistrement dans la table DHTData pour cet ESP
            dht_data = DHTData.objects.create(
                esp=esp,  # Associer les données à l'ESP correspondant
                temperature=temperature,
                humidity=humidity,
                gaz=gaz,
                feux=feux
            )

            # Retourner une réponse JSON indiquant le succès
            return JsonResponse({'status': 'success', 'temperature': temperature, 'humidity': humidity, 'gaz': gaz, 'feux': feux})
        except json.JSONDecodeError:
            # Retourner une erreur si les données sont mal formatées
            return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)
    # Retourner une erreur si la requête n'est pas POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

#courbe pour esp id
"""
@login_required(login_url='login_util')
def courbe_data(request, esp_id=None):
    if esp_id:
        # récupérer les données pour cet ESP
        esp = ESP.objects.get(id=esp_id)
        latest_data = DHTData.objects.filter(esp=esp).last()
    else:
        # par défaut, prendre les données du premier ESP de l'utilisateur
        esp = ESP.objects.filter(user=request.user).first()
        latest_data = DHTData.objects.filter(user=request.user).last()

    profil = models.UserProfile.objects.get(user=request.user)

    return render(request, 'Util/courbe.html', {
        'dht_data': latest_data,
        'utilisateur': request.user,
        'profil': profil,
        'esp_id': esp.id  # Passer l'ID de l'ESP au template
    })"""
def courbe_data(request, esp_id):
    esp = get_object_or_404(models.ESP, id=esp_id)
    # Récupérer le profil de l'utilisateur connecté
    profil = models.UserProfile.objects.get(user=request.user)
    # Récupérez les données de DHTData sans utiliser le champ esp
    data = DHTData.objects.last()  # Ou appliquez d'autres filtres si nécessaire
    # Préparez les données pour votre template
    context = {
        'data': data,
        'esp': esp,
        'esp_id': esp_id,  # Ajoutez esp_id ici
        'utilisateur': request.user,
        'profil': profil,
    }
    return render(request, 'Util/courbe.html', context)
    #utilisateur a son propre donnée
@login_required(login_url='login_util')

def bar_data(request, esp_id):
    esp = get_object_or_404(models.ESP, id=esp_id)
    # Récupérer les dernières données de l'utilisateur connecté
    data = DHTData.objects.last()
    # Récupérer le profil de l'utilisateur connecté
    profil = models.UserProfile.objects.get(user=request.user)
    return render(request, 'Util/bar.html', {
        'data': data,
        'esp': esp,
        'esp_id': esp_id,
        'utilisateur': request.user,
        'profil': profil,
    })
    #utilisateur a son propre donnée
@login_required(login_url='login_util')

def jauge_data(request, esp_id):
    esp = get_object_or_404(models.ESP, id=esp_id)
    # Récupérer les dernières données de l'utilisateur connecté
    data = DHTData.objects.last()
    # Récupérer le profil de l'utilisateur connecté
    profil = models.UserProfile.objects.get(user=request.user)
    return render(request, 'Util/jauge.html', {
        'data': data,
        'esp': esp,
        'esp_id': esp_id,
        'utilisateur': request.user,
        'profil': profil,
    })
    #ESP correspond au id
from django.http import JsonResponse


import logging
from django.http import JsonResponse


logger = logging.getLogger(__name__)
#Pour l'ajax rechercher de mise a jour des données dans la base
def get_data(request, esp_id):
    logger.info(f"Request for esp_id: {esp_id}")
    try:
        last_data = DHTData.objects.filter(esp_id=esp_id).last()
        if last_data:
            data = {
                'temperature': last_data.temperature,
                'humidity': last_data.humidity,
                'gaz': last_data.gaz
                
            }
            logger.info(f"Data found: {data}")
        else:
            data = {
                'temperature': None,
                'humidity': None,
                'gaz': None
            }
            logger.warning(f"No data found for esp_id: {esp_id}")
    except Exception as e:
        logger.error(f"Error retrieving data: {str(e)}")
        data = {
            'error': str(e)
        }
    
    return JsonResponse(data)


#historique pour l'eps correspond au id
@login_required(login_url='login_util')
def historique_data(request, esp_id):
    # Récupérer l'ESP correspondant à l'ID
    esp = get_object_or_404(models.ESP, id=esp_id)

    # Récupérer les données associées à cet ESP
    esp_data = DHTData.objects.filter(esp=esp).order_by('-timestamp')

    # Récupérer le profil de l'utilisateur connecté
    try:
        profil = models.UserProfile.objects.get(user=request.user)
    except models.UserProfile.DoesNotExist:
        profil = None

    return render(request, 'Util/historique.html', {
        'all_data': esp_data,  # Affiche uniquement les données de l'ESP sélectionné
        'profil': profil,
        'utilisateur': request.user,
        'esp': esp,
    })


    
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Utilisateur.forms import DHTDataForm

#ajouter donnée au interface
@login_required
def add_dht_data(request):
    if request.method == 'POST':
        form = DHTDataForm(request.POST)
        if form.is_valid():
            dht_data = form.save(commit=False)
            dht_data.user = request.user
            dht_data.save()
            return redirect('historique')  # Redirige vers une page où les données sont affichées
    else:
        form = DHTDataForm()
    
    return render(request, 'Util/add_dht_data.html', {'form': form})

"""
recevoire de donnée combiner
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            gaz = data.get('gaz')
            incendie = data.get('feux')
            if incendie==1:
                feux = "Oui"
            else:
                feux = "Non"
            
            # Afficher les données dans le terminal
            print(f"Température : {temperature}°C, Humidité : {humidity}% , Gaz : {gaz}mg/L, Feux: {feux}")
            
            # Enregistrer les données dans la base de données
            dht_data = DHTData(temperature=temperature, humidity=humidity, gaz=gaz ,feux=feux)
            dht_data.save()

            return JsonResponse({'status': 'success', 'temperature': temperature, 'humidity': humidity, 'gaz': gaz, 'feux': feux})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
"""

"""
#utilisateur combiner a un donner
@login_required(login_url='login_util') #verroullage
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


def get_data(request):#pour le graphe avec ajax
    latest_data = DHTData.objects.last()
    if latest_data:
        data = {
            'temperature': latest_data.temperature,
            'humidity': latest_data.humidity,
            'gaz': latest_data.gaz,
            'timestamp': latest_data.timestamp
        }
    else:
        data = {
            'temperature': None,
            'humidity': None,
            'gaz': None,
        }
    return JsonResponse(data)
"""
"""
#historique combiner
@login_required(login_url='login_util') #verroullage
def display_data(request):
    # Récupérer toutes les données de la base de données
    all_data = DHTData.objects.all().order_by('-timestamp')
     # Récupérer le profil de l'utilisateur connecté
    profil = models.UserProfile.objects.get(user=request.user)
    return render(request, 'Util/historique.html', {'all_data': all_data,
                                                    'profil': profil,
                                                    'utilisateur': request.user,})
"""

def login_util(request):
    if request.method == 'POST':
        nm = request.POST.get('name')
        pwd = request.POST.get('pass')
        if not nm or not pwd:
            messages.error(request, "Veuillez remplir tous les champs!")
        
        else:
            user = authenticate(request,username=nm,password=pwd)
            if user is not None:
                login(request,user)
                return redirect('acceil')
            else:
                messages.error(request,"Nom d'utilisateur ou mot de passe incorrect!")
    return render(request, 'Util/login.html')

def logout_util(request):
    logout(request)
    return redirect('login_util')

from django.views.decorators.csrf import csrf_exempt



@login_required(login_url='login_util')
def modifier_profil(request):
    utilisateur = request.user  # récupérer l'utilisateur connecté
     # Récupérer le profil de l'utilisateur connecté
    #profil = models.UserProfile.objects.get(user=request.user)
    
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
        #return redirect('P_modifier')
 
    #return render(request, 'Util/modifier.html', {'utilisateur': utilisateur})

# Vous pouvez retourner une réponse HTTP 204 No Content pour indiquer que tout s'est bien passé
        return HttpResponse(status=204)

    # Si la méthode n'est pas POST, vous n'avez pas besoin de faire quoi que ce soit.
    return HttpResponse(status=400)  # Ou un autre statut si nécessaire
#**************************pour android**************************************

from django.http import HttpResponse
import time


@csrf_exempt  # Désactiver CSRF pour les requêtes venant de l'application Android
def login_app(request):
    if request.method == 'POST':
        nm = request.POST.get('name')
        pwd = request.POST.get('pass')
        user = authenticate(request, username=nm, password=pwd)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful'})
        else:
            return JsonResponse({'status': 'error', 'message': "Nom d'utilisateur ou mot de passe incorrect!"}, status=401)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


from django.http import JsonResponse
import random

def random_data(request):
    # Génération de deux ensembles de données aléatoires
    data1 = [random.uniform(10, 100) for _ in range(10)]  # Données pour le LineChart
    data2 = [random.uniform(20, 200) for _ in range(10)]  # Données pour le BarChart

    # Retourne une réponse JSON avec les deux jeux de données
    return JsonResponse({"data1": data1, "data2": data2})


def apk_data(request):
    latest_data = DHTData.objects.last()
    if latest_data:
        data1 = latest_data.temperature,
        data2 = latest_data.humidity,
    else:
        data1 = None,
        data2 = None,
    return JsonResponse({"data1": data1, "data2": data2})
#efa mety f tss sary
"""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
#from .models import UserProfile

@login_required
def user_profile_view(request):
    user = request.user

    # Récupérer le profil de l'utilisateur connecté
    try:
        user_profile = models.UserProfile.objects.get(user=user)
        response_data = {
            'username': user.username,
            'email': user.email,
            'profile_image': request.build_absolute_uri(user_profile.image.url) if user_profile.image else None,
        }
        return JsonResponse(response_data)

    except models.UserProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Profil utilisateur non trouvé'}, status=404)
        """
        
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
#from .models import UserProfile  # Assurez-vous que vous importez UserProfile

@login_required
def user_profile_view(request):
    user = request.user

    # Récupérer le profil de l'utilisateur connecté
    try:
        user_profile = models.UserProfile.objects.get(user=user)
        response_data = {
            'username': user.username,
            'email': user.email,
            'profile_image': request.build_absolute_uri(user_profile.image.url) if user_profile.image else None,
        }
        return JsonResponse(response_data)

    except models.UserProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Profil utilisateur non trouvé'}, status=404)

#recupere historique
# views.py
from django.http import JsonResponse


def dht_data_view(request):
    # Récupérer toutes les données de DHTData
    data = DHTData.objects.all().order_by('-timestamp')  # Trier par date de façon décroissante
    data_list = list(data.values('temperature', 'humidity', 'gaz', 'timestamp'))
    
    # Renvoyer les données sous forme de JSON
    return JsonResponse({'dht_data': data_list})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
#from .models import UserProfile  # Importez votre modèle UserProfile si vous en avez un
from django.core.files.base import ContentFile
import base64
"""
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        # Récupération des données de l'utilisateur
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_image_base64 = request.POST.get('profile_image')

        # Vérification si l'utilisateur est authentifié
        if request.user.is_authenticated:
            user = request.user

            # Mise à jour des données de l'utilisateur
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.set_password(password)  # Change le mot de passe
            user.save()

            # Mise à jour de l'image de profil si fournie
            if profile_image_base64:
                try:
                    format, imgstr = profile_image_base64.split(';base64,') 
                    ext = format.split('/')[-1] 
                    profile_image = ContentFile(base64.b64decode(imgstr), name=f"{user.username}.{ext}")
                    
                    # Assurez-vous que vous avez un champ `image` dans votre modèle UserProfile
                    user_profile = models.UserProfile.objects.get(user=user)
                    user_profile.image = profile_image
                    user_profile.save()
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': "User not authenticated"}, status=401)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
"""
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if request.user.is_authenticated:
            user = request.user

            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.set_password(password)
            user.save()

            # Mise à jour de l'image de profil si fournie
            if 'profile_image' in request.FILES:
                try:
                    profile_image = request.FILES['profile_image']
                    
                    user_profile, created = models.UserProfile.objects.get_or_create(user=user)
                    user_profile.image = profile_image
                    user_profile.save()
                except Exception as e:
                    print(f"Error updating profile image: {e}")
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': "User not authenticated"}, status=401)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

