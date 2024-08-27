# views.py

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from .models import DHTData

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
    return render(request, 'Util\graphique.html', {'dht_data': latest_data})

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
    return render(request, 'Util\historique.html', {'all_data': all_data})

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
    return render(request, 'Util\login.html')

def logout_util(request):
    logout(request)
    return redirect('login_util')
