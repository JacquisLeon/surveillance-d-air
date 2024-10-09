
  #include <ESP8266WiFi.h>
  #include <ESP8266HTTPClient.h>
  #include <DHT.h>

  #define DHTPIN 2      // n où le capteur DHT est connecté
  #define DHTTYPE DHT22 // Type de capteur
  #define Cap_feux 16
  //String feux;

  DHT dht(DHTPIN, DHTTYPE);

  const int analogPin = A0;
  //const float tensionRef = 5.0;
  //const int resolutionADC = 1023;

  const char* ssid = "ESP";          // Remplace par ton SSID Wi-Fi
  const char* password = "12345678";  // Remplace par ton mot de passe Wi-Fi
  const char* serverUrl = "http://192.168.4.2:8000/receive/"; // URL de ton serveur Django
  //const char* serverUrl = "http://192.168.137.44:8000";
  WiFiClient client;  // Créer un objet WiFiClient

  void setup() {
  Serial.begin(115200);
  pinMode(Cap_feux, INPUT);
  dht.begin();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion au Wi-Fi...");
  }
  Serial.println("Connecté au Wi-Fi");
  }

  void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int gaz = analogRead(analogPin);
   
    int feux = digitalRead(Cap_feux);

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Erreur de lecture du capteur DHT");
      return;
    }

    // Créer une requête HTTP POST avec WiFiClient
    http.begin(client, serverUrl);  // Utilise WiFiClient ici
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer 1234"); // Ajoutez l'en-tête d'autorisation
    //String postData = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + ", \"gaz\": " + String(gaz) + ", \"feux\": " + String(feux) + "}";

    //Specifier les données a un utilisateur
    String esp_id = "2";  // Remplacez ceci par un identifiant utilisateur dynamique ou configuré
    String postData = "{\"esp_id\": \"" + esp_id + "\", \"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + ", \"gaz\": " + String(gaz) + ", \"feux\": " + String(feux) + "}";

    int httpResponseCode = http.POST(postData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Réponse du serveur : " + response);
    } else {
      Serial.println("Erreur lors de l'envoi : " + String(httpResponseCode));
    }

    http.end();
  }

  delay(10000); // Envoyer les données toutes les 10 secondes
  }
  
/*
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>
#include <AESLib.h>  // Bibliothèque pour le chiffrement AES

#define DHTPIN 2      // Pin où le capteur DHT est connecté
#define DHTTYPE DHT22 // Type de capteur
#define Cap_feux 16

DHT dht(DHTPIN, DHTTYPE);

const int analogPin = A0;
const char* ssid = "ESP";          // Votre SSID Wi-Fi
const char* password = "12345678";  // Votre mot de passe Wi-Fi
const char* serverUrl = "http://192.168.4.2:8000/receive/"; // URL de votre serveur Django

WiFiClient client;
AESLib aesLib;  // Instance pour le chiffrement AES

// Clé secrète pour le chiffrement (16 caractères pour AES-128)
byte aes_key[16] = {0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46};

// Vecteur d'initialisation pour AES (nécessaire pour le chiffrement en mode CBC)
byte aes_iv[16] = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46};

void setup() {
  Serial.begin(115200);
  pinMode(Cap_feux, INPUT);
  dht.begin();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion au Wi-Fi...");
  }
  Serial.println("Connecté au Wi-Fi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int gaz = analogRead(analogPin);
    int feux = digitalRead(Cap_feux);

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Erreur de lecture du capteur DHT");
      return;
    }

    // Créer les données en JSON
    String esp_id = "2";
    String postData = "{\"esp_id\": \"" + esp_id + "\", \"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + ", \"gaz\": " + String(gaz) + ", \"feux\": " + String(feux) + "}";

    // Convertir les données en tableau de caractères pour le chiffrement
    char data_to_encrypt[256];
    postData.toCharArray(data_to_encrypt, 256);

    // Crée un tableau pour stocker les données chiffrées
    char encrypted_output[256];
    int data_length = strlen(data_to_encrypt);

    // Chiffrer les données avec AES-128 CBC
    aesLib.encrypt64((byte*)data_to_encrypt, data_length, encrypted_output, aes_key, 128, aes_iv);

    // Convertir les données chiffrées en une chaîne de caractères hexadécimale
    String encryptedData = String(encrypted_output);

    // Créer une requête HTTP POST avec les données chiffrées
    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(encryptedData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Réponse du serveur : " + response);
    } else {
      Serial.println("Erreur lors de l'envoi : " + String(httpResponseCode));
    }

    http.end();
  }

  delay(10000); // Envoyer les données toutes les 10 secondes
}
*/
/*
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "ESP";          // Remplace par ton SSID Wi-Fi
const char* password = "12345678"; // Remplace par ton mot de passe Wi-Fi
const char* serverUrl = "http://192.168.4.2:8000/receive/"; // URL de ton serveur Django

WiFiClient client;

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connexion au Wi-Fi...");
    }
    Serial.println("Connecté au Wi-Fi");
}

void loop() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        
        // Exemple de données à envoyer
        String jsonData = "{\"value\":12}";

        // Envoi des données
        http.begin(client, serverUrl);
        http.addHeader("Content-Type", "application/json");
        http.addHeader("Authorization", "Bearer 1234"); // Ajoutez l'en-tête d'autorisation

        int httpResponseCode = http.POST(jsonData);
        Serial.println("Données envoyées : " + jsonData);
        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println("Réponse du serveur : " + response);
        } else {
            Serial.println("Erreur lors de l'envoi : " + String(httpResponseCode));
        }

        http.end();
    }

    delay(10000); // Envoyer les données toutes les 10 secondes
}
*/
