#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>
#include <MQUnifiedsensor.h>
// Définitions
#define placa "ESP8266"  // Changer pour ESP8266
#define Voltage_Resolution 3.3  // L'ESP8266 fonctionne avec 3.3V
#define pin A0  // Pin analogique de l'ESP8266
#define type "MQ-135"  // MQ135
#define ADC_Bit_Resolution 10  // Résolution ADC pour ESP8266
#define RatioMQ135CleanAir 3.6  // RS / R0 = 3.6 ppm

#define DHTPIN 2      // Pin où le capteur DHT est connecté
#define DHTTYPE DHT22 // Type de capteur
#define Cap_feux 16
// Déclarer le capteur
MQUnifiedsensor MQ135(placa, Voltage_Resolution, ADC_Bit_Resolution, pin, type);

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "ESP";          // Remplace par ton SSID Wi-Fi
const char* password = "12345678"; // Remplace par ton mot de passe Wi-Fi
const char* serverUrl = "http://192.168.4.2:8000/fr/receive/"; // URL de ton serveur Django

WiFiClient client;  // Créer un objet WiFiClient

void setup() {
  Serial.begin(115200);
  pinMode(Cap_feux, INPUT);
  dht.begin();
// **************MQ135********************
  // Définir le modèle mathématique pour calculer la concentration en PPM et la valeur des constantes
  MQ135.setRegressionMethod(1); //_PPM = a * ratio^b

  // Initialiser le capteur MQ
  MQ135.init(); 

  // Routine de calibration
  Serial.print("Calibration en cours, veuillez patienter.");
  float calcR0 = 0;
  for(int i = 1; i <= 10; i++) {
    MQ135.update(); // Mettre à jour les données
    calcR0 += MQ135.calibrate(RatioMQ135CleanAir);
    Serial.print(".");
  }
  MQ135.setR0(calcR0 / 10);
  Serial.println(" fait!");

  if (isinf(calcR0)) {
    Serial.println("Avertissement : Problème de connexion, R0 est infini (circuit ouvert détecté). Veuillez vérifier votre câblage et l'alimentation.");
    while (1);
  }
  if (calcR0 == 0) {
    Serial.println("Avertissement : Problème de connexion trouvé, R0 est zéro (la pin analogique est court-circuitée à la masse). Veuillez vérifier votre câblage et l'alimentation.");
    while (1);
  }

  //Serial.println("** Valeurs du MQ-135 ****");
  //Serial.println("|    CO   |  Alcool |   CO2  |  Toluène  |  NH4  |  Acétone  |");  
//***********************
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
  MQ135.update(); // Mettre à jour les données
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
  MQ135.setA(110.47); MQ135.setB(-2.862); // CO2
  float gaz = (MQ135.readSensor())+400; 
    int feux = digitalRead(Cap_feux);

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Erreur de lecture du capteur DHT");
      return;
    }

    // Créer une requête HTTP POST avec WiFiClient
    http.begin(client, serverUrl);  // Utilise WiFiClient ici
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer 1234"); // Ajoutez l'en-tête d'autorisation

    // Spécifier les données à un utilisateur
    String esp_id = "2";  // Remplacez ceci par un identifiant utilisateur dynamique ou configuré
    String postData = "{\"esp_id\": \"" + esp_id + "\", \"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + ", \"gaz\": " + String(gaz) + ", \"feux\": " + String(feux) + "}";

    int httpResponseCode = http.POST(postData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Réponse du serveur : " + response);
    } else {
      Serial.println("Erreur lors de l'envoi : " + String(httpResponseCode));
    }
/*Serial.print("Co2: ");
Serial.println(gaz);*/
    http.end();
  }

  delay(500); // Envoyer les données toutes les 10 secondes
}

/*
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
  const char* serverUrl = "http://192.168.4.2:8000/fr/receive/"; // URL de ton serveur Django
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
  }*/
  
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
