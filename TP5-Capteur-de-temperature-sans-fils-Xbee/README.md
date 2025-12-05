# TP5 - Création d'un capteur de température avec liaison sans fil XBee

## 📋 Informations générales

**Type d'activité :** Mini-projet  
**Durée :** 10 heures  
**Type d'évaluation :** Compte-rendu d'activité (format numérique en PDF)

---

## 🎯 Objectifs

À l'issue de ce TP, vous serez capable de :

- Configurer la liaison série UART sur Raspberry Pi
- Utiliser des modules XBee pour la communication sans fil
- Interfacer un capteur de température I2C (TCN75A)
- Créer et transmettre des trames de données personnalisées
- Automatiser l'envoi de données avec Cron
- Mesurer et valider des trames série avec un oscilloscope

---

## 🛠️ Matériel nécessaire

- **2 Raspberry Pi** (modèle 3 ou supérieur)
- **2 Cartes Shield XBee pour Raspberry Pi**
- **2 Modules XBee** (série 1 ou 2)
- **1 Capteur de température TCN75A** (I2C)
- **Oscilloscope Analog Discovery 2 (AD2)**
- **Câbles de connexion**
- **Thermomètre de référence** (pour validation)

---

## 📡 Architecture du système

### Schéma du système complet

```
┌─────────┐  L1   ┌──────────┐  L2   ┌─────────┐
│ TCN75A  ├──────►│ Rasp #1  ├──────►│ XBee #1 ├───┐
└─────────┘       └──────────┘       └─────────┘   │
      (I2C)         (I2C+UART)          (UART)      │
                                                    │
                                                    │ L3
                                              (Sans fil)
                                                    │
                                                    │
┌──────────┐  L4   ┌─────────┐                     │
│ Rasp #2  │◄──────┤ XBee #2 │◄────────────────────┘
└──────────┘       └─────────┘
   (UART)            (UART)
```

### Description des liaisons

- **L1** : Liaison I2C entre TCN75A et Raspberry Pi #1 (SDA, SCL)
- **L2** : Liaison UART entre Raspberry Pi #1 et XBee #1 (TX, RX)
- **L3** : Liaison sans fil entre XBee #1 et XBee #2 (2.4 GHz)
- **L4** : Liaison UART entre XBee #2 et Raspberry Pi #2 (TX, RX)

---

## 📝 Tâches à effectuer

### Tâche 1 : Configuration de la liaison série UART

#### Objectif

Configurer et valider la communication série UART sur les deux Raspberry Pi avec des tests unitaires complets.

---

#### Partie A : Configuration du Raspberry Pi #1 (Émetteur)

**Étape 1 : Activer l'UART**

La liaison UART est désactivée par défaut sur Raspberry Pi. Pour l'activer :

```bash
sudo raspi-config
```

1. Sélectionner **Interface Options**
2. Choisir **Serial Port**
3. **Login shell over serial** : `No` (désactiver la console)
4. **Serial port hardware** : `Yes` (activer le port)
5. Redémarrer : `sudo reboot`

**Étape 2 : Vérifier l'activation**

```bash
ls -l /dev/serial*
```

Vous devriez voir :
- `/dev/serial0` → lien vers `/dev/ttyAMA0` (ou `/dev/ttyS0`)

**Étape 3 : Configurer le port série**

Vérifier les paramètres :

```bash
stty -F /dev/serial0
```

Configurer si nécessaire (9600 bauds, 8N1) :

```bash
stty -F /dev/serial0 9600 cs8 -cstopb -parenb
```

---

#### Partie B : Tests unitaires de la liaison

**Test 1 : Envoi d'une trame simple "TEST"**

Créer un script Python `test_uart_tx.py` :

```python
#!/usr/bin/env python3
import serial
import time

# Configuration du port série
port = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

print("Envoi de la trame TEST...")

# Envoi de la trame
trame = "TEST\n"
port.write(trame.encode('utf-8'))
print(f"Trame envoyée : {trame.strip()}")

port.close()
```

Exécuter :

```bash
chmod +x test_uart_tx.py
python3 test_uart_tx.py
```

**Test 2 : Mesure de la trame avec l'AD2**

1. **Connecter l'AD2** :
   - Canal 1+ (orange) : GPIO 14 (TX) - Pin 8
   - GND (noir) : GND - Pin 6

2. **Ouvrir WaveForms**
3. **Logic Analyzer** :
   - Sélectionner UART
   - Baudrate : 9600
   - 8 bits, No parity, 1 stop bit
4. **Capturer** : Lancer l'acquisition
5. **Exécuter** le script Python
6. **Observer** la trame "TEST" décodée

**À documenter :**
- Capture d'écran de WaveForms montrant la trame
- Temps de bit mesuré (≈ 104 µs pour 9600 bauds)
- Caractérisation du signal (niveaux 0V/3.3V)

---

#### Partie C : Configuration du Raspberry Pi #2 (Récepteur)

**Répéter les étapes A1 et A2** sur le Raspberry Pi #2.

**Test 3 : Réception de la trame**

Créer un script `test_uart_rx.py` sur Raspberry Pi #2 :

```python
#!/usr/bin/env python3
import serial

# Configuration du port série
port = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=5
)

print("En attente de réception...")

try:
    while True:
        if port.in_waiting > 0:
            data = port.readline().decode('utf-8').strip()
            print(f"Trame reçue : {data}")
except KeyboardInterrupt:
    print("\nArrêt du programme")
finally:
    port.close()
```

**Test bidirectionnel :**

1. **Rasp #1 → Rasp #2** : Lancer `test_uart_rx.py` sur #2, puis `test_uart_tx.py` sur #1
2. **Rasp #2 → Rasp #1** : Inverser (lancer RX sur #1, TX sur #2)

**À documenter :**
- Captures d'écran des terminaux (envoi et réception)
- Mesures AD2 dans les deux sens
- Débit effectif mesuré

---

### Tâche 2 : Validation du capteur TCN75A

#### Objectif

Mettre en œuvre le capteur de température TCN75A et le valider par des tests comparatifs.

---

#### Partie A : Câblage du TCN75A

**Schéma de connexion (I2C) :**

| Pin TCN75A | Pin Raspberry Pi | Description |
|------------|------------------|-------------|
| VCC        | Pin 1 (3.3V)     | Alimentation |
| GND        | Pin 6 (GND)      | Masse |
| SDA        | Pin 3 (GPIO 2)   | Données I2C |
| SCL        | Pin 5 (GPIO 3)   | Horloge I2C |

**Résistances pull-up :**
- Si le TCN75A n'a pas de pull-up intégrées, ajouter 4.7kΩ entre SDA/VCC et SCL/VCC

**À documenter :**
- Schéma de câblage dessiné (à la main ou sur logiciel)
- Photo du montage réel

---

#### Partie B : Activation de l'I2C

```bash
sudo raspi-config
```

1. **Interface Options** > **I2C** > **Yes**
2. Redémarrer : `sudo reboot`

**Vérifier l'activation :**

```bash
lsmod | grep i2c
```

**Installer les outils I2C :**

```bash
sudo apt install i2c-tools python3-smbus
```

**Détecter le capteur :**

```bash
sudo i2cdetect -y 1
```

Vous devriez voir l'adresse du TCN75A (généralement `0x48`, `0x49`, `0x4A` ou `0x4B`).

---

#### Partie C : Programme de test du TCN75A

Créer le fichier `test_tcn75a.py` :

```python
#!/usr/bin/env python3
import smbus2
import time

# Adresse I2C du TCN75A (à adapter selon votre câblage)
TCN75A_ADDR = 0x48

# Registres
REG_TEMP = 0x00
REG_CONFIG = 0x01

# Initialisation du bus I2C
bus = smbus2.SMBus(1)

def lire_temperature():
    """Lit la température du TCN75A"""
    try:
        # Lire 2 octets du registre température
        data = bus.read_i2c_block_data(TCN75A_ADDR, REG_TEMP, 2)
        
        # Convertir en température
        # Les 12 bits de poids fort contiennent la température
        temp_raw = (data[0] << 4) | (data[1] >> 4)
        
        # Gestion du signe (complément à 2)
        if temp_raw & 0x800:
            temp_raw = temp_raw - 4096
        
        # Conversion en °C (résolution 0.0625°C)
        temperature = temp_raw * 0.0625
        
        return round(temperature, 1)
    
    except Exception as e:
        print(f"Erreur lecture capteur : {e}")
        return None

# Boucle de test
print("=== Test du capteur TCN75A ===\n")

try:
    while True:
        temp = lire_temperature()
        if temp is not None:
            print(f"Température : {temp:5.1f}°C")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n\nArrêt du programme")
finally:
    bus.close()
```

**Exécuter :**

```bash
chmod +x test_tcn75a.py
python3 test_tcn75a.py
```

---

#### Partie D : Validation avec thermomètre de référence

**Procédure :**

1. Laisser stabiliser le capteur TCN75A (5 minutes)
2. Noter la température affichée : **T_TCN75A = _____°C**
3. Placer un thermomètre de référence à proximité (< 5 cm)
4. Noter la température de référence : **T_ref = _____°C**
5. Calculer l'écart : **ΔT = |T_TCN75A - T_ref| = _____°C**

**Test dans différentes conditions :**

| Condition | T_TCN75A | T_ref | ΔT | Validité |
|-----------|----------|-------|-----|----------|
| Ambiante  |          |       |     |          |
| Chauffée (main) |    |       |     |          |
| Refroidie (glaçon) | |       |     |          |

**Critère d'acceptation :** ΔT < 1°C

**À documenter :**
- Tableau des mesures comparatives
- Photos du montage avec thermomètre
- Analyse des écarts

---

### Tâche 3 : Création de la trame de température

#### Objectif

Réaliser un programme Python qui lit la température et crée une trame au format :

```
$NOM-D1D2D3$
```

Où :
- **$** : Caractère de début et fin
- **NOM** : 3 premières lettres du nom de famille en MAJUSCULES
- **D1** : Dizaine de la température
- **D2** : Unité de la température
- **D3** : Décimale de la température (après la virgule)

**Exemples :**
- Température 23.7°C, nom "Dupont" → `$DUP-237$`
- Température 18.2°C, nom "Martin" → `$MAR-182$`
- Température 9.5°C, nom "Bernard" → `$BER-095$`

---

#### Programme complet

Créer le fichier `capteur_temperature_trame.py` :

```python
#!/usr/bin/env python3
"""
Programme de lecture de température TCN75A
et création de trame personnalisée
"""

import smbus2
import time

# Configuration
TCN75A_ADDR = 0x48
REG_TEMP = 0x00
NOM = "WAI"  # Remplacer par les 3 premières lettres de VOTRE nom

# Initialisation I2C
bus = smbus2.SMBus(1)

def lire_temperature():
    """Lit la température du TCN75A"""
    try:
        data = bus.read_i2c_block_data(TCN75A_ADDR, REG_TEMP, 2)
        temp_raw = (data[0] << 4) | (data[1] >> 4)
        
        if temp_raw & 0x800:
            temp_raw = temp_raw - 4096
        
        temperature = temp_raw * 0.0625
        return round(temperature, 1)
    
    except Exception as e:
        print(f"Erreur lecture capteur : {e}")
        return None

def creer_trame(temperature, nom):
    """
    Crée une trame au format $NOM-D1D2D3$
    
    Args:
        temperature (float): Température mesurée
        nom (str): 3 premières lettres du nom
    
    Returns:
        str: Trame formatée
    """
    # Convertir la température en entier (multiplier par 10)
    temp_int = int(temperature * 10)
    
    # Gérer les températures négatives
    if temp_int < 0:
        temp_int = abs(temp_int)
        signe = "-"
    else:
        signe = ""
    
    # Extraire les décimales
    d1 = (temp_int // 100) % 10  # Dizaine
    d2 = (temp_int // 10) % 10   # Unité
    d3 = temp_int % 10            # Décimale
    
    # Créer la trame
    trame = f"${nom.upper()}{signe}-{d1}{d2}{d3}$"
    
    return trame

def main():
    """Fonction principale"""
    print(f"=== Capteur de température avec trame {NOM} ===\n")
    
    try:
        while True:
            # Lire la température
            temp = lire_temperature()
            
            if temp is not None:
                # Créer la trame
                trame = creer_trame(temp, NOM)
                
                # Afficher
                print(f"Température : {temp:5.1f}°C | Trame : {trame}")
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\nArrêt du programme")
    finally:
        bus.close()

if __name__ == "__main__":
    main()
```

**Tester le programme :**

```bash
python3 capteur_temperature_trame.py
```

**Exemple de sortie :**

```
=== Capteur de température avec trame WAI ===

Température :  22.3°C | Trame : $WAI-223$
Température :  22.4°C | Trame : $WAI-224$
Température :  22.3°C | Trame : $WAI-223$
```

---

#### Mesure de la trame avec l'AD2

**Modifier le programme pour envoyer la trame sur l'UART :**

Ajouter après la ligne `print(...)` :

```python
# Envoi de la trame sur l'UART
import serial

port = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)
port.write(f"{trame}\n".encode('utf-8'))
port.close()
```

**Mesurer avec l'AD2 :**

1. Connecter l'AD2 sur GPIO 14 (TX)
2. Ouvrir WaveForms > Logic Analyzer
3. Configurer UART 9600 bauds
4. Lancer l'acquisition
5. Exécuter le programme Python
6. Observer la trame décodée

**À documenter :**
- Capture d'écran de la trame dans WaveForms
- Détail des octets transmis
- Durée totale de la trame

---

### Tâche 4 : Validation de la transmission complète (Schéma 1)

#### Objectif

Valider le système complet avec transmission sans fil via XBee.

---

#### Partie A : Configuration des modules XBee

**Matériel nécessaire :**
- 2 modules XBee (série 1 ou 2)
- Adaptateur USB-XBee (pour la configuration initiale)
- Logiciel XCTU (Windows) ou minicom (Linux)

**Configuration XBee #1 (Coordinateur) :**

1. Connecter via USB
2. Ouvrir XCTU
3. Paramètres :
   - **PAN ID** : `1234` (même pour les deux)
   - **DH** : `0`
   - **DL** : `2` (adresse du XBee #2)
   - **MY** : `1` (sa propre adresse)
   - **Baudrate** : `9600`
4. Écrire la configuration

**Configuration XBee #2 (Router) :**

1. Paramètres :
   - **PAN ID** : `1234`
   - **DH** : `0`
   - **DL** : `1` (adresse du XBee #1)
   - **MY** : `2`
   - **Baudrate** : `9600`
2. Écrire la configuration

---

#### Partie B : Montage du système complet

**Sur Raspberry Pi #1 :**

1. Monter le Shield XBee
2. Insérer le XBee #1
3. Connecter le capteur TCN75A (I2C)
4. Vérifier les connexions

**Sur Raspberry Pi #2 :**

1. Monter le Shield XBee
2. Insérer le XBee #2

---

#### Partie C : Programme émetteur (Raspberry Pi #1)

Créer `emetteur_complet.py` :

```python
#!/usr/bin/env python3
import smbus2
import serial
import time

# Configuration
TCN75A_ADDR = 0x48
REG_TEMP = 0x00
NOM = "WAI"  # MODIFIER

# I2C et Serial
bus = smbus2.SMBus(1)
uart = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

def lire_temperature():
    data = bus.read_i2c_block_data(TCN75A_ADDR, REG_TEMP, 2)
    temp_raw = (data[0] << 4) | (data[1] >> 4)
    if temp_raw & 0x800:
        temp_raw = temp_raw - 4096
    return round(temp_raw * 0.0625, 1)

def creer_trame(temperature, nom):
    temp_int = int(abs(temperature) * 10)
    d1 = (temp_int // 100) % 10
    d2 = (temp_int // 10) % 10
    d3 = temp_int % 10
    return f"${nom.upper()}-{d1}{d2}{d3}$"

print("=== Émetteur température XBee ===\n")

try:
    while True:
        temp = lire_temperature()
        trame = creer_trame(temp, NOM)
        
        # Envoi via XBee
        uart.write(f"{trame}\n".encode('utf-8'))
        
        print(f"[{time.strftime('%H:%M:%S')}] T={temp:5.1f}°C | Envoyé: {trame}")
        
        time.sleep(5)  # Envoi toutes les 5 secondes

except KeyboardInterrupt:
    print("\nArrêt")
finally:
    bus.close()
    uart.close()
```

---

#### Partie D : Programme récepteur (Raspberry Pi #2)

Créer `recepteur_complet.py` :

```python
#!/usr/bin/env python3
import serial
import time

# Configuration
uart = serial.Serial('/dev/serial0', baudrate=9600, timeout=5)

print("=== Récepteur XBee ===\n")
print("En attente de trames...\n")

try:
    while True:
        if uart.in_waiting > 0:
            trame = uart.readline().decode('utf-8').strip()
            
            if trame:
                timestamp = time.strftime('%H:%M:%S')
                print(f"[{timestamp}] Reçu : {trame}")
                
                # Décoder la trame
                if trame.startswith('$') and trame.endswith('$'):
                    contenu = trame[1:-1]  # Retirer les $
                    if '-' in contenu:
                        nom, temp_str = contenu.split('-')
                        
                        # Extraire la température
                        d1 = int(temp_str[0])
                        d2 = int(temp_str[1])
                        d3 = int(temp_str[2])
                        temp = d1 * 10 + d2 + d3 / 10.0
                        
                        print(f"         → Nom: {nom}, Température: {temp:.1f}°C\n")

except KeyboardInterrupt:
    print("\nArrêt")
finally:
    uart.close()
```

---

#### Partie E : Tests de validation

**Test 1 : Transmission locale (sans XBee)**

Connecter directement TX #1 vers RX #2 (avec adaptateur de niveau si nécessaire).

**Test 2 : Transmission avec XBee (portée courte)**

1. Placer les deux Raspberry Pi à 1 mètre
2. Lancer le récepteur sur #2
3. Lancer l'émetteur sur #1
4. Vérifier la réception correcte

**Test 3 : Test de portée**

Éloigner progressivement les deux systèmes :
- 1 m, 5 m, 10 m, 20 m, etc.
- Noter la portée maximale avant perte de signal

**Test 4 : Test d'obstacles**

Tester la transmission à travers :
- Mur en plâtre
- Porte fermée
- Étage différent

**À documenter :**
- Captures d'écran des terminaux (émetteur et récepteur)
- Tableau de portée vs obstacles
- Photos du montage complet
- Analyse des performances

---

### Tâche 5 : Automatisation avec Cron (envoi toutes les 2 minutes)

#### Objectif

Automatiser l'envoi de la température toutes les 2 minutes avec Crontab.

---

#### Partie A : Créer le script d'envoi unique

Modifier `emetteur_complet.py` pour **un seul envoi** :

Créer `envoi_temperature.py` :

```python
#!/usr/bin/env python3
import smbus2
import serial

# Configuration
TCN75A_ADDR = 0x48
REG_TEMP = 0x00
NOM = "WAI"  # MODIFIER

# I2C et Serial
bus = smbus2.SMBus(1)
uart = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

def lire_temperature():
    data = bus.read_i2c_block_data(TCN75A_ADDR, REG_TEMP, 2)
    temp_raw = (data[0] << 4) | (data[1] >> 4)
    if temp_raw & 0x800:
        temp_raw = temp_raw - 4096
    return round(temp_raw * 0.0625, 1)

def creer_trame(temperature, nom):
    temp_int = int(abs(temperature) * 10)
    d1 = (temp_int // 100) % 10
    d2 = (temp_int // 10) % 10
    d3 = temp_int % 10
    return f"${nom.upper()}-{d1}{d2}{d3}$"

# Lecture et envoi
temp = lire_temperature()
trame = creer_trame(temp, NOM)
uart.write(f"{trame}\n".encode('utf-8'))

print(f"Envoyé: {trame} ({temp:.1f}°C)")

# Fermeture
bus.close()
uart.close()
```

**Rendre exécutable :**

```bash
chmod +x envoi_temperature.py
```

---

#### Partie B : Configurer Crontab

**Éditer la crontab :**

```bash
crontab -e
```

**Ajouter la ligne (envoi toutes les 2 minutes) :**

```bash
*/2 * * * * /usr/bin/python3 /home/pi/envoi_temperature.py >> /home/pi/temperature.log 2>&1
```

**Explication :**
- `*/2` : Toutes les 2 minutes
- `* * * *` : Toutes les heures, jours, mois, jours de la semaine
- `>> /home/pi/temperature.log` : Log des envois
- `2>&1` : Redirection des erreurs

**Vérifier la crontab :**

```bash
crontab -l
```

---

#### Partie C : Vérification du fonctionnement

**Consulter les logs :**

```bash
tail -f /home/pi/temperature.log
```

Vous devriez voir un nouvel envoi toutes les 2 minutes.

**Exemple de sortie :**

```
Envoyé: $WAI-234$ (23.4°C)
Envoyé: $WAI-235$ (23.5°C)
Envoyé: $WAI-234$ (23.4°C)
```

**Vérifier les logs système de cron :**

```bash
grep CRON /var/log/syslog | tail -20
```

**À documenter :**
- Ligne crontab configurée
- Extraits des logs sur 10 minutes
- Preuve de réception sur Raspberry Pi #2

---

## 📊 Compte-rendu d'activité

### Structure du compte-rendu (format PDF)

**1. Page de garde**
- Titre, nom, classe, date

**2. Sommaire**

**3. Introduction**
- Contexte et objectifs
- Présentation du protocole XBee
- Architecture du système

**4. Partie technique**

**4.1 Configuration UART**
- Démarche effectuée
- Captures d'écran des fichiers Linux
- Tests unitaires :
  - Envoi trame TEST
  - Mesure AD2 (capture + analyse)
  - Réception Rasp #2
  - Test bidirectionnel

**4.2 Capteur TCN75A**
- Schéma de câblage
- Programme de test (code commenté)
- Relevés comparatifs avec thermomètre
- Photos du montage
- Analyse des écarts

**4.3 Création de la trame**
- Format de la trame
- Algorithme de création
- Code source commenté
- Exemples de trames générées
- Mesure AD2 de la trame

**4.4 Transmission XBee**
- Configuration des modules
- Schéma complet du système (préciser L1, L2, L3, L4)
- Code émetteur et récepteur
- Tests de validation :
  - Transmission locale
  - Transmission XBee courte distance
  - Tests de portée
  - Tests d'obstacles
- Captures d'écran des terminaux
- Analyse des performances

**4.5 Automatisation Cron**
- Configuration crontab
- Script d'envoi
- Logs d'exécution
- Validation du fonctionnement

**5. Analyse et discussion**
- Difficultés rencontrées
- Solutions apportées
- Performances du système
- Portée effective
- Fiabilité de la transmission
- Améliorations possibles

**6. Conclusion**
- Objectifs atteints
- Compétences acquises
- Bilan du projet

**7. Annexes**
- Code source complet
- Datasheets des composants
- Captures supplémentaires

---

## ✅ Checklist finale

### Configuration
- [ ] UART activé sur les 2 Raspberry Pi
- [ ] I2C activé sur Raspberry Pi #1
- [ ] Modules XBee configurés (PAN ID, adresses)

### Tests unitaires
- [ ] Envoi trame TEST validé
- [ ] Mesure AD2 de la trame
- [ ] Réception sur Rasp #2 validée
- [ ] Test bidirectionnel effectué

### Capteur TCN75A
- [ ] Câblage correct (schéma + photo)
- [ ] Détection I2C OK (i2cdetect)
- [ ] Programme de test fonctionnel
- [ ] Validation avec thermomètre de référence
- [ ] Écarts < 1°C

### Création de trame
- [ ] Format de trame respecté ($NOM-D1D2D3$)
- [ ] Programme de création de trame fonctionnel
- [ ] Tests avec différentes températures
- [ ] Mesure AD2 de la trame complète

### Transmission XBee
- [ ] Système complet câblé
- [ ] Programme émetteur opérationnel
- [ ] Programme récepteur opérationnel
- [ ] Transmission locale validée
- [ ] Transmission XBee validée
- [ ] Tests de portée effectués
- [ ] Tests d'obstacles documentés

### Automatisation
- [ ] Script d'envoi unique créé
- [ ] Crontab configurée (toutes les 2 minutes)
- [ ] Logs fonctionnels
- [ ] Validation sur 10 minutes minimum

### Documentation
- [ ] Compte-rendu complet en PDF
- [ ] Tous les codes sources commentés
- [ ] Captures d'écran de toutes les étapes
- [ ] Photos du montage
- [ ] Schémas de câblage
- [ ] Analyses et mesures

---

## 🔧 Dépannage

### Problèmes UART

**Erreur "Permission denied" sur /dev/serial0**

Solution :
```bash
sudo usermod -a -G dialout $USER
# Puis redémarrer ou se déconnecter/reconnecter
```

**UART ne fonctionne pas**

Vérifier :
```bash
# Vérifier que la console série est désactivée
cat /boot/cmdline.txt
# Ne doit PAS contenir "console=serial0,115200"

# Vérifier config.txt
cat /boot/config.txt
# Doit contenir : enable_uart=1
```

### Problèmes I2C

**Capteur non détecté (i2cdetect ne voit rien)**

- Vérifier le câblage (SDA, SCL)
- Vérifier l'alimentation 3.3V
- Vérifier les résistances pull-up
- Essayer une autre adresse (0x48, 0x49, 0x4A, 0x4B)

### Problèmes XBee

**Pas de communication entre les modules**

- Vérifier que les deux XBee ont le même PAN ID
- Vérifier les adresses (DL doit pointer vers MY de l'autre)
- Vérifier le baudrate (9600)
- Tester les modules individuellement avec XCTU

**Portée limitée**

- Vérifier les antennes
- Éloigner des sources d'interférences (WiFi, Bluetooth)
- Vérifier l'alimentation des modules

### Problèmes Crontab

**Script ne s'exécute pas**

Vérifier :
```bash
# Logs système
grep CRON /var/log/syslog | tail -20

# Chemin absolu dans crontab
which python3
# Utiliser /usr/bin/python3 dans crontab

# Tester le script manuellement
/usr/bin/python3 /home/pi/envoi_temperature.py
```

---

## 📚 Ressources

### Documentation protocoles

- **UART** : [Serial HOWTO](https://tldp.org/HOWTO/Serial-HOWTO.html)
- **I2C** : [I2C Bus Specification](https://www.nxp.com/docs/en/user-guide/UM10204.pdf)
- **XBee** : [Documentation Digi](https://www.digi.com/resources/documentation/digidocs/90001456-13/)

### Datasheets

- **TCN75A** : [Microchip TCN75A](https://www.microchip.com/wwwproducts/en/TCN75A)
- **XBee S1** : [XBee/XBee-PRO RF Modules](https://www.digi.com/resources/documentation/digidocs/pdfs/90000982.pdf)

### Outils

- **XCTU** : [Configuration XBee](https://www.digi.com/products/embedded-systems/digi-xbee/digi-xbee-tools/xctu)
- **WaveForms** : [Analog Discovery 2](https://digilent.com/reference/software/waveforms/waveforms-3/start)

### Python

- **pySerial** : [Documentation](https://pyserial.readthedocs.io/)
- **smbus2** : [Documentation I2C Python](https://pypi.org/project/smbus2/)

---

## 💡 Améliorations possibles

### Court terme

- Ajouter un checksum à la trame pour détecter les erreurs
- Implémenter un accusé de réception
- Ajouter l'horodatage dans la trame
- Logger les données dans une base de données

### Moyen terme

- Créer une interface web pour visualiser les températures
- Ajouter plusieurs capteurs (multi-points)
- Implémenter un système d'alerte (température hors limites)
- Créer des graphiques d'évolution

### Long terme

- Mode veille pour économie d'énergie
- Alimenter sur batterie avec panneau solaire
- Réseau maillé avec plusieurs nœuds XBee
- Intégration IoT (MQTT, cloud)

---

## 📐 Annexe : Calculs et formules

### Temporisation UART (9600 bauds)

**Durée d'un bit :**
```
T_bit = 1 / baudrate = 1 / 9600 ≈ 104 µs
```

**Trame complète (10 bits : 1 start + 8 data + 1 stop) :**
```
T_octet = 10 × T_bit ≈ 1.04 ms
```

**Trame "$WAI-234$" (9 octets + LF) :**
```
T_trame = 10 × 1.04 ms ≈ 10.4 ms
```

### Résolution TCN75A

**Résolution :** 12 bits  
**Pas de mesure :** 0.0625°C (1/16°C)  
**Plage :** -40°C à +125°C

### Portée théorique XBee

**Série 1 (intérieur) :** ~30 mètres  
**Série 1 (extérieur, champ libre) :** ~100 mètres  
**Série 2 Pro (extérieur) :** jusqu'à 1.6 km

---

**Bon courage pour ce projet de communication sans fil ! 📡🌡️**