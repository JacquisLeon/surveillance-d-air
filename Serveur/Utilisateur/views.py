# views.py
from django.utils.translation import gettext as _
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
   # esp_list = models.ESP.objects.all()
   # esp_data = [{'id':esp.id,'latitude': esp.latitude, 'longitude': esp.longitude, 'lieu': esp.lieu} for esp in esp_list]
    esp_list = models.ESP.objects.all()
    esp_data = []
    
    for esp in esp_list:
        dernier_dht = models.DHTData.objects.filter(esp=esp).order_by('-timestamp').first()  # Récupère la dernière donnée pour chaque ESP
        esp_data.append({
            'id': esp.id,
            'latitude': esp.latitude,
            'longitude': esp.longitude,
            'lieu': esp.lieu,
            'feux': dernier_dht.feux if dernier_dht else "N/A"  # Valeur de feux ou N/A si pas de données
        })
    return render(request, 'Util/Acceil.html',{'utilisateur': request.user,
        'profil': profil,
        'esp_list': json.dumps(esp_data)})

from django.http import JsonResponse
import json
from Administrateur.models import DHTData

# Définissez votre token personnalisé ici
CUSTOM_TOKEN = '1234'
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        
        # Vérifiez le token
        if token != f'Bearer {CUSTOM_TOKEN}':
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

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


def courbe_data(request, esp_id):
    esp = get_object_or_404(models.ESP, id=esp_id)
    # Récupérer le profil de l'utilisateur connecté
    profil = models.UserProfile.objects.get(user=request.user)
    # Récupérez les données de DHTData sans utiliser le champ esp
    data = models.DHTData.objects.last()  # Ou appliquez d'autres filtres si nécessaire
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
    data = models.DHTData.objects.last()
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
    data = models.DHTData.objects.last()
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
        last_data = models.DHTData.objects.filter(esp_id=esp_id).last()
        if last_data:
            data = {
                'temperature': last_data.temperature,
                'humidity': last_data.humidity,
                'gaz': last_data.gaz,
                'feux': last_data.feux
                
            }
            logger.info(f"Data found: {data}")
        else:
            data = {
                'temperature': None,
                'humidity': None,
                'gaz': None,
                'feux': None
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
    esp_data = models.DHTData.objects.filter(esp=esp).order_by('-timestamp')

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




def login_util(request):
    if request.method == 'POST':
        nm = request.POST.get('name')
        pwd = request.POST.get('pass')
        if not nm or not pwd:
            messages.error(request, _("Veuillez remplir tous les champs!"))
        
        else:
            user = authenticate(request,username=nm,password=pwd)
            if user is not None:
                login(request,user)
                return redirect('acceil')
            else:
                messages.error(request, _("Nom d'utilisateur ou mot de passe incorrect!"))
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

       # messages.success(request, "Votre profil a été mis à jour avec succès!")
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



def apk_data(request):
    latest_data = models.DHTData.objects.last()
    if latest_data:
        data1 = latest_data.temperature,
        data2 = latest_data.humidity,
    else:
        data1 = None,
        data2 = None,
    return JsonResponse({"data1": data1, "data2": data2})

        
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
###############################################
from django.http import JsonResponse
from Administrateur import models # Assurez-vous d'importer vos modèles
#historique
def get_esp_data(request, esp_id):
    try:
        # Récupérer l'objet ESP correspondant à l'esp_id
        esp = models.ESP.objects.get(id=esp_id)

        # Récupérer les données DHT associées à cet ESP
        esp_data = models.DHTData.objects.filter(esp=esp).order_by('-timestamp')

        # Convertir les données en format JSON
        data = list(esp_data.values('temperature', 'humidity', 'gaz', 'feux', 'timestamp'))

        # Ajouter 'lieu' à chaque entrée de la réponse
        for item in data:
            item['lieu'] = esp.lieu  # Ajouter le lieu de l'ESP aux données

        return JsonResponse(data, safe=False)  # Renvoie les données au format JSON
    except models.ESP.DoesNotExist:
        return JsonResponse({'error': 'ESP not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#Graphique
def get_last_data(request, esp_id):
    try:
        # Récupérer l'ESP correspondant à l'esp_id
        esp = models.ESP.objects.filter(id=esp_id).first()  # Changez DHTData par ESP pour obtenir les données de l'ESP

        if esp:
            last_data = models.DHTData.objects.filter(esp_id=esp_id).last()  # Récupérer la dernière donnée pour cet ESP

            if last_data:
                data = {
                    'temperature': last_data.temperature,
                    'humidity': last_data.humidity,
                    'gaz': last_data.gaz,
                    'feux': last_data.feux,
                    'timestamp': last_data.timestamp,
                    'lieu': esp.lieu  # Récupérer le lieu de l'ESP
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'No data found'}, status=404)
        else:
            return JsonResponse({'error': 'ESP not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
from django.http import JsonResponse
from django.db.models import Max
from Administrateur.models import ESP, DHTData
def get_esp_position(request):
    #esp_data = list(models.ESP.objects.values('id', 'lieu', 'latitude', 'longitude'))
    #return JsonResponse(esp_data, safe=False)
    esp_data = []
    esp_objects = ESP.objects.all()

    for esp in esp_objects:
        last_data = DHTData.objects.filter(esp=esp).order_by('-timestamp').first()  # Récupère la dernière donnée

        esp_info = {
            'id': esp.id,
            'lieu': esp.lieu,
            'latitude': esp.latitude,
            'longitude': esp.longitude,
            'feux': last_data.feux if last_data else 'N/A',  # 'N/A' si pas de données
        }

        esp_data.append(esp_info)

    return JsonResponse(esp_data, safe=False)

def teste_connexion(request):
    # Renvoie une réponse JSON avec un statut 200 pour indiquer que le serveur fonctionne
    return JsonResponse({'status': 'OK'}, status=200)