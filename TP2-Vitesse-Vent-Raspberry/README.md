# TP2 - Raspberry Pi : Mesure de vitesse du vent - Programme avec interruption

## 📋 Informations générales

**Type d'activité :** Mini-projet  
**Durée :** 10 heures  
**Type d'évaluation :** Compte-rendu d'activité & questionnement oral

---

## 🎯 Objectifs

À l'issue de ce TP, vous serez capable de :

- Interfacer un capteur anémomètre sur Raspberry Pi
- Comprendre et utiliser les résistances pull-up
- Mettre en œuvre les interruptions GPIO en Python
- Mesurer et calculer une fréquence de signal
- Convertir des unités physiques (km/h, m/s, Hz, tr/s)
- Implémenter un filtrage par moyenne glissante
- Calibrer un système de mesure avec un générateur de signaux

---

## 🛠️ Matériel nécessaire

- **Raspberry Pi** (modèle 3 ou supérieur recommandé)
- **Anémomètre** (capteur à interrupteur ILS)
- **Résistance de pull-up 10kΩ** (si non intégrée)
- **Câbles de connexion** (jumpers)
- **Oscilloscope Analog Discovery 2 (AD2)**
- **Générateur de signaux** (AD2 : pour la calibration)

---

## 📐 Principe de fonctionnement

### L'anémomètre

Un anémomètre est un capteur mesurant la vitesse du vent à l'aide de coupelles qui tournent. À chaque rotation, un interrupteur à lame souple (ILS - Interrupteur à Lame Souple ou Reed Switch) s'ouvre et se ferme, générant des impulsions électriques.

### Schéma de câblage

```
      3,3V
       |
      [10kΩ] ← Résistance de pull-up
       |
       ├─────────→ GPIO (entrée Raspberry Pi)
       |
    [Switch]  ← Anémomètre (ILS)
       |
      GND
```

**Fonctionnement :**
- **Switch ouvert** : Le signal GPIO est au niveau HAUT (3,3V) grâce à la résistance de pull-up
- **Switch fermé** : Le signal GPIO passe au niveau BAS (0V)

---

## 📝 Tâches à effectuer

### Partie 1 : Câblage et validation du signal

#### Tâche 1 : Réalisation du câblage

**Connexion de l'anémomètre :**

| Anémomètre | Raspberry Pi | Description |
|------------|--------------|-------------|
| Fil 1 (signal) | GPIO 17 (Pin 11) | Signal de sortie |
| Fil 2 (GND) | GND (Pin 6) | Masse commune |
| 3,3V | Pin 1 (3.3V) | Via résistance 10kΩ |

**Schéma détaillé :**
- Connecter une extrémité de la résistance 10kΩ au 3,3V
- Connecter l'autre extrémité à GPIO 17
- Connecter un fil de l'anémomètre à GPIO 17
- Connecter l'autre fil de l'anémomètre à GND

**⚠️ Important :** Noter le GPIO choisi pour la suite du TP.

**À documenter dans le compte-rendu :**
- Schéma de câblage réalisé
- Photo du montage
- Numéro de GPIO utilisé

---

#### Tâche 2 : Validation du signal avec l'oscilloscope AD2

**Objectif :** Vérifier que le signal de l'anémomètre est correctement reçu par le Raspberry Pi.

**Procédure :**

1. **Connecter l'oscilloscope AD2 :**
   - Canal 1 : GPIO 17 (signal)
   - GND : GND commun

2. **Lancer WaveForms (logiciel AD2)**

3. **Faire tourner manuellement l'anémomètre**

4. **Observer le signal :**
   - Forme du signal (rectangulaire attendu)
   - Amplitude (0V à 3,3V attendu)
   - Fréquence (variable selon la vitesse)

**À documenter dans le compte-rendu :**
- Capture d'écran de l'oscilloscope
- Caractéristiques du signal :
  - Niveau HAUT : ___ V
  - Niveau BAS : ___ V
  - Fréquence mesurée : ___ Hz
  - Période : ___ ms
  - Rapport cyclique : ___ %

---

### Partie 2 : Formules et calculs théoriques

#### Tâche 3 : Relation vitesse du vent ↔ vitesse de rotation

**Formule générique pour un anémomètre :**

La relation entre la vitesse du vent **V** (en m/s) et la vitesse de rotation **Vr** (en tr/s) dépend du rayon des coupelles et de l'efficacité aérodynamique.

**Formule typique :**
```
V (m/s) = k × Vr (tr/s)
```

Où **k** est le coefficient aérodynamique de l'anémomètre (généralement entre 2 et 4).

**Pour ce TP, on utilisera :** `k = 2.4` (valeur typique)

```
V (m/s) = 2.4 × Vr (tr/s)
```

**À documenter :**
- Origine de la constante k (documentation constructeur)
- Unités et cohérence dimensionnelle

---

#### Tâche 4 : Relation vitesse de rotation ↔ fréquence du capteur

L'anémomètre génère **1 impulsion par tour**.

Donc :
```
Fc (Hz) = Vr (tr/s)
```

Où :
- **Fc** : Fréquence du signal en Hz
- **Vr** : Vitesse de rotation en tours par seconde (tr/s)

**Formule finale combinée :**
```
V (m/s) = 2.4 × Fc (Hz)
```

**Conversion en km/h :**
```
V (km/h) = V (m/s) × 3.6
V (km/h) = 2.4 × Fc × 3.6
V (km/h) = 8.64 × Fc (Hz)
```

---

#### Tâche 5 : Tableur de calcul

**Créer un fichier tableur (LibreOffice Calc ou Excel) avec les colonnes suivantes :**

| Vitesse (km/h) | Vitesse (m/s) | Vitesse rotation (tr/s) | Fréquence (Hz) | Période (ms) |
|----------------|---------------|------------------------|---------------|--------------|
| 0 | 0.00 | 0.00 | 0.00 | ∞ |
| 10 | 2.78 | 1.16 | 1.16 | 864 |
| 20 | 5.56 | 2.31 | 2.31 | 432 |
| 30 | 8.33 | 3.47 | 3.47 | 288 |
| 40 | 11.11 | 4.63 | 4.63 | 216 |
| 50 | 13.89 | 5.79 | 5.79 | 173 |
| 60 | 16.67 | 6.94 | 6.94 | 144 |
| 70 | 19.44 | 8.10 | 8.10 | 123 |
| 80 | 22.22 | 9.26 | 9.26 | 108 |
| 90 | 25.00 | 10.42 | 10.42 | 96 |
| 100 | 27.78 | 11.57 | 11.57 | 86 |

**Formules à utiliser :**
- `V(m/s) = V(km/h) / 3.6`
- `Vr(tr/s) = V(m/s) / 2.4`
- `Fc(Hz) = Vr(tr/s)`
- `Période(ms) = 1000 / Fc(Hz)`

**À inclure dans le compte-rendu :**
- Fichier tableur complet
- Graphique Vitesse(km/h) vs Fréquence(Hz)

---

### Partie 3 : Programme Python avec interruptions

#### Tâche 6 : Mesure instantanée de la fréquence et vitesse

**Créer le fichier `mesure_vent_instant.py` :**

```python
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Configuration
GPIO_PIN = 17  # GPIO utilisé pour l'anémomètre
K_AERO = 2.4   # Coefficient aérodynamique

# Variables globales
pulse_count = 0
last_time = 0
frequency = 0

def setup_gpio():
    """Initialise le GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def pulse_callback(channel):
    """Fonction appelée à chaque front descendant (interruption)"""
    global pulse_count, last_time, frequency
    
    current_time = time.time()
    
    if last_time > 0:
        # Calculer le temps entre deux impulsions
        time_diff = current_time - last_time
        
        if time_diff > 0:
            # Calculer la fréquence (Hz)
            frequency = 1.0 / time_diff
    
    last_time = current_time
    pulse_count += 1

def calculate_wind_speed(freq):
    """Calcule la vitesse du vent à partir de la fréquence"""
    v_ms = K_AERO * freq          # Vitesse en m/s
    v_kmh = v_ms * 3.6             # Vitesse en km/h
    return v_ms, v_kmh

def main():
    """Fonction principale"""
    global frequency
    
    print("=== Mesure de vitesse du vent (instantanée) ===")
    print(f"GPIO utilisé: {GPIO_PIN}")
    print(f"Coefficient k: {K_AERO}")
    print("\nAppuyez sur Ctrl+C pour arrêter\n")
    
    setup_gpio()
    
    # Attacher l'interruption sur front descendant
    GPIO.add_event_detect(GPIO_PIN, GPIO.FALLING, callback=pulse_callback, bouncetime=10)
    
    try:
        while True:
            time.sleep(1)  # Affichage toutes les secondes
            
            if frequency > 0:
                v_ms, v_kmh = calculate_wind_speed(frequency)
                
                print(f"Fréquence: {frequency:6.2f} Hz | "
                      f"Vitesse: {v_ms:6.2f} m/s | "
                      f"{v_kmh:6.2f} km/h")
            else:
                print("En attente de signal...")
                
    except KeyboardInterrupt:
        print("\n\nArrêt du programme")
    finally:
        GPIO.cleanup()
        print(f"Total d'impulsions: {pulse_count}")

if __name__ == "__main__":
    main()
```

**Rendre le script exécutable :**
```bash
chmod +x mesure_vent_instant.py
```

**Exécution :**
```bash
python3 mesure_vent_instant.py
```

**À documenter :**
- Captures d'écran du programme en fonctionnement
- Observations sur la stabilité des mesures

---

#### Tâche 7 : Calibration avec le générateur AD2

**Objectif :** Vérifier que le programme mesure correctement la fréquence.

**Procédure :**

1. **Déconnecter l'anémomètre** du GPIO

2. **Connecter le générateur AD2 :**
   - Sortie W1 du générateur → GPIO 17
   - GND → GND commun

3. **Configurer WaveForms :**
   - Signal : Carré
   - Amplitude : 3,3V
   - Offset : 1,65V
   - Fréquence : selon le tableau (tâche 5)

4. **Pour chaque fréquence du tableau :**
   - Régler le générateur
   - Lancer le programme Python
   - Noter la fréquence mesurée
   - Calculer l'erreur

**Tableau de calibration à compléter :**

| V théorique (km/h) | Fc théorique (Hz) | Fc mesurée (Hz) | Erreur (%) |
|-------------------|------------------|----------------|-----------|
| 10 | 1.16 | | |
| 20 | 2.31 | | |
| 30 | 3.47 | | |
| 40 | 4.63 | | |
| 50 | 5.79 | | |
| 60 | 6.94 | | |
| 70 | 8.10 | | |
| 80 | 9.26 | | |
| 90 | 10.42 | | |
| 100 | 11.57 | | |

**Formule de l'erreur :**
```
Erreur (%) = |Fc_mesurée - Fc_théorique| / Fc_théorique × 100
```

---

### Partie 4 : Programme avec moyenne glissante

#### Tâche 8 : Implémentation de la moyenne sur 10 valeurs

**Créer le fichier `mesure_vent_moyenne.py` :**

```python
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from collections import deque

# Configuration
GPIO_PIN = 17
K_AERO = 2.4
WINDOW_SIZE = 10  # Nombre de valeurs pour la moyenne

# Variables globales
last_time = 0
frequency_buffer = deque(maxlen=WINDOW_SIZE)

def setup_gpio():
    """Initialise le GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def pulse_callback(channel):
    """Fonction appelée à chaque impulsion"""
    global last_time, frequency_buffer
    
    current_time = time.time()
    
    if last_time > 0:
        time_diff = current_time - last_time
        
        if time_diff > 0:
            freq = 1.0 / time_diff
            frequency_buffer.append(freq)
    
    last_time = current_time

def calculate_average_frequency():
    """Calcule la fréquence moyenne"""
    if len(frequency_buffer) == 0:
        return 0
    return sum(frequency_buffer) / len(frequency_buffer)

def calculate_wind_speed(freq):
    """Calcule la vitesse du vent"""
    v_ms = K_AERO * freq
    v_kmh = v_ms * 3.6
    return v_ms, v_kmh

def main():
    """Fonction principale"""
    print("=== Mesure de vitesse du vent (moyenne glissante) ===")
    print(f"GPIO utilisé: {GPIO_PIN}")
    print(f"Taille de la fenêtre: {WINDOW_SIZE} valeurs")
    print(f"Coefficient k: {K_AERO}")
    print("\nAppuyez sur Ctrl+C pour arrêter\n")
    
    setup_gpio()
    GPIO.add_event_detect(GPIO_PIN, GPIO.FALLING, callback=pulse_callback, bouncetime=10)
    
    try:
        while True:
            time.sleep(1)
            
            freq_avg = calculate_average_frequency()
            
            if freq_avg > 0:
                v_ms, v_kmh = calculate_wind_speed(freq_avg)
                
                print(f"Échantillons: {len(frequency_buffer):2d}/{WINDOW_SIZE} | "
                      f"Fréquence moy: {freq_avg:6.2f} Hz | "
                      f"Vitesse: {v_ms:6.2f} m/s | "
                      f"{v_kmh:6.2f} km/h")
            else:
                print("En attente de signal...")
                
    except KeyboardInterrupt:
        print("\n\nArrêt du programme")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
```

**Exécution :**
```bash
python3 mesure_vent_moyenne.py
```

**Avantages de la moyenne glissante :**
- ✅ Réduit le bruit et les fluctuations
- ✅ Donne une mesure plus stable
- ✅ Filtre les valeurs aberrantes

---

#### Tâche 9 : Calibration du programme avec moyenne

**Répéter la procédure de calibration (Tâche 7) avec le nouveau programme.**

**Tableau de comparaison :**

| V (km/h) | Fc théo (Hz) | Fc instant (Hz) | Fc moyenne (Hz) | Stabilité |
|---------|-------------|----------------|----------------|----------|
| 10 | 1.16 | | | |
| 20 | 2.31 | | | |
| ... | ... | | | |

**Questions à analyser :**
- Quel programme donne les résultats les plus stables ?
- L'erreur de mesure est-elle réduite avec la moyenne ?
- Quel est le temps de réponse du système avec la moyenne ?

---

## 📊 Compte-rendu attendu

Votre compte-rendu doit contenir :

### 1. Page de garde
- Titre du TP
- Nom, prénom, classe
- Date

### 2. Introduction
- Objectifs du TP
- Principe de fonctionnement de l'anémomètre

### 3. Partie expérimentale

**3.1 Câblage**
- Schéma de câblage réalisé
- Photo du montage
- Explication du rôle de la résistance pull-up

**3.2 Validation du signal**
- Captures oscilloscope
- Caractérisation complète du signal

**3.3 Calculs théoriques**
- Formules utilisées
- Tableur avec les 11 valeurs
- Graphique Vitesse vs Fréquence

**3.4 Programmation**
- Code Python commenté (les deux versions)
- Explication du fonctionnement des interruptions
- Principe de la moyenne glissante

**3.5 Calibration**
- Tableaux de mesures complets
- Calcul des erreurs
- Analyse de la précision

### 4. Analyse et discussion
- Comparaison des deux programmes
- Avantages/inconvénients de chaque méthode
- Sources d'erreur
- Améliorations possibles

### 5. Conclusion
- Objectifs atteints
- Compétences acquises
- Difficultés rencontrées

### 6. Annexes
- Code source complet
- Datasheets
- Captures d'écran supplémentaires

---

## 🔧 Dépannage

### Aucun signal détecté

**Vérifier :**
- Le câblage (connexions correctes ?)
- La résistance pull-up (bien connectée ?)
- L'anémomètre (fonctionne-t-il mécaniquement ?)
- Le numéro de GPIO dans le code

**Test simple :**
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    print(GPIO.input(17))
    time.sleep(0.1)
```

### Valeurs instables ou aberrantes

**Solutions :**
- Augmenter le `bouncetime` dans l'interruption
- Utiliser la moyenne glissante (Tâche 8)
- Filtrer les valeurs trop éloignées (détection d'outliers)

### Interruptions ne fonctionnent pas

**Vérifier :**
```bash
# Vérifier que RPi.GPIO est installé
pip3 list | grep RPi.GPIO

# Réinstaller si nécessaire
pip3 install RPi.GPIO
```

---

## 📚 Ressources

### Documentation
- Voir le dossier `Documents/` du TP
- [Documentation RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/)
- [Guide des interruptions GPIO](https://raspberrypi.stackexchange.com/questions/8544/gpio-interrupt-debounce)

### Datasheets
- Anémomètre (voir dossier Documents)
- Raspberry Pi GPIO Pinout : [pinout.xyz](https://pinout.xyz)

---

## ✅ Checklist finale

Avant de rendre le compte-rendu :

- [ ] Câblage réalisé et documenté
- [ ] Signal validé à l'oscilloscope
- [ ] Formules établies et vérifiées
- [ ] Tableur complet (11 valeurs)
- [ ] Programme instantané fonctionnel
- [ ] Calibration instantanée effectuée
- [ ] Programme avec moyenne fonctionnel
- [ ] Calibration moyenne effectuée
- [ ] Compte-rendu rédigé et relu
- [ ] Codes sources commentés et annexés
- [ ] Graphiques et tableaux inclus

---

## 💡 Pour aller plus loin (optionnel)

- Ajouter un affichage LCD pour visualiser la vitesse en temps réel
- Enregistrer les données dans un fichier CSV
- Créer une interface web pour visualiser les mesures
- Implémenter une détection de rafales (pic de vitesse)
- Ajouter un historique graphique des mesures

---

**Bon courage pour ce TP ! 🌬️**
