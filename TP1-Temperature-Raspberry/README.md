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

- [Raspberry Pi Zero](https://www.raspberrypi.com/products/raspberry-pi-zero-w/) avec son image système (à préparer; voir tuto)
- [Capteur de température et humidité BME680](https://wiki.seeedstudio.com/Grove-Temperature_Humidity_Pressure_Gas_Sensor_BME680/) (interface I2C)
- [Carte HUB Grove Base Hat](https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi/)
- [Github Seeed sur le BME680](https://github.com/Seeed-Studio/Seeed_Arduino_BME68x)
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
- [ ] Écrire la carte avec Pi Imager (voir [tutoriel Pi Imager](https://github.com/oliv2a/guides-etudiants/blob/main/tuto-raspberry-pi-imager.md))
- [ ] Démarrer le Raspberry Pi Zero
- [ ] Vérifier que le système démarre correctement
- [ ] Noter l'adresse IP

#### Tâche 2 : Connexion SSH
- [ ] Ouvrir PuTTY (Windows) ou un terminal (Linux/Mac)
- [ ] Se connecter en SSH à l'adresse IP fournie par le professeur
- [ ] Utiliser les identifiants : `pi` / `raspberry`

**Commande Linux/Mac :**
```bash
ssh pi@192.168.1.XXX
```

Remplacez `XXX` par l'adresse IP de votre Raspberry Pi.

#### Tâche 3 : Configuration du proxy du lycée
- [ ] Configurer le proxy pour permettre l'accès internet

**Éditer le fichier de configuration :**
```bash
sudo nano /etc/apt/apt.conf.d/proxy
```

**Ajouter la ligne suivante (adapter selon votre proxy) :**
```bash
Acquire::http::Proxy "http://172.16.160.100:3130";
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
- Tester Apache : ouvrir `http://192.168.1.XXX` dans un navigateur (remplacer par votre IP)
- Tester PHPMyAdmin : `http://192.168.1.XXX/phpmyadmin`

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
sudo apt install i2c-tools python3-pip
pip3 install smbus2
```

---

### Partie 4 : Branchement et test du capteur

#### Tâche 7 : Câblage du capteur BME680

**Schéma de connexion avec Grove Base Hat :**

Si vous utilisez le Grove Base Hat, branchez simplement le capteur BME680 sur l'un des ports I2C de la carte (généralement marqués I2C).

**Détection du capteur sur le bus I2C :**
```bash
sudo i2cdetect -y 1
```

Vous devriez voir l'adresse du capteur BME680 (généralement `0x76` ou `0x77`).

**Script de test Python :**

Le fichier `test_bme680.py` est fourni dans le dossier `Fichiers/`.

**Exécuter le test :**
```bash
cd ~/projet_capteur/Fichiers
python3 test_bme680.py
```

Vous devriez voir s'afficher la température et l'humidité toutes les 2 secondes.

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

**Étape 1 : Créer et activer un environnement virtuel Python**

Un environnement virtuel permet d'isoler les dépendances du projet.

```bash
# Créer l'environnement virtuel dans le dossier du projet
python3 -m venv ~/projet_capteur/venv

# Activer l'environnement virtuel
source ~/projet_capteur/venv/bin/activate
```

Une fois activé, votre prompt devrait afficher `(venv)` au début.

**Étape 2 : Installer le connecteur MySQL pour Python**

**Option A : Installation depuis le fichier fourni (recommandé)**

Si le fichier `.whl` est fourni dans le dossier `Fichiers/` :

```bash
# Se placer dans le dossier du projet
cd ~/projet_capteur

# Installer depuis le fichier local
pip install Fichiers/mysql_connector_python-9.4.0-py2.py3-none-any.whl
```

**Option B : Installation depuis internet**

Si vous avez accès à internet :

```bash
pip install mysql-connector-python
```

**Vérification de l'installation :**

```bash
pip list | grep mysql
```

Vous devriez voir : `mysql-connector-python    9.4.0`

**Étape 3 : Installer les autres dépendances nécessaires**

```bash
# Pour le capteur BME680
pip install smbus2

# Vérifier toutes les installations
pip list
```

**Note importante :** Pour toutes les prochaines sessions, n'oubliez pas d'activer l'environnement virtuel avant de lancer vos scripts :

```bash
source ~/projet_capteur/venv/bin/activate
python3 enregistrer_mesure.py
```

**Pour désactiver l'environnement virtuel :**

```bash
deactivate
```

**Créer le fichier `enregistrer_mesure.py` :**

Ce script utilise le module BME680 du fichier `test_bme680.py` fourni dans le dossier `Fichiers/`.

```python
#!/usr/bin/env python3
"""
Script d'acquisition et d'enregistrement des mesures du BME680
Utilise le module BME680 personnalisé (test_bme680.py)
"""

import sys
import mysql.connector
from datetime import datetime

# Importer la classe BME680 depuis le fichier fourni
sys.path.insert(0, '/home/pi/projet_capteur/Fichiers')
from test_bme680 import BME680

# Configuration de la base de données
db_config = {
    'host': 'localhost',
    'user': 'pi',
    'password': 'raspberry',
    'database': 'capteur_temp'
}

def lire_capteur():
    """Lit les valeurs du capteur BME680"""
    try:
        sensor = BME680()
        temperature, humidite = sensor.read()
        
        # Arrondir à 1 décimale
        temperature = round(temperature, 1)
        humidite = round(humidite, 1)
        
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

**Note importante sur l'import :**

Le script importe la classe `BME680` depuis le fichier `test_bme680.py` situé dans le dossier `Fichiers/`. Assurez-vous que :
- Le fichier `test_bme680.py` est bien présent dans `/home/pi/projet_capteur/Fichiers/`
- Le chemin est correct selon votre structure de projet

**Alternative si les fichiers sont dans le même dossier :**

Si vous placez `test_bme680.py` et `enregistrer_mesure.py` dans le même dossier, simplifiez l'import :

```python
# Remplacer les lignes 9-10 par :
from test_bme680 import BME680
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
nano /home/pi/projet_capteur/lancer_mesure.sh
```

**Contenu du script :**

```bash
#!/bin/bash

# Script de lancement automatique pour les mesures BME680
# Active l'environnement virtuel et exécute le script Python

# Se placer dans le répertoire du projet
cd /home/pi/projet_capteur

# Activer l'environnement virtuel
source /home/pi/projet_capteur/venv/bin/activate

# Exécuter le script Python
python3 /home/pi/projet_capteur/enregistrer_mesure.py >> /home/pi/projet_capteur/mesure.log 2>&1

# Désactiver l'environnement virtuel
deactivate
```

**Rendre le script exécutable :**

```bash
chmod +x /home/pi/projet_capteur/lancer_mesure.sh
```

**Tester le script manuellement :**

Avant de l'ajouter à crontab, vérifiez qu'il fonctionne :

```bash
/home/pi/projet_capteur/lancer_mesure.sh
```

Vérifiez le contenu du log :

```bash
cat /home/pi/projet_capteur/mesure.log
```

**Éditer la crontab :**

```bash
crontab -e
```

**Ajouter la ligne suivante (exécution toutes les minutes) :**

```bash
* * * * * /home/pi/projet_capteur/lancer_mesure.sh
```

**Explication de la syntaxe crontab :**
- `* * * * *` = toutes les minutes (minute, heure, jour, mois, jour de la semaine)
- Suivi du chemin complet vers le script

**Exemples d'autres planifications :**

```bash
# Toutes les 5 minutes
*/5 * * * * /home/pi/projet_capteur/lancer_mesure.sh

# Toutes les 10 minutes
*/10 * * * * /home/pi/projet_capteur/lancer_mesure.sh

# Toutes les heures
0 * * * * /home/pi/projet_capteur/lancer_mesure.sh

# Tous les jours à 8h00
0 8 * * * /home/pi/projet_capteur/lancer_mesure.sh
```

**Vérifier que la tâche est active :**

```bash
crontab -l
```

Vous devriez voir votre ligne avec le script `lancer_mesure.sh`.

**Consulter les logs en temps réel :**

```bash
tail -f /home/pi/projet_capteur/mesure.log
```

Pour arrêter l'affichage : `Ctrl+C`

**Consulter les dernières lignes du log :**

```bash
tail -n 20 /home/pi/projet_capteur/mesure.log
```

**Vider le fichier de log (si nécessaire) :**

```bash
> /home/pi/projet_capteur/mesure.log
```

**Test unitaire :**

1. Attendre 2-3 minutes après l'activation de crontab
2. Vérifier que de nouvelles mesures apparaissent dans la BDD :

```bash
mysql -u pi -p capteur_temp -e "SELECT * FROM mesures ORDER BY date_heure DESC LIMIT 5;"
```

3. Vérifier le fichier de log :

```bash
tail -f /home/pi/projet_capteur/mesure.log
```

**Dépannage si ça ne fonctionne pas :**

**Vérifier que cron est actif :**
```bash
sudo systemctl status cron
```

**Consulter les logs système de cron :**
```bash
grep CRON /var/log/syslog | tail -20
```

**Tester les permissions :**
```bash
ls -l /home/pi/projet_capteur/lancer_mesure.sh
```

Le fichier doit être exécutable (`-rwxr-xr-x`).

**Vérifier que l'environnement virtuel existe :**
```bash
ls -la /home/pi/projet_capteur/venv/bin/activate
```

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
Ouvrir dans un navigateur : `http://192.168.1.XXX/index.php` (remplacer par votre IP)

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
Ouvrir dans un navigateur : `http://192.168.1.XXX/recherche.php` (remplacer par votre IP)

---

### Partie 10 : Application mobile avec App Inventor

#### Tâche 13 : Création d'une application Android

**Prérequis :**
- Compte sur [App Inventor](https://appinventor.mit.edu)
- Tablette Android connectée au même réseau WiFi

**Étape 1 : Créer une API PHP**

Créer le fichier `/var/
www/html/api_mesure.php` :
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
Ouvrir : `http://192.168.1.XXX/api_mesure.php` (remplacer par votre IP)

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
   - Au clic sur le bouton : appeler l'URL `http://192.168.1.XXX/api_mesure.php` (remplacer par votre IP)
   - Quand `Web.GotText` : parser le JSON et afficher les valeurs
   - Configurer le `Clock` pour actualiser toutes les 60 secondes

**Exemple de blocs simplifié :**
- `When Button1.Click` → `set Web1.Url to "http://192.168.1.XXX/api_mesure.php"` (remplacer par votre IP) → `call Web1.Get`
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
tail -f /home/pi/projet_capteur/mesure.log
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

### Tutoriels
- [Comment créer une image Raspberry Pi avec Pi Imager](https://github.com/oliv2a/guides-etudiants/blob/main/tuto-raspberry-pi-imager.md)

### Documentation
- Consulter le dossier `Documents/` du TP
- [Documentation BME680](https://wiki.seeedstudio.com/Grove-Temperature_Humidity_Pressure_Gas_Sensor_BME680/)
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

