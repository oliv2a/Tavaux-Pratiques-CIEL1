# TP1 - Réalisation d'un capteur de température et humidité connecté

## 📋 Informations générales

**Type d'activité :** Mini-projet  
**Durée :** 10 heures  
**Type d'évaluation :** Mini oral (5 minutes de présentation + 5 minutes de questions), préparer une présentation multimédia

---

## 🎯 Objectifs

À l'issue de ce TP, vous serez capable de :

- Configurer et utiliser un Raspberry Pi Zero
- Interfacer un capteur I2C (BME680)
- Créer et gérer une base de données MySQL
- Développer un script Python pour l'acquisition de données
- Automatiser des tâches avec Crontab
- Créer une interface web en PHP
- Développer une application mobile avec App Inventor

---

## 🛠️ Matériel nécessaire

- **[Raspberry Pi Zero](https://www.raspberrypi.com/products/raspberry-pi-zero-w/)** avec son image système (à préparer; voir tuto )
- **[Capteur de température et humidité BME680](https://wiki.seeedstudio.com/Grove-Temperature_Humidity_Pressure_Gas_Sensor_BME680/) ** (interface I2C)
- **[Carte HUB Grove Base Hat](https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/) **
- **Accès réseau** (WiFi ou Ethernet)
- **Tablette Android** (pour la partie App Inventor)

---

## 📡 Informations de connexion

**Raspberry Pi Zero :**
- **Adresse IP :** Demander au professeur
- **Utilisateur :** pi
- **Mot de passe :** raspberry
- **Protocole :** SSH (port 22)

---

## 📝 Tâches à effectuer

### Partie 1 : Configuration initiale du Raspberry Pi

#### Tâche 1 : Démarrage et vérification
- [ ] Démarrer le Raspberry Pi Zero
- [ ] Vérifier que le système démarre correctement
- [ ] Noter l'adresse IP si elle diffère

#### Tâche 2 : Connexion SSH
- [ ] Ouvrir PuTTY (Windows) ou un terminal (Linux/Mac)
- [ ] Se connecter en SSH à l'adresse IP : `192.168.1.151`
- [ ] Utiliser les identifiants : `pi` / `raspberry`

**Commande Linux/Mac :**
```bash
ssh pi@192.168.1.151
```

#### Tâche 3 : Configuration du proxy du lycée
- [ ] Configurer le proxy pour permettre l'accès internet

**Éditer le fichier de configuration :**
```bash
sudo nano /etc/environment
```

**Ajouter les lignes suivantes (adapter selon votre proxy) :**
```bash
http_proxy="http://proxy.lycee:port/"
https_proxy="http://proxy.lycee:port/"
no_proxy="localhost,127.0.0.1"
```

**Redémarrer pour appliquer :**
```bash
sudo reboot
```

---

### Partie 2 : Installation des services WEB

#### Tâche 4 : Installation et test des services WEB

**Installer Apache2 :**
```bash
sudo apt update
sudo apt install apache2
```

**Installer PHP :**
```bash
sudo apt install php php-mbstring php-mysql
```

**Installer MariaDB (MySQL) :**
```bash
sudo apt install mariadb-server
```

**Installer PHPMyAdmin :**
```bash
sudo apt install phpmyadmin
```

**Vérification :**
- Tester Apache : ouvrir `http://192.168.1.151` dans un navigateur
- Tester PHPMyAdmin : `http://192.168.1.151/phpmyadmin`

**Configurer les droits d'accès :**
```bash
sudo chown -R pi:www-data /var/www/html/
sudo chmod -R 770 /var/www/html/
```

---

### Partie 3 : Configuration du bus I2C

#### Tâche 5 : Activer le bus I2C

**Via raspi-config :**
```bash
sudo raspi-config
```

- Sélectionner : `3 Interface Options`
- Puis : `I5 I2C`
- Choisir : `Yes` pour activer
- Redémarrer si demandé

**Vérifier l'activation :**
```bash
lsmod | grep i2c
```

#### Tâche 6 : Installation des outils I2C

**Installer les outils de détection I2C :**
```bash
sudo apt install i2c-tools python3-smbus
```

**Installer les bibliothèques Python pour le capteur :**
```bash
pip3 install adafruit-circuitpython-ahtx0
```

ou

```bash
sudo apt install python3-pip
pip3 install adafruit-blinka
pip3 install adafruit-circuitpython-ahtx0
```

---

### Partie 4 : Branchement et test du capteur

#### Tâche 7 : Câblage du capteur AHT10

**Schéma de connexion :**

| Pin AHT10 | Pin Raspberry Pi Zero | Description |
|-----------|----------------------|-------------|
| VCC       | Pin 1 (3.3V)         | Alimentation |
| GND       | Pin 6 (GND)          | Masse |
| SDA       | Pin 3 (GPIO 2 - SDA) | Données I2C |
| SCL       | Pin 5 (GPIO 3 - SCL) | Horloge I2C |

**Détection du capteur sur le bus I2C :**
```bash
sudo i2cdetect -y 1
```

Vous devriez voir l'adresse du capteur (généralement `0x38` ou `0x39`).

**Script de test Python :**

Créer le fichier `test_capteur.py` :
```python
import time
import board
import adafruit_ahtx0

# Initialiser le capteur
i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

# Lire et afficher les valeurs
while True:
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    
    print(f"Température: {temperature:.1f}°C")
    print(f"Humidité: {humidity:.1f}%")
    print("-" * 30)
    
    time.sleep(2)
```

**Exécuter le test :**
```bash
python3 test_capteur.py
```

---

### Partie 5 : Création de la base de données

#### Tâche 8 : Création de la BDD et de la table

**Se connecter à MySQL :**
```bash
sudo mysql -u root
```

**Créer la base de données :**
```sql
CREATE DATABASE capteur_temp;
USE capteur_temp;
```

**Créer la table :**
```sql
CREATE TABLE mesures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_heure DATETIME NOT NULL,
    temperature DECIMAL(4,1) NOT NULL,
    humidite DECIMAL(4,1) NOT NULL,
    INDEX(date_heure)
);
```

**Créer un utilisateur pour Python :**
```sql
CREATE USER 'pi'@'localhost' IDENTIFIED BY 'raspberry';
GRANT ALL PRIVILEGES ON capteur_temp.* TO 'pi'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**Vérification :**
```bash
mysql -u pi -p capteur_temp
# Entrer le mot de passe : raspberry
```

```sql
SHOW TABLES;
DESCRIBE mesures;
EXIT;
```

---

### Partie 6 : Programme Python de mesure

#### Tâche 9 : Création du script d'acquisition

**Installer le connecteur MySQL pour Python :**
```bash
pip3 install mysql-connector-python
```

**Créer le fichier `enregistrer_mesure.py` :**
```python
#!/usr/bin/env python3
import time
import board
import adafruit_ahtx0
import mysql.connector
from datetime import datetime

# Configuration de la base de données
db_config = {
    'host': 'localhost',
    'user': 'pi',
    'password': 'raspberry',
    'database': 'capteur_temp'
}

def lire_capteur():
    """Lit les valeurs du capteur AHT10"""
    try:
        i2c = board.I2C()
        sensor = adafruit_ahtx0.AHTx0(i2c)
        
        temperature = round(sensor.temperature, 1)
        humidite = round(sensor.relative_humidity, 1)
        
        return temperature, humidite
    except Exception as e:
        print(f"Erreur lecture capteur: {e}")
        return None, None

def enregistrer_bdd(temperature, humidite):
    """Enregistre les mesures dans la base de données"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        date_heure = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        INSERT INTO mesures (date_heure, temperature, humidite)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(query, (date_heure, temperature, humidite))
        conn.commit()
        
        print(f"[{date_heure}] Enregistré: {temperature}°C, {humidite}%")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Erreur BDD: {e}")
        return False

def main():
    """Fonction principale"""
    print("Acquisition de mesure...")
    
    # Lire le capteur
    temperature, humidite = lire_capteur()
    
    if temperature is not None and humidite is not None:
        # Enregistrer dans la BDD
        if enregistrer_bdd(temperature, humidite):
            print("Mesure enregistrée avec succès!")
        else:
            print("Échec de l'enregistrement")
    else:
        print("Échec de la lecture du capteur")

if __name__ == "__main__":
    main()
```

**Rendre le script exécutable :**
```bash
chmod +x enregistrer_mesure.py
```

**Test unitaire :**
```bash
python3 enregistrer_mesure.py
```

**Vérifier l'enregistrement :**
```bash
mysql -u pi -p capteur_temp -e "SELECT * FROM mesures ORDER BY date_heure DESC LIMIT 5;"
```

---

### Partie 7 : Automatisation avec Crontab

#### Tâche 10 : Configuration de Crontab

**Créer un script shell de lancement :**
```bash
nano /home/pi/lancer_mesure.sh
```

**Contenu du script :**
```bash
#!/bin/bash
cd /home/pi
/usr/bin/python3 /home/pi/enregistrer_mesure.py >> /home/pi/mesure.log 2>&1
```

**Rendre exécutable :**
```bash
chmod +x /home/pi/lancer_mesure.sh
```

**Éditer la crontab :**
```bash
crontab -e
```

**Ajouter la ligne suivante (exécution toutes les minutes) :**
```bash
* * * * * /home/pi/lancer_mesure.sh
```

**Vérifier que la tâche est active :**
```bash
crontab -l
```

**Consulter les logs :**
```bash
tail -f /home/pi/mesure.log
```

**Test unitaire :**
Attendre 2-3 minutes et vérifier que de nouvelles mesures apparaissent dans la BDD.

---

### Partie 8 : Page d'accueil Web

#### Tâche 11 : Création de la page d'accueil PHP

**Créer le fichier `/var/www/html/index.php` :**
```php
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capteur Température et Humidité</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .info-box {
            background-color: #e3f2fd;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            border-left: 4px solid #2196F3;
        }
        .mesure {
            font-size: 24px;
            font-weight: bold;
            color: #1976D2;
        }
        .date {
            color: #666;
            font-size: 14px;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #2196F3;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        a:hover {
            background-color: #1976D2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌡️ Capteur de Température et Humidité</h1>
        
        <?php
        // Configuration de la connexion à la base de données
        $host = 'localhost';
        $dbname = 'capteur_temp';
        $username = 'pi';
        $password = 'raspberry';
        
        try {
            // Connexion à la base de données
            $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
            // Récupérer la dernière mesure
            $stmt = $pdo->query("
                SELECT date_heure, temperature, humidite 
                FROM mesures 
                ORDER BY date_heure DESC 
                LIMIT 1
            ");
            
            $mesure = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if ($mesure) {
                // Affichage de la date et heure actuelles
                echo '<div class="info-box">';
                echo '<strong>Date et heure actuelles :</strong><br>';
                echo '<span class="date">' . date('d/m/Y H:i:s') . '</span>';
                echo '</div>';
                
                // Affichage de la dernière mesure
                echo '<div class="info-box">';
                echo '<strong>Dernière mesure :</strong><br>';
                echo '<span class="date">Enregistrée le ' . date('d/m/Y à H:i:s', strtotime($mesure['date_heure'])) . '</span><br><br>';
                echo '<span class="mesure">🌡️ Température : ' . $mesure['temperature'] . '°C</span><br>';
                echo '<span class="mesure">💧 Humidité : ' . $mesure['humidite'] . '%</span>';
                echo '</div>';
            } else {
                echo '<div class="info-box">';
                echo '<p>Aucune mesure disponible.</p>';
                echo '</div>';
            }
            
        } catch (PDOException $e) {
            echo '<div class="info-box" style="border-left-color: #f44336; background-color: #ffebee;">';
            echo '<strong>Erreur de connexion à la base de données :</strong><br>';
            echo $e->getMessage();
            echo '</div>';
        }
        ?>
        
        <a href="recherche.php">🔍 Rechercher une mesure</a>
    </div>
</body>
</html>
```

**Test :**
Ouvrir dans un navigateur : `http://192.168.1.151/index.php`

---

### Partie 9 : Page de recherche

#### Tâche 12 : Création de la page de recherche PHP

**Créer le fichier `/var/www/html/recherche.php` :**
```php
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recherche de mesure</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        form {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-top: 10px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            margin-top: 20px;
            padding: 10px 30px;
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #1976D2;
        }
        .resultat {
            background-color: #e8f5e9;
            padding: 20px;
            margin-top: 20px;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }
        .erreur {
            background-color: #ffebee;
            padding: 20px;
            margin-top: 20px;
            border-radius: 5px;
            border-left: 4px solid #f44336;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            color: #2196F3;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Recherche de mesure</h1>
        
        <form method="POST">
            <label>Date (AAAA-MM-JJ) :</label>
            <input type="date" name="date" required value="<?php echo date('Y-m-d'); ?>">
            
            <label>Heure (HH) :</label>
            <input type="number" name="heure" min="0" max="23" required value="<?php echo date('H'); ?>">
            
            <label>Minute (MM) :</label>
            <input type="number" name="minute" min="0" max="59" required value="<?php echo date('i'); ?>">
            
            <label>Seconde (SS) :</label>
            <input type="number" name="seconde" min="0" max="59" required value="0">
            
            <button type="submit">Rechercher</button>
        </form>
        
        <?php
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            // Configuration de la connexion
            $host = 'localhost';
            $dbname = 'capteur_temp';
            $username = 'pi';
            $password = 'raspberry';
            
            try {
                $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
                $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                
                // Récupération et formatage de la date/heure recherchée
                $date = $_POST['date'];
                $heure = str_pad($_POST['heure'], 2, '0', STR_PAD_LEFT);
                $minute = str_pad($_POST['minute'], 2, '0', STR_PAD_LEFT);
                $seconde = str_pad($_POST['seconde'], 2, '0', STR_PAD_LEFT);
                
                $datetime_recherche = "$date $heure:$minute:$seconde";
                
                // Recherche exacte
                $stmt = $pdo->prepare("
                    SELECT date_heure, temperature, humidite 
                    FROM mesures 
                    WHERE date_heure = :datetime
                    LIMIT 1
                ");
                $stmt->execute(['datetime' => $datetime_recherche]);
                $mesure = $stmt->fetch(PDO::FETCH_ASSOC);
                
                if ($mesure) {
                    // Mesure trouvée exactement
                    echo '<div class="resultat">';
                    echo '<h3>✅ Mesure trouvée</h3>';
                    echo '<p><strong>Date et heure :</strong> ' . date('d/m/Y à H:i:s', strtotime($mesure['date_heure'])) . '</p>';
                    echo '<p><strong>🌡️ Température :</strong> ' . $mesure['temperature'] . '°C</p>';
                    echo '<p><strong>💧 Humidité :</strong> ' . $mesure['humidite'] . '%</p>';
                    echo '</div>';
                } else {
                    // Recherche de la mesure juste avant
                    $stmt = $pdo->prepare("
                        SELECT date_heure, temperature, humidite 
                        FROM mesures 
                        WHERE date_heure < :datetime
                        ORDER BY date_heure DESC
                        LIMIT 1
                    ");
                    $stmt->execute(['datetime' => $datetime_recherche]);
                    $mesure_avant = $stmt->fetch(PDO::FETCH_ASSOC);
                    
                    if ($mesure_avant) {
                        echo '<div class="resultat">';
                        echo '<h3>⚠️ Mesure exacte non trouvée</h3>';
                        echo '<p>Mesure la plus proche (juste avant) :</p>';
                        echo '<p><strong>Date et heure :</strong> ' . date('d/m/Y à H:i:s', strtotime($mesure_avant['date_heure'])) . '</p>';
                        echo '<p><strong>🌡️ Température :</strong> ' . $mesure_avant['temperature'] . '°C</p>';
                        echo '<p><strong>💧 Humidité :</strong> ' . $mesure_avant['humidite'] . '%</p>';
                        echo '</div>';
                    } else {
                        echo '<div class="erreur">';
                        echo '<h3>❌ Aucune mesure trouvée</h3>';
                        echo '<p>Pas de valeur mesurée à cette date/heure ou avant.</p>';
                        echo '</div>';
                    }
                }
                
            } catch (PDOException $e) {
                echo '<div class="erreur">';
                echo '<strong>Erreur de connexion :</strong><br>';
                echo $e->getMessage();
                echo '</div>';
            }
        }
        ?>
        
        <a href="index.php">← Retour à l'accueil</a>
    </div>
</body>
</html>
```

**Test :**
Ouvrir dans un navigateur : `http://192.168.1.151/recherche.php`

---

### Partie 10 : Application mobile avec App Inventor

#### Tâche 13 : Création d'une application Android

**Prérequis :**
- Compte sur [App Inventor](https://appinventor.mit.edu)
- Tablette Android connectée au même réseau WiFi

**Étape 1 : Créer une API PHP**

Créer le fichier `/var/www/html/api_mesure.php` :
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
    
    $stmt = $pdo->query("
        SELECT date_heure, temperature, humidite 
        FROM mesures 
        ORDER BY date_heure DESC 
        LIMIT 1
    ");
    
    $mesure = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if ($mesure) {
        echo json_encode([
            'success' => true,
            'date_heure' => $mesure['date_heure'],
            'temperature' => $mesure['temperature'],
            'humidite' => $mesure['humidite']
        ]);
    } else {
        echo json_encode([
            'success' => false,
            'message' => 'Aucune mesure disponible'
        ]);
    }
    
} catch (PDOException $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Erreur: ' . $e->getMessage()
    ]);
}
?>
```

**Test de l'API :**
Ouvrir : `http://192.168.1.151/api_mesure.php`

**Étape 2 : Créer l'application sur App Inventor**

1. Se connecter sur [App Inventor](https://appinventor.mit.edu)
2. Créer un nouveau projet : "CapteurTemperature"
3. **Designer (Interface) :**
   - Ajouter un `Label` pour le titre
   - Ajouter des `Label` pour afficher la date/heure, température, humidité
   - Ajouter un `Button` "Actualiser"
   - Ajouter un composant `Web` (dans Connectivity)
   - Ajouter un `Clock` pour l'actualisation automatique

4. **Blocks (Programmation) :**
   - Au clic sur le bouton : appeler l'URL `http://192.168.1.151/api_mesure.php`
   - Quand `Web.GotText` : parser le JSON et afficher les valeurs
   - Configurer le `Clock` pour actualiser toutes les 60 secondes

**Exemple de blocs simplifié :**
- `When Button1.Click` → `set Web1.Url to "http://192.168.1.151/api_mesure.php"` → `call Web1.Get`
- `When Web1.GotText` → Parser le JSON et mettre à jour les labels

**Installation :**
- Générer l'APK
- Installer sur la tablette Android
- Tester l'application

---

## 📊 Évaluation

### Critères d'évaluation (Mini oral)

**Présentation (5 minutes) :**
- Présentation du projet et de ses objectifs
- Démonstration du fonctionnement (page web + application)
- Explication des choix techniques

**Questions (5 minutes) :**
- Compréhension du code Python
- Fonctionnement du bus I2C
- Gestion de la base de données
- Problèmes rencontrés et solutions apportées

**Barème indicatif :**
- Configuration et câblage : 20%
- Programme Python et BDD : 30%
- Interface web PHP : 25%
- Application mobile : 15%
- Présentation et questions : 10%

---

## 🔧 Dépannage

### Le capteur n'est pas détecté

**Vérifier le câblage :**
```bash
sudo i2cdetect -y 1
```

**Vérifier que l'I2C est activé :**
```bash
lsmod | grep i2c
```

### Erreur de connexion à la BDD

**Vérifier que MySQL fonctionne :**
```bash
sudo systemctl status mariadb
```

**Tester la connexion :**
```bash
mysql -u pi -p capteur_temp
```

### Les mesures ne s'enregistrent pas

**Consulter les logs :**
```bash
tail -f /home/pi/mesure.log
```

**Vérifier que crontab fonctionne :**
```bash
grep CRON /var/log/syslog
```

### La page PHP affiche une erreur

**Vérifier les logs Apache :**
```bash
sudo tail -f /var/log/apache2/error.log
```

**Vérifier les droits :**
```bash
ls -l /var/www/html/
```

---

## 📚 Ressources

### Documentation
- Consulter le dossier `Documents/` du TP
- [Documentation AHT10](https://learn.adafruit.com/adafruit-aht20)
- [Raspberry Pi GPIO](https://pinout.xyz)
- [App Inventor Tutorials](https://appinventor.mit.edu/explore/ai2/tutorials)

### Aide en ligne
- [Forum Raspberry Pi](https://forums.raspberrypi.com)
- [Stack Overflow](https://stackoverflow.com)

---

## ✅ Checklist finale

Avant la présentation, vérifiez que :

- [ ] Le capteur fonctionne correctement
- [ ] Les mesures s'enregistrent toutes les minutes dans la BDD
- [ ] La page d'accueil affiche la dernière mesure
- [ ] La page de recherche fonctionne correctement
- [ ] L'application mobile récupère et affiche les données
- [ ] Vous pouvez expliquer le fonctionnement de chaque partie
- [ ] Vous avez préparé votre présentation orale

---

**Bon courage pour ce mini-projet ! 🚀**
