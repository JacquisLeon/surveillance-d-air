# views.py

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

# Variable pour stocker temporairement les données DHT22
dht_data = {'temperature': None, 'humidity': None}

@csrf_exempt
def receive_data(request):
    global dht_data  # Accéder à la variable globale
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            
             # Afficher les données dans le terminal
            print(f"Température : {temperature}°C, Humidité : {humidity}%")
            
            # Stocker les données dans la variable globale
            dht_data['temperature'] = temperature
            dht_data['humidity'] = humidity

            return JsonResponse({'status': 'success', 'temperature': temperature, 'humidity': humidity})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def show_data(request):
    # Passer les données au template pour les afficher
    return render(request, 'index.html', {'dht_data': dht_data})

def get_data(request):
    return JsonResponse(dht_data)