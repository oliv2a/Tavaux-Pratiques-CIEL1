# 📱 Projet Capteur Température/Humidité
## API PHP + Application Android (App Inventor)

---

# 🎯 OBJECTIF DU PROJET

Créer une application Android qui affiche en temps réel les mesures de température et d'humidité depuis une base de données MySQL via une API PHP.

**Architecture :**
```
┌─────────────┐      ┌──────────┐      ┌──────────┐      ┌──────────────┐
│   Capteur   │─────►│ Arduino/ │─────►│  MySQL   │◄────│ Application  │
│  DHT11/22   │      │   ESP    │      │ Database │     │   Android    │
└─────────────┘      └──────────┘      └──────────┘      └──────────────┘
                                             ▲                    │
                                             │                    │
                                             └────────────────────┘
                                                   API PHP
```

---

# PARTIE 1️⃣ : CRÉER L'API PHP

## Étape 1.1 : Préparer la base de données

### Connexion SSH au Raspberry Pi
```bash
ssh pi@192.168.1.XXX
```

### Créer la base de données (si pas déjà fait)
```bash
sudo mysql -u root -p
```

```sql
CREATE DATABASE IF NOT EXISTS capteur_temp;
USE capteur_temp;

CREATE TABLE IF NOT EXISTS mesures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_heure DATETIME NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    humidite DECIMAL(5,2) NOT NULL,
    INDEX idx_date (date_heure)
);

-- Créer l'utilisateur
CREATE USER IF NOT EXISTS 'pi'@'localhost' IDENTIFIED BY 'raspberry';
GRANT ALL PRIVILEGES ON capteur_temp.* TO 'pi'@'localhost';
FLUSH PRIVILEGES;

-- Insérer une mesure de test
INSERT INTO mesures (date_heure, temperature, humidite) 
VALUES (NOW(), 22.5, 55.0);

EXIT;
```

---

## Étape 1.2 : Créer le fichier API PHP

### Créer le fichier
```bash
sudo nano /var/www/html/api_mesure.php
```

### Code PHP complet
```php
<?php
// ============================================
// API CAPTEUR TEMPÉRATURE/HUMIDITÉ
// Fichier: /var/www/html/api_mesure.php
// ============================================

// En-têtes HTTP pour JSON et CORS
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

// Configuration de la base de données
$host = 'localhost';
$dbname = 'capteur_temp';
$username = 'pi';
$password = 'raspberry';

try {
    // Connexion à MySQL
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Requête SQL : récupérer la dernière mesure
    $stmt = $pdo->query("
        SELECT date_heure, temperature, humidite 
        FROM mesures 
        ORDER BY date_heure DESC 
        LIMIT 1
    ");
    
    // Récupérer le résultat
    $mesure = $stmt->fetch(PDO::FETCH_ASSOC);
    
    // Vérifier si une mesure existe
    if ($mesure) {
        // Réponse de succès
        echo json_encode([
            'success' => true,
            'date_heure' => $mesure['date_heure'],
            'temperature' => $mesure['temperature'],
            'humidite' => $mesure['humidite']
        ], JSON_PRETTY_PRINT);
    } else {
        // Aucune donnée trouvée
        echo json_encode([
            'success' => false,
            'message' => 'Aucune mesure disponible'
        ], JSON_PRETTY_PRINT);
    }
    
} catch (PDOException $e) {
    // Erreur de connexion ou requête
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Erreur serveur: ' . $e->getMessage()
    ], JSON_PRETTY_PRINT);
}
?>
```

### Enregistrer et fermer
```
Ctrl + O  (sauvegarder)
Entrée
Ctrl + X  (quitter)
```

### Définir les permissions
```bash
sudo chmod 644 /var/www/html/api_mesure.php
sudo chown www-data:www-data /var/www/html/api_mesure.php
```

---

## Étape 1.3 : Tester l'API

### Test 1 : Depuis le navigateur
Ouvrir dans un navigateur :
```
http://192.168.1.XXX/api_mesure.php
```
**Remplacez XXX par l'IP de votre Raspberry Pi**

### Réponse attendue (JSON) :
```json
{
    "success": true,
    "date_heure": "2025-12-17 14:30:45",
    "temperature": "22.50",
    "humidite": "55.00"
}
```

### Test 2 : Depuis le terminal
```bash
curl http://192.168.1.XXX/api_mesure.php
```

### Test 3 : Avec les détails HTTP
```bash
curl -i http://192.168.1.XXX/api_mesure.php
```

### Vérifier les logs Apache (en cas d'erreur)
```bash
sudo tail -f /var/log/apache2/error.log
```

---

## Étape 1.4 : API améliorée (OPTIONNEL)

### Version avec historique (dernières 10 mesures)

Créer `/var/www/html/api_historique.php` :

```php
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$host = 'localhost';
$dbname = 'capteur_temp';
$username = 'pi';
$password = 'raspberry';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Récupérer les 10 dernières mesures
    $stmt = $pdo->query("
        SELECT date_heure, temperature, humidite 
        FROM mesures 
        ORDER BY date_heure DESC 
        LIMIT 10
    ");
    
    $mesures = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    if ($mesures) {
        echo json_encode([
            'success' => true,
            'count' => count($mesures),
            'mesures' => $mesures
        ], JSON_PRETTY_PRINT);
    } else {
        echo json_encode([
            'success' => false,
            'message' => 'Aucune mesure disponible'
        ], JSON_PRETTY_PRINT);
    }
    
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Erreur: ' . $e->getMessage()
    ], JSON_PRETTY_PRINT);
}
?>
```

---

# PARTIE 2️⃣ : APPLICATION APP INVENTOR

## Étape 2.1 : Créer le projet

### 1. Se connecter à App Inventor
```
https://appinventor.mit.edu/
```

### 2. Créer un nouveau projet
- Cliquer sur **"Projects"** → **"Start new project"**
- Nom : **"CapteurTemperature"**
- Cliquer sur **"OK"**

---

## Étape 2.2 : Designer (Interface)

### Palette des composants à utiliser

#### **User Interface** (Palette de gauche)
1. **Label** × 5
2. **Button** × 1
3. **HorizontalArrangement** × 3 (optionnel, pour organisation)

#### **Connectivity**
4. **Web** × 1 (renommer en "Web1")

#### **Sensors**
5. **Clock** × 1 (renommer en "Horloge1")

---

### Layout de l'interface

```
┌──────────────────────────────────────────────┐
│  Screen1                                     │
│  BackgroundColor: LightBlue                  │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Label_Titre                           │  │
│  │  Texte: "🌡️ Capteur Météo"            │  │
│  │  Police: Gras, 24                      │  │
│  │  AlignementHorizontal: Centre          │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Label_DateTime                        │  │
│  │  Texte: "Date/Heure: --"               │  │
│  │  Police: 16                            │  │
│  │  CouleurFond: Blanc                    │  │
│  │  Padding: 10                           │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Label_Temperature                     │  │
│  │  Texte: "🌡️ Température: -- °C"       │  │
│  │  Police: Gras, 18                      │  │
│  │  CouleurTexte: Rouge                   │  │
│  │  CouleurFond: Blanc                    │  │
│  │  Padding: 10                           │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Label_Humidite                        │  │
│  │  Texte: "💧 Humidité: -- %"           │  │
│  │  Police: Gras, 18                      │  │
│  │  CouleurTexte: Bleu                    │  │
│  │  CouleurFond: Blanc                    │  │
│  │  Padding: 10                           │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Label_Status                          │  │
│  │  Texte: "Status: En attente..."        │  │
│  │  Police: 14                            │  │
│  │  CouleurTexte: Gris                    │  │
│  │  AlignementHorizontal: Centre          │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │         Bouton_Actualiser              │  │
│  │         Texte: "🔄 Actualiser"         │  │
│  │         CouleurFond: Vert              │  │
│  │         CouleurTexte: Blanc            │  │
│  │         Forme: Arrondi                 │  │
│  │         Largeur: Remplir parent        │  │
│  └────────────────────────────────────────┘  │
│                                              │
└──────────────────────────────────────────────┘

Composants non-visibles (en bas) :
[Web1]  [Horloge1]
```

---

### Configuration des propriétés (Properties)

#### **Screen1**
```
Title: Capteur Température
BackgroundColor: LightBlue (#ADD8E6)
```

#### **Label_Titre**
```
Text: 🌡️ Capteur Météo
FontBold: ✓ (coché)
FontSize: 24
TextAlignment: center (1)
Width: Fill parent
Height: 50 pixels
BackgroundColor: DarkBlue (#00008B)
TextColor: White
```

#### **Label_DateTime**
```
Text: 📅 Date/Heure: --
FontSize: 16
Width: Fill parent
Height: Automatic
BackgroundColor: White
TextColor: Black
```

#### **Label_Temperature**
```
Text: 🌡️ Température: -- °C
FontBold: ✓
FontSize: 18
Width: Fill parent
Height: Automatic
BackgroundColor: White
TextColor: Red (#FF0000)
```

#### **Label_Humidite**
```
Text: 💧 Humidité: -- %
FontBold: ✓
FontSize: 18
Width: Fill parent
Height: Automatic
BackgroundColor: White
TextColor: Blue (#0000FF)
```

#### **Label_Status**
```
Text: Status: En attente...
FontSize: 14
TextAlignment: center (1)
Width: Fill parent
Height: Automatic
TextColor: Gray (#808080)
```

#### **Bouton_Actualiser**
```
Text: 🔄 Actualiser
FontBold: ✓
FontSize: 16
Width: Fill parent
Height: 50 pixels
BackgroundColor: Green (#008000)
TextColor: White
Shape: Rounded (1)
```

#### **Web1** (Composant non-visible)
```
URL: http://192.168.1.XXX/api_mesure.php
(⚠️ REMPLACEZ XXX par votre IP Raspberry Pi !)
```

#### **Horloge1** (Clock - Composant non-visible)
```
TimerInterval: 60000 (= 60 secondes)
TimerEnabled: ✓ (coché)
```

---

## Étape 2.3 : Blocks (Programmation)

### Variable globale

**Créer la variable `json_data` :**
```
Tiroir "Variables" → "Initialiser variable globale"
┌────────────────────────────────────────────┐
│ initialiser variable globale json_data à   │
│   ┌──────────────────────────────────┐     │
│   │ créer dictionnaire vide          │     │
│   └──────────────────────────────────┘     │
└────────────────────────────────────────────┘
```

---

### BLOC 1 : Démarrage automatique au lancement

```
┌───────────────────────────────────────────────────┐
│ quand  Screen1 . Initialize                       │
├───────────────────────────────────────────────────┤
│ faire                                             │
│   ┌───────────────────────────────────────────┐   │
│   │ appeler  Web1 . Get                       │   │
│   └───────────────────────────────────────────┘   │
└───────────────────────────────────────────────────┘
```

**Localisation :**
- Tiroir `Screen1` → `quand Screen1.Initialize`
- Tiroir `Web1` → `appeler Web1.Get`

---

### BLOC 2 : Actualisation manuelle (bouton)

```
┌───────────────────────────────────────────────────┐
│ quand  Bouton_Actualiser . Clic                   │
├───────────────────────────────────────────────────┤
│ faire                                             │
│   ┌───────────────────────────────────────────┐   │
│   │ définir  Label_Status . Texte  à          │   │
│   │   "⏳ Chargement..."                      │   │
│   └───────────────────────────────────────────┘   │
│   ┌───────────────────────────────────────────┐   │
│   │ appeler  Web1 . Get                       │   │
│   └───────────────────────────────────────────┘   │
└───────────────────────────────────────────────────┘
```

**Localisation :**
- Tiroir `Bouton_Actualiser` → `quand Bouton_Actualiser.Clic`
- Tiroir `Label_Status` → `définir Label_Status.Texte à`
- Tiroir `Texte` → bloc texte `"⏳ Chargement..."`
- Tiroir `Web1` → `appeler Web1.Get`

---

### BLOC 3 : Actualisation automatique (horloge)

```
┌───────────────────────────────────────────────────┐
│ quand  Horloge1 . Minuteur                        │
├───────────────────────────────────────────────────┤
│ faire                                             │
│   ┌───────────────────────────────────────────┐   │
│   │ appeler  Web1 . Get                       │   │
│   └───────────────────────────────────────────┘   │
└───────────────────────────────────────────────────┘
```

**Localisation :**
- Tiroir `Horloge1` → `quand Horloge1.Minuteur`
- Tiroir `Web1` → `appeler Web1.Get`

---

### BLOC 4 : Parser et afficher les données JSON (PRINCIPAL)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ quand  Web1 . GotText                                                   │
│   responseCode                                                          │
│   responseType                                                          │
│   responseContent                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│ faire                                                                   │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ si  ┌──────────────────────────────────────┐                    │   │
│   │     │  responseCode  =  200                │                    │   │
│   │     └──────────────────────────────────────┘                    │   │
│   ├─────────────────────────────────────────────────────────────────┤   │
│   │ alors                                                           │   │
│   │   ┌─────────────────────────────────────────────────────────┐   │   │
│   │   │ définir  variable globale  json_data  à                 │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ appeler  Web1 . JsonTextDecode                  │   │   │   │
│   │   │   │   jsonText:  responseContent                    │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   └─────────────────────────────────────────────────────────┘   │   │
│   │                                                                 │   │
│   │   ┌─────────────────────────────────────────────────────────┐   │   │
│   │   │ définir  variable  success  à                           │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ obtenir valeur pour clé  "success"              │   │   │   │
│   │   │   │   dictionnaire:  variable globale json_data     │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   └─────────────────────────────────────────────────────────┘   │   │
│   │                                                                 │   │
│   │   ┌─────────────────────────────────────────────────────────┐   │   │
│   │   │ si  success                                             │   │   │
│   │   ├─────────────────────────────────────────────────────────┤   │   │
│   │   │ alors                                                   │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ définir  Label_DateTime . Texte  à              │   │   │   │
│   │   │   │   ┌─────────────────────────────────────────┐   │   │   │   │
│   │   │   │   │ joindre  "📅 "                          │   │   │   │   │
│   │   │   │   │   ┌─────────────────────────────────┐   │   │   │   │   │
│   │   │   │   │   │ obtenir valeur pour clé         │   │   │   │   │   │
│   │   │   │   │   │   "date_heure"                  │   │   │   │   │   │
│   │   │   │   │   │   dictionnaire: json_data       │   │   │   │   │   │
│   │   │   │   │   └─────────────────────────────────┘   │   │   │   │   │
│   │   │   │   └─────────────────────────────────────────┘   │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   │                                                         │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ définir  Label_Temperature . Texte  à           │   │   │   │
│   │   │   │   ┌─────────────────────────────────────────┐   │   │   │   │
│   │   │   │   │ joindre  "🌡️ Température: "            │   │   │   │   │
│   │   │   │   │   ┌─────────────────────────────────┐   │   │   │   │   │
│   │   │   │   │   │ obtenir valeur pour clé         │   │   │   │   │   │
│   │   │   │   │   │   "temperature"                 │   │   │   │   │   │
│   │   │   │   │   │   dictionnaire: json_data       │   │   │   │   │   │
│   │   │   │   │   └─────────────────────────────────┘   │   │   │   │   │
│   │   │   │   │   " °C"                                 │   │   │   │   │
│   │   │   │   └─────────────────────────────────────────┘   │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   │                                                         │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ définir  Label_Humidite . Texte  à              │   │   │   │
│   │   │   │   ┌─────────────────────────────────────────┐   │   │   │   │
│   │   │   │   │ joindre  "💧 Humidité: "                │   │   │   │   │
│   │   │   │   │   ┌─────────────────────────────────┐   │   │   │   │   │
│   │   │   │   │   │ obtenir valeur pour clé         │   │   │   │   │   │
│   │   │   │   │   │   "humidite"                    │   │   │   │   │   │
│   │   │   │   │   │   dictionnaire: json_data       │   │   │   │   │   │
│   │   │   │   │   └─────────────────────────────────┘   │   │   │   │   │
│   │   │   │   │   " %"                                  │   │   │   │   │
│   │   │   │   └─────────────────────────────────────────┘   │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   │                                                         │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ définir  Label_Status . Texte  à                │   │   │   │
│   │   │   │   "✅ Données actualisées"                      │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ définir  Label_Status . CouleurTexte  à vert    │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   ├─────────────────────────────────────────────────────────┤   │   │
│   │   │ sinon                                                   │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ définir  Label_Status . Texte  à                │   │   │   │
│   │   │   │   "⚠️ Aucune mesure disponible"                 │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ définir  Label_Status . CouleurTexte  à orange  │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   └─────────────────────────────────────────────────────────┘   │   │
│   ├─────────────────────────────────────────────────────────────────┤   │
│   │ sinon                                                           │   │
│   │   ┌─────────────────────────────────────────────────────────┐   │   │
│   │   │ définir  Label_Status . Texte  à                        │   │   │
│   │   │   ┌─────────────────────────────────────────────────┐   │   │   │
│   │   │   │ joindre  "❌ Erreur HTTP "  responseCode        │   │   │   │
│   │   │   └─────────────────────────────────────────────────┘   │   │   │
│   │   └─────────────────────────────────────────────────────────┘   │   │
│   │   ┌─────────────────────────────────────────────────────────┐   │   │
│   │   │ définir  Label_Status . CouleurTexte  à  rouge          │   │   │
│   │   └─────────────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Ordre d'assemblage des blocs (étape par étape)

#### 1. Créer la structure principale
```
Tiroir "Web1" → quand Web1.GotText
```

#### 2. Ajouter le test HTTP
```
Tiroir "Contrôle" → si... alors... sinon
Tiroir "Math" → =
Assembler: responseCode = 200
```

#### 3. Parser le JSON
```
Tiroir "Variables" → définir variable globale json_data à
Tiroir "Web1" → appeler Web1.JsonTextDecode
Connecter: responseContent → jsonText
```

#### 4. Extraire "success"
```
Tiroir "Variables" → définir variable success à
Tiroir "Dictionnaires" → obtenir valeur pour clé... dictionnaire...
Clé: "success"
Dict: json_data
```

#### 5. Tester "success"
```
Tiroir "Contrôle" → si... alors... sinon
Variable: success
```

#### 6. Afficher les données (répéter 3 fois)
```
Pour chaque Label (DateTime, Temperature, Humidite):
  1. Tiroir du Label → définir Label_XXX.Texte à
  2. Tiroir "Texte" → joindre
  3. Ajouter emoji et texte
  4. Tiroir "Dictionnaires" → obtenir valeur pour clé
  5. Ajouter l'unité
```

---

## Étape 2.4 : Test et débogage

### Liste de vérification avant test

- [ ] **Web1.URL** est configurée avec la bonne IP
- [ ] Tous les **labels sont nommés correctement**
- [ ] La **variable json_data** est initialisée
- [ ] Le **Raspberry Pi** est allumé et accessible
- [ ] Le serveur **Apache** fonctionne
- [ ] La **base de données** contient des données
- [ ] L'API PHP répond correctement dans le navigateur

### Test dans l'émulateur

1. Cliquer sur **"Connect"** → **"AI Companion"**
2. Scanner le QR code avec l'application MIT AI2 Companion
3. Tester le bouton "Actualiser"
4. Vérifier l'affichage des données

### Débogage

#### Si aucune donnée ne s'affiche :

**1. Vérifier la connexion réseau**
```
Le téléphone est-il sur le même réseau WiFi que le Raspberry Pi ?
```

**2. Tester l'API dans le navigateur du téléphone**
```
http://192.168.1.XXX/api_mesure.php
```

**3. Ajouter un label de debug**
```
Créer Label_Debug
Dans Web1.GotText, ajouter:
  définir Label_Debug.Texte à responseContent
```

**4. Vérifier les logs Apache**
```bash
sudo tail -f /var/log/apache2/error.log
```

**5. Tester la requête avec curl depuis le Pi**
```bash
curl http://localhost/api_mesure.php
```

---

## Étape 2.5 : Compiler et installer l'APK

### Générer l'APK

1. Cliquer sur **"Build"** (menu du haut)
2. Sélectionner **"Android App (.apk)"**
3. Attendre la compilation (2-5 minutes)
4. Télécharger le fichier `.apk`

### Installer sur Android

#### Méthode 1 : Transfert direct
1. Connecter la tablette au PC via USB
2. Copier le fichier `.apk` vers la tablette
3. Ouvrir le fichier sur la tablette
4. Autoriser l'installation d'applications inconnues
5. Installer l'application

#### Méthode 2 : QR Code
1. Après compilation, App Inventor affiche un QR code
2. Scanner avec la tablette
3. Télécharger et installer

#### Méthode 3 : Email
1. Envoyer l'APK par email
2. Ouvrir l'email sur la tablette
3. Télécharger et installer

---

# PARTIE 3️⃣ : AMÉLIORATIONS POSSIBLES

## Amélioration 1 : Graphiques

### Installer l'extension Chart
1. Dans App Inventor : **"Extensions"** → **"Import extension"**
2. Chercher **"Chart"** ou **"ChartView2D"**
3. Ajouter à votre projet

### Utiliser pour afficher l'historique des températures

## Amélioration 2 : Notifications

### Ajouter des alertes si température anormale

```
si  temperature > 30  ou  temperature < 10
alors
  appeler Notifier1.ShowAlert
    titre: "⚠️ Alerte Température"
    message: "Température anormale détectée !"
```

## Amélioration 3 : Sauvegarde locale

### Utiliser TinyDB pour sauvegarder l'historique

```
appeler TinyDB1.StoreValue
  tag: joindre "mesure_" date_heure
  valueToStore: json_data
```

## Amélioration 4 : Interface améliorée

### Ajouter des icônes météo selon la température
```
si  temperature > 25
  définir Image_Meteo.Picture à "soleil.png"
sinon si temperature < 15
  définir Image_Meteo.Picture à "nuage.png"
```

## Amélioration 5 : Mode sombre

### Bouton pour basculer en mode sombre
```
quand Bouton_ModeSombre.Clic
si mode_sombre
alors
  définir Screen1.BackgroundColor à noir
  définir tous les labels.CouleurTexte à blanc
sinon
  définir Screen1.BackgroundColor à blanc
  définir tous les labels.CouleurTexte à noir
```

---

# PARTIE 4️⃣ : MAINTENANCE ET DÉPANNAGE

## Problèmes courants

### 1. "Erreur HTTP 404"
**Cause :** Fichier API introuvable
**Solution :**
```bash
ls -la /var/www/html/api_mesure.php
# Vérifier que le fichier existe
```

### 2. "Erreur HTTP 500"
**Cause :** Erreur PHP
**Solution :**
```bash
sudo tail -f /var/log/apache2/error.log
# Examiner les erreurs PHP
```

### 3. "Erreur parsing JSON"
**Cause :** Réponse non-JSON de l'API
**Solution :**
- Tester l'API dans le navigateur
- Vérifier les en-têtes HTTP
- Ajouter `JSON_PRETTY_PRINT` dans `json_encode()`

### 4. "Aucune mesure disponible"
**Cause :** Table vide
**Solution :**
```sql
-- Insérer une mesure de test
INSERT INTO mesures (date_heure, temperature, humidite)
VALUES (NOW(), 22.5, 55.0);
```

### 5. "Connection refused"
**Cause :** Apache arrêté
**Solution :**
```bash
sudo systemctl status apache2
sudo systemctl start apache2
```

### 6. Application ne se connecte pas
**Cause :** Mauvaise IP ou réseau différent
**Solution :**
- Vérifier l'IP du Raspberry Pi :
```bash
hostname -I
```
- S'assurer que le téléphone est sur le même réseau WiFi

---

## Commandes utiles

### Redémarrer Apache
```bash
sudo systemctl restart apache2
```

### Voir les logs en temps réel
```bash
sudo tail -f /var/log/apache2/access.log
sudo tail -f /var/log/apache2/error.log
```

### Tester la base de données
```bash
sudo mysql -u pi -p capteur_temp
```
```sql
SELECT * FROM mesures ORDER BY date_heure DESC LIMIT 5;
```

### Vérifier les permissions
```bash
ls -la /var/www/html/api_mesure.php
```

---

# PARTIE 5️⃣ : CHECKLIST FINALE

## ✅ Backend (Raspberry Pi)

- [ ] MySQL installé et fonctionnel
- [ ] Base de données `capteur_temp` créée
- [ ] Table `mesures` créée avec index
- [ ] Utilisateur `pi` avec les droits
- [ ] Au moins une mesure dans la table
- [ ] Apache2 installé et démarré
- [ ] PHP installé (avec extension MySQL)
- [ ] Fichier `/var/www/html/api_mesure.php` créé
- [ ] Permissions correctes (644)
- [ ] API testée dans le navigateur
- [ ] JSON correctement formaté
- [ ] IP du Raspberry Pi notée

## ✅ Frontend (App Inventor)

- [ ] Projet "CapteurTemperature" créé
- [ ] Tous les labels créés et nommés
- [ ] Bouton "Actualiser" créé
- [ ] Composant Web1 ajouté
- [ ] URL de Web1 configurée avec la bonne IP
- [ ] Composant Horloge1 ajouté et configuré
- [ ] Variable globale `json_data` initialisée
- [ ] Bloc Screen1.Initialize créé
- [ ] Bloc Bouton_Actualiser.Clic créé
- [ ] Bloc Horloge1.Minuteur créé
- [ ] Bloc Web1.GotText créé et complet
- [ ] Test dans AI Companion réussi
- [ ] APK généré
- [ ] Application installée sur tablette
- [ ] Application testée et fonctionnelle

---

# 📊 RÉSUMÉ DU FLUX DE DONNÉES

```
┌─────────────────────────────────────────────────────────┐
│                    FLUX COMPLET                         │
└─────────────────────────────────────────────────────────┘

1. [Capteur DHT] mesure Temp & Humidité
              ↓
2. [Arduino/ESP] envoie vers MySQL
              ↓
3. [MySQL] stocke dans table `mesures`
              ↓
4. [Application Android] appuie sur "Actualiser"
              ↓
5. [Web1.Get] envoie requête HTTP vers Raspberry Pi
              ↓
6. [Apache] reçoit la requête
              ↓
7. [api_mesure.php] se connecte à MySQL
              ↓
8. [MySQL] retourne la dernière mesure
              ↓
9. [PHP] encode en JSON
              ↓
10. [Apache] renvoie le JSON
              ↓
11. [Application] reçoit responseContent
              ↓
12. [JsonTextDecode] parse le JSON
              ↓
13. [Labels] affichent les valeurs
              ↓
14. [Utilisateur] voit les données à l'écran
```

---

# 🎓 CONCLUSION

Vous avez maintenant :

✅ Une **API PHP** qui expose les données du capteur
✅ Une **application Android** qui affiche les mesures en temps réel
✅ Un système de **rafraîchissement automatique** toutes les 60 secondes
✅ Une interface **claire et lisible**
✅ Une gestion des **erreurs** robuste

## Prochaines étapes suggérées :

1. Ajouter des **graphiques** pour visualiser l'évolution
2. Implémenter des **alertes** en cas de valeurs anormales
3. Sauvegarder l'**historique** localement
4. Créer une **version web** de l'interface
5. Ajouter d'**autres capteurs** (pression, luminosité, etc.)

---

**Projet réalisé pour Olivier**
**Documentation complète : API PHP + App Inventor**
**Décembre 2024**
