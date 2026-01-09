# TP10 - Module GSM SIM800C et contrôle d'arrosage par SMS

## 📋 Informations générales

**Durée estimée :** 10 heures  
**Niveau :** Intermédiaire/Avancé  
**Prérequis :**
- Connaissances de base en Python
- Notions sur les GPIO du Raspberry Pi
- Bases de la communication série
- Connaissances minimales en développement Android (AppInventor)

**Matériel nécessaire :**
- Raspberry Pi 3 avec Raspberry Pi OS Legacy (32 bits) Lite
- Carte Waveshare SIM800C
- Carte SIM avec forfait SMS
- 2 relais (5V)
- 2 électrovannes d'arrosage
- Smartphone Android
- Câbles de connexion
- Alimentation adaptée

---

## 🎯 Objectifs du TP

À l'issue de ce TP, vous serez capable de :
- Installer et configurer un module GSM SIM800C sur Raspberry Pi
- Communiquer avec le module via des commandes AT
- Envoyer et recevoir des SMS en Python
- Contrôler des GPIO pour piloter des relais
- Créer un système de commande à distance par SMS
- Développer une application Android avec App Inventor
- Mettre en place un service au démarrage du Raspberry Pi

---

## 📚 Partie 1 : Installation et test du matériel

### 1.1 Préparation du Raspberry Pi

#### Installation de Raspberry Pi OS Legacy Lite

1. Téléchargez **Raspberry Pi OS Legacy (32-bit) Lite** depuis le site officiel
2. Utilisez **Raspberry Pi Imager** pour flasher la carte SD
3. Avant de démarrer :
   - Activez SSH (créez un fichier vide nommé `ssh` à la racine de la partition boot)
   - Configurez le Wi-Fi si nécessaire (fichier `wpa_supplicant.conf`)

4. Démarrez le Raspberry Pi et connectez-vous via SSH :
```bash
ssh pi@adresse_ip_raspberry
```

5. Mettez à jour le système :
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

#### Installation des outils nécessaires

```bash
# Installation de Python et bibliothèques
sudo apt-get install python3-serial python3-rpi.gpio -y

# Installation de minicom pour les tests
sudo apt-get install minicom -y

# Installation de git (utile pour partager votre code)
sudo apt-get install git -y
```

### 1.2 Connexion de la carte Waveshare SIM800C

#### Schéma de connexion

La carte SIM800C se connecte sur les GPIO du Raspberry Pi :

| SIM800C | Raspberry Pi 3 |
|---------|----------------|
| VCC | 5V (Pin 2 ou 4) |
| GND | GND (Pin 6) |
| TXD | RXD (GPIO 15, Pin 10) |
| RXD | TXD (GPIO 14, Pin 8) |

**⚠️ Attention :**
- Assurez-vous que la carte SIM est bien insérée (contacts vers le bas)
- L'alimentation doit être suffisante (2A minimum)
- Le module nécessite quelques secondes pour démarrer (LED rouge clignotante)

#### Configuration du port série

Par défaut, le port série du Raspberry Pi est utilisé pour la console. Il faut le libérer :

```bash
sudo raspi-config
```

- Allez dans **3 Interface Options**
- Sélectionnez **I6 Serial Port**
- "Would you like a login shell to be accessible over serial?" → **No**
- "Would you like the serial port hardware to be enabled?" → **Yes**
- Redémarrez : `sudo reboot`

### 1.3 Vérification de la connexion

Après redémarrage, vérifiez que le port série est disponible :

```bash
ls -l /dev/ttyS0
```

Vous devriez voir quelque chose comme :
```
crw-rw---- 1 root dialout 4, 64 Jan 10 10:30 /dev/ttyS0
```

### 1.4 Test avec AT_Console.py

Le logiciel `AT_Console.py` permet de communiquer facilement avec le module GSM.

#### Installation et configuration

Créez le fichier `AT_Console.py` :

```python
#!/usr/bin/env python3
import serial
import time
import sys

# Configuration du port série
PORT = "/dev/ttyS0"
BAUDRATE = 115200

class ATConsole:
    def __init__(self, port, baudrate):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)
            print(f"✓ Connecté à {port} à {baudrate} baud")
            print("=" * 50)
            print("Console AT pour SIM800C")
            print("Tapez vos commandes AT (Ctrl+C pour quitter)")
            print("=" * 50)
        except Exception as e:
            print(f"✗ Erreur de connexion : {e}")
            sys.exit(1)
    
    def send_command(self, command):
        """Envoie une commande AT et affiche la réponse"""
        try:
            # Envoi de la commande
            self.ser.write((command + '\r').encode())
            time.sleep(0.5)
            
            # Lecture de la réponse
            response = ""
            while self.ser.in_waiting:
                response += self.ser.read(self.ser.in_waiting).decode(errors='ignore')
                time.sleep(0.1)
            
            return response
        except Exception as e:
            return f"Erreur : {e}"
    
    def run(self):
        """Boucle principale de la console"""
        while True:
            try:
                # Lecture de la commande utilisateur
                cmd = input("AT> ")
                
                if not cmd:
                    continue
                
                # Envoi et affichage de la réponse
                response = self.send_command(cmd)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n✓ Fermeture de la console")
                self.ser.close()
                break
            except Exception as e:
                print(f"Erreur : {e}")

if __name__ == "__main__":
    console = ATConsole(PORT, BAUDRATE)
    console.run()
```

Rendez le script exécutable :
```bash
chmod +x AT_Console.py
```

Lancez la console AT :
```bash
python3 AT_Console.py
```

### 1.5 Test des commandes AT de base

Une fois dans la console AT, testez les commandes suivantes :

#### 🔹 **AT** - Test de communication
```
AT> AT
```
**Réponse attendue :** `OK`

**Explication :** Cette commande vérifie que le module répond. C'est le test le plus basique.

---

#### 🔹 **AT+CPIN?** - Vérification de la carte SIM
```
AT> AT+CPIN?
```
**Réponse attendue :** `+CPIN: READY`

**Explication :** 
- `READY` = La carte SIM est détectée et déverrouillée
- `SIM PIN` = Un code PIN est requis
- `SIM PUK` = La carte est bloquée

---

#### 🔹 **AT+CSQ** - Qualité du signal
```
AT> AT+CSQ
```
**Réponse attendue :** `+CSQ: 28,0`

**Explication :**
- Le premier chiffre (0-31) indique la force du signal :
  - 0-9 : Marginal
  - 10-14 : OK
  - 15-19 : Bon
  - 20-31 : Excellent
  - 99 : Pas de signal
- Le second chiffre (0-7) est le taux d'erreur de bit (généralement 0 ou 99)

---

#### 🔹 **AT+CREG?** - Enregistrement sur le réseau
```
AT> AT+CREG?
```
**Réponse attendue :** `+CREG: 0,1` ou `+CREG: 0,5`

**Explication :**
- Format : `+CREG: n,stat`
- `stat` :
  - 0 : Non enregistré, pas de recherche
  - 1 : Enregistré sur le réseau local
  - 2 : Non enregistré, recherche en cours
  - 3 : Enregistrement refusé
  - 5 : Enregistré en itinérance (roaming)

---

#### 🔹 **AT+COPS?** - Opérateur réseau
```
AT> AT+COPS?
```
**Réponse attendue :** `+COPS: 0,0,"Orange F",7`

**Explication :**
- Affiche l'opérateur actuel (Orange, SFR, Bouygues, Free, etc.)
- Le dernier chiffre indique la technologie (0=GSM, 7=LTE)

---

#### 🔹 **AT+CBC** - État de la batterie
```
AT> AT+CBC
```
**Réponse attendue :** `+CBC: 0,100,4150`

**Explication :**
- Format : `+CBC: bcs,bcl,voltage`
- `bcs` : État de charge (0=pas en charge, 1=en charge)
- `bcl` : Niveau de batterie (0-100%)
- `voltage` : Tension en mV

---

#### 🔹 **AT+CCID** - Numéro de la carte SIM (ICCID)
```
AT> AT+CCID
```
**Réponse attendue :** `+CCID: 89330123456789012345`

**Explication :** Affiche le numéro unique de votre carte SIM (utile pour identification)

---

#### 🔹 **AT+CNUM** - Numéro de téléphone de la SIM
```
AT> AT+CNUM
```
**Réponse attendue :** `+CNUM: "","0612345678",129`

**Explication :** Affiche le numéro de téléphone associé à la SIM (peut être vide si non configuré par l'opérateur)

---

### 1.6 Test d'envoi de SMS en mode AT

#### Configuration en mode texte

```
AT> AT+CMGF=1
```
**Réponse :** `OK`

**Explication :** Configure le module pour envoyer des SMS en mode texte (mode 1) plutôt qu'en mode PDU (mode 0)

---

#### Envoi d'un SMS

```
AT> AT+CMGS="+33612345678"
```

Après avoir tapé cette commande, le module affiche `>`. Vous pouvez alors taper votre message :

```
> Bonjour depuis Raspberry Pi
```

**Pour envoyer le message :** Tapez `Ctrl+Z` (caractère SUB, code ASCII 26)

**Réponse attendue :** `+CMGS: 42` suivi de `OK`

**Explication :**
- `AT+CMGS` = "GSM Mobile Originating Short Message"
- Le numéro doit être au format international (+33 pour France)
- Le chiffre dans la réponse (42) est l'ID du message
- Si vous voyez `ERROR`, vérifiez le crédit SMS de votre carte

---

### 1.7 Test de réception de SMS

#### Activation des notifications

```
AT> AT+CNMI=2,2,0,0,0
```
**Réponse :** `OK`

**Explication :** Configure le module pour afficher automatiquement les SMS reçus

---

#### Lecture de tous les SMS

```
AT> AT+CMGL="ALL"
```

**Réponse attendue :**
```
+CMGL: 1,"REC READ","+33612345678","","25/01/09,14:30:45+04"
Bonjour depuis mon téléphone

OK
```

**Explication :**
- Format : `+CMGL: index,status,number,"",date`
- `index` : Numéro du SMS en mémoire (1, 2, 3...)
- `status` : État du SMS
  - `REC UNREAD` : Non lu
  - `REC READ` : Lu
  - `STO UNSENT` : Non envoyé
  - `STO SENT` : Envoyé
- Suivi du contenu du message sur la ligne suivante

**Autres commandes de lecture :**
```
AT+CMGL="REC UNREAD"  → Affiche uniquement les SMS non lus
AT+CMGL="REC READ"    → Affiche uniquement les SMS lus
AT+CMGR=1             → Lit le SMS numéro 1
```

---

### 1.8 Test d'effacement de SMS

#### Effacer un SMS spécifique

```
AT> AT+CMGD=1
```
**Réponse :** `OK`

**Explication :** Supprime le SMS à l'index 1

---

#### Effacer tous les SMS

```
AT> AT+CMGD=1,4
```
**Réponse :** `OK`

**Explication :**
- Format : `AT+CMGD=index,delflag`
- `delflag` :
  - 0 : Supprime uniquement le message à l'index spécifié
  - 1 : Supprime tous les messages lus
  - 2 : Supprime tous les messages lus et envoyés
  - 3 : Supprime tous les messages lus, envoyés et non envoyés
  - 4 : **Supprime TOUS les messages** (recommandé pour vider complètement)

---

### 1.9 Commandes AT avancées (exploration)

Explorez ces commandes supplémentaires pour mieux comprendre le module :

#### 🔹 **AT+CMGF?** - Vérifier le mode SMS actuel
```
AT> AT+CMGF?
```
**Réponse :** `+CMGF: 1` (1=texte, 0=PDU)

---

#### 🔹 **AT+CPMS?** - Capacité de stockage des SMS
```
AT> AT+CPMS?
```
**Réponse :** `+CPMS: "SM",3,50,"SM",3,50,"SM",3,50`

**Explication :** 
- Format : `"mémoire",utilisé,total`
- Ici : 3 SMS stockés sur un total de 50 possibles

---

#### 🔹 **AT+CSCS?** - Jeu de caractères
```
AT> AT+CSCS?
```
**Réponse :** `+CSCS: "GSM"`

**Explication :** Jeu de caractères utilisé (GSM, IRA, UTF-8...)

---

#### 🔹 **AT+CLIP=1** - Affichage du numéro appelant
```
AT> AT+CLIP=1
```
**Explication :** Active l'affichage du numéro en cas d'appel entrant (utile pour des projets avancés)

---

#### 🔹 **ATI** - Informations sur le module
```
AT> ATI
```
**Réponse :**
```
SIM800C R14.18
OK
```
**Explication :** Affiche le modèle et la version du firmware du module

---

#### 🔹 **AT+CGMI** - Fabricant du module
```
AT> AT+CGMI
```
**Réponse :** `SIMCOM_Ltd`

---

#### 🔹 **AT+CGMM** - Modèle du module
```
AT> AT+CGMM
```
**Réponse :** `SIMCOM_SIM800C`

---

### ✅ Validation Partie 1

Avant de passer à la Partie 2, vérifiez que vous avez réussi à :

- [ ] Installer Raspberry Pi OS Legacy Lite
- [ ] Connecter la carte SIM800C au Raspberry Pi
- [ ] Configurer le port série
- [ ] Utiliser AT_Console.py pour communiquer avec le module
- [ ] Obtenir `OK` avec la commande `AT`
- [ ] Vérifier la carte SIM avec `AT+CPIN?`
- [ ] Obtenir un bon signal avec `AT+CSQ`
- [ ] Confirmer l'enregistrement réseau avec `AT+CREG?`
- [ ] Envoyer un SMS avec succès
- [ ] Recevoir et lire un SMS
- [ ] Effacer un SMS puis tous les SMS

**Si toutes ces étapes fonctionnent, vous pouvez passer à la Partie 2 !**

---

## 📚 Partie 2 : Programmation Python pour la gestion des SMS

Dans cette partie, nous allons créer trois programmes Python pour :
1. Envoyer des SMS
2. Recevoir et lire des SMS
3. Effacer des SMS

### 2.1 Programme d'envoi de SMS

Créez le fichier `envoyer_sms.py` :

```python
#!/usr/bin/env python3
"""
Programme d'envoi de SMS via SIM800C
Auteur : Votre nom
Date : 2025-01-10
"""

import serial
import time
import sys

# Configuration
PORT = "/dev/ttyS0"
BAUDRATE = 115200
TIMEOUT = 1

def envoyer_sms(numero, message):
    """
    Envoie un SMS à un numéro donné
    
    Args:
        numero (str): Numéro de téléphone au format international (ex: +33612345678)
        message (str): Contenu du message à envoyer
    
    Returns:
        bool: True si envoi réussi, False sinon
    """
    try:
        # Connexion au module SIM800C
        print(f"📡 Connexion au module sur {PORT}...")
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        time.sleep(2)  # Attendre que le module soit prêt
        
        # Test de communication
        print("🔧 Test de communication...")
        ser.write(b'AT\r')
        time.sleep(0.5)
        reponse = ser.read(ser.in_waiting).decode(errors='ignore')
        if "OK" not in reponse:
            print("✗ Le module ne répond pas correctement")
            return False
        print("✓ Module OK")
        
        # Configuration en mode texte
        print("🔧 Configuration en mode texte...")
        ser.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        reponse = ser.read(ser.in_waiting).decode(errors='ignore')
        if "OK" not in reponse:
            print("✗ Erreur de configuration")
            return False
        print("✓ Mode texte activé")
        
        # Envoi du numéro de destination
        print(f"📤 Envoi vers {numero}...")
        commande = f'AT+CMGS="{numero}"\r'
        ser.write(commande.encode())
        time.sleep(0.5)
        reponse = ser.read(ser.in_waiting).decode(errors='ignore')
        
        if ">" not in reponse:
            print("✗ Le module n'est pas prêt à recevoir le message")
            print(f"Réponse : {reponse}")
            return False
        
        # Envoi du message (terminer par Ctrl+Z = caractère 26)
        print(f"✍️  Message : {message}")
        ser.write(message.encode())
        ser.write(b'\x1A')  # Ctrl+Z
        
        # Attendre la confirmation (peut prendre plusieurs secondes)
        print("⏳ Envoi en cours...")
        time.sleep(5)
        reponse = ser.read(ser.in_waiting).decode(errors='ignore')
        
        # Vérifier la réussite
        if "+CMGS:" in reponse and "OK" in reponse:
            print("✅ SMS envoyé avec succès !")
            print(f"Réponse : {reponse.strip()}")
            ser.close()
            return True
        else:
            print("✗ Erreur lors de l'envoi")
            print(f"Réponse : {reponse}")
            ser.close()
            return False
        
    except serial.SerialException as e:
        print(f"✗ Erreur de connexion série : {e}")
        return False
    except Exception as e:
        print(f"✗ Erreur inattendue : {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("Programme d'envoi de SMS - SIM800C")
    print("=" * 60)
    
    # Configuration du destinataire et du message
    # ⚠️ IMPORTANT : Remplacez par votre numéro de test
    numero_destination = "+33612345678"
    message = "Test d'envoi SMS depuis Raspberry Pi avec SIM800C"
    
    # Affichage des paramètres
    print(f"\n📋 Paramètres :")
    print(f"   - Destinataire : {numero_destination}")
    print(f"   - Message : {message}")
    print(f"   - Port série : {PORT}")
    print(f"   - Vitesse : {BAUDRATE} bauds\n")
    
    # Confirmation
    reponse = input("Voulez-vous envoyer ce SMS ? (o/n) : ")
    if reponse.lower() != 'o':
        print("❌ Envoi annulé")
        return
    
    # Envoi du SMS
    print()
    succes = envoyer_sms(numero_destination, message)
    
    if succes:
        print("\n🎉 Opération terminée avec succès")
    else:
        print("\n❌ L'opération a échoué")
        print("💡 Vérifiez :")
        print("   - La connexion de la carte SIM800C")
        print("   - Le crédit SMS de votre carte SIM")
        print("   - Le signal réseau (AT+CSQ)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programme interrompu par l'utilisateur")
        sys.exit(0)
```

#### Test du programme

```bash
python3 envoyer_sms.py
```

**N'oubliez pas** de modifier le numéro de destination dans le code avant de tester !

---

### 2.2 Programme de réception de SMS

Créez le fichier `recevoir_sms.py` :

```python
#!/usr/bin/env python3
"""
Programme de réception et lecture de SMS via SIM800C
Auteur : Votre nom
Date : 2025-01-10
"""

import serial
import time
import sys
import re

# Configuration
PORT = "/dev/ttyS0"
BAUDRATE = 115200
TIMEOUT = 1

def recevoir_sms():
    """
    Lit tous les SMS stockés sur la carte SIM
    
    Returns:
        list: Liste de dictionnaires contenant les SMS
    """
    try:
        # Connexion au module
        print(f"📡 Connexion au module sur {PORT}...")
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        time.sleep(2)
        
        # Configuration en mode texte
        print("🔧 Configuration en mode texte...")
        ser.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        ser.read(ser.in_waiting)
        
        # Paramétrage pour afficher les détails
        ser.write(b'AT+CSDH=1\r')
        time.sleep(0.5)
        ser.read(ser.in_waiting)
        
        # Lecture de tous les SMS
        print("📬 Lecture des SMS...\n")
        ser.write(b'AT+CMGL="ALL"\r')
        time.sleep(2)
        
        reponse = ser.read(ser.in_waiting).decode(errors='ignore')
        ser.close()
        
        # Analyse de la réponse
        liste_sms = []
        
        # Regex pour extraire les SMS
        # Format : +CMGL: index,"status","numero","","date,heure"
        pattern = r'\+CMGL: (\d+),"([^"]+)","([^"]+)","[^"]*","([^"]+)"\r\n(.+?)(?=\r\n\+CMGL|\r\n\r\nOK)'
        
        matches = re.finditer(pattern, reponse, re.DOTALL)
        
        for match in matches:
            sms = {
                'index': match.group(1),
                'statut': match.group(2),
                'numero': match.group(3),
                'date': match.group(4),
                'message': match.group(5).strip()
            }
            liste_sms.append(sms)
        
        return liste_sms
        
    except Exception as e:
        print(f"✗ Erreur : {e}")
        return []

def afficher_sms(liste_sms):
    """
    Affiche les SMS de manière formatée
    
    Args:
        liste_sms (list): Liste des SMS à afficher
    """
    if not liste_sms:
        print("📭 Aucun SMS en mémoire")
        return
    
    print(f"📨 {len(liste_sms)} SMS trouvé(s) :\n")
    print("=" * 70)
    
    for sms in liste_sms:
        print(f"📩 SMS #{sms['index']} - {sms['statut']}")
        print(f"   De : {sms['numero']}")
        print(f"   Date : {sms['date']}")
        print(f"   Message : {sms['message']}")
        print("-" * 70)

def main():
    """Fonction principale"""
    print("=" * 60)
    print("Programme de réception de SMS - SIM800C")
    print("=" * 60)
    print()
    
    # Réception des SMS
    liste_sms = recevoir_sms()
    
    # Affichage
    afficher_sms(liste_sms)
    
    print("\n✅ Opération terminée")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programme interrompu par l'utilisateur")
        sys.exit(0)
```

#### Test du programme

```bash
python3 recevoir_sms.py
```

**Astuce :** Envoyez-vous d'abord un SMS depuis votre téléphone vers la carte SIM du module, puis exécutez le programme.

---

### 2.3 Programme d'effacement de SMS

Créez le fichier `effacer_sms.py` :

```python
#!/usr/bin/env python3
"""
Programme d'effacement de SMS via SIM800C
Auteur : Votre nom
Date : 2025-01-10
"""

import serial
import time
import sys

# Configuration
PORT = "/dev/ttyS0"
BAUDRATE = 115200
TIMEOUT = 1

def effacer_sms(index=None, tous=False):
    """
    Efface un ou tous les SMS
    
    Args:
        index (int): Numéro du SMS à effacer (None pour tous)
        tous (bool): True pour effacer tous les SMS
    
    Returns:
        bool: True si succès, False sinon
    """
    try:
        # Connexion au module
        print(f"📡 Connexion au module sur {PORT}...")
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        time.sleep(2)
        
        # Commande d'effacement
        if tous:
            print("🗑️  Effacement de TOUS les SMS...")
            commande = b'AT+CMGD=1,4\r'  # 4 = effacer tous les SMS
        elif index:
            print(f"🗑️  Effacement du SMS #{index}...")
            commande = f'AT+CMGD={index}\r'.encode()
        else:
            print("✗ Aucun SMS spécifié")
            return False
        
        ser.write(commande)
        time.sleep(1)
        
        reponse = ser.read(ser.in_waiting).decode(errors='ignore')
        ser.close()
        
        # Vérification
        if "OK" in reponse:
            print("✅ SMS effacé(s) avec succès")
            return True
        else:
            print("✗ Erreur lors de l'effacement")
            print(f"Réponse : {reponse}")
            return False
        
    except Exception as e:
        print(f"✗ Erreur : {e}")
        return False

def menu():
    """Affiche le menu et gère les choix"""
    print("=" * 60)
    print("Programme d'effacement de SMS - SIM800C")
    print("=" * 60)
    print("\n📋 Options :")
    print("   1. Effacer un SMS spécifique")
    print("   2. Effacer TOUS les SMS")
    print("   3. Quitter")
    print()
    
    choix = input("Votre choix (1-3) : ")
    
    if choix == "1":
        index = input("Numéro du SMS à effacer : ")
        try:
            index = int(index)
            effacer_sms(index=index)
        except ValueError:
            print("✗ Numéro invalide")
    
    elif choix == "2":
        confirmation = input("⚠️  Êtes-vous sûr de vouloir effacer TOUS les SMS ? (o/n) : ")
        if confirmation.lower() == 'o':
            effacer_sms(tous=True)
        else:
            print("❌ Opération annulée")
    
    elif choix == "3":
        print("👋 Au revoir !")
        sys.exit(0)
    
    else:
        print("✗ Choix invalide")

def main():
    """Fonction principale"""
    menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programme interrompu par l'utilisateur")
        sys.exit(0)
```

#### Test du programme

```bash
python3 effacer_sms.py
```

---

### ✅ Validation Partie 2

Vérifiez que vous avez réussi à :

- [ ] Créer les trois programmes Python
- [ ] Envoyer un SMS avec `envoyer_sms.py`
- [ ] Recevoir et afficher des SMS avec `recevoir_sms.py`
- [ ] Effacer un SMS spécifique avec `effacer_sms.py`
- [ ] Effacer tous les SMS avec `effacer_sms.py`

**Si tous ces programmes fonctionnent, passez à la Partie 3 !**

---

## 📚 Partie 3 : Contrôle d'arrosage par SMS

Dans cette partie, nous allons créer un système complet de contrôle d'arrosage à distance par SMS.

### 3.1 Connexion des relais

#### Schéma de câblage

Les relais permettent de contrôler les électrovannes d'arrosage :

| Composant | GPIO | Pin | Fonction |
|-----------|------|-----|----------|
| Relais 1 | GPIO 16 | Pin 36 | Électrovanne 1 |
| Relais 2 | GPIO 26 | Pin 37 | Électrovanne 2 |
| GND | GND | Pin 39 | Masse commune |
| VCC | 5V | Pin 2 | Alimentation relais |

**⚠️ Important :**
- Les relais sont **actifs BAS** : GPIO=0 → relais FERMÉ (électrovanne ON)
- Les relais sont **inactifs HAUT** : GPIO=1 → relais OUVERT (électrovanne OFF)

#### Test simple des relais

Créez `test_relais.py` pour tester les GPIO :

```python
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RELAIS_1 = 16
RELAIS_2 = 26

# Initialisation des GPIO en sortie
GPIO.setup(RELAIS_1, GPIO.OUT)
GPIO.setup(RELAIS_2, GPIO.OUT)

# État initial : relais ouverts (électrovannes OFF)
GPIO.output(RELAIS_1, GPIO.HIGH)
GPIO.output(RELAIS_2, GPIO.HIGH)

print("Test des relais")
print("=" * 40)

try:
    print("Activation Relais 1 (3 secondes)...")
    GPIO.output(RELAIS_1, GPIO.LOW)  # Fermer relais
    time.sleep(3)
    GPIO.output(RELAIS_1, GPIO.HIGH)  # Ouvrir relais
    print("✓ Relais 1 OK\n")
    
    time.sleep(1)
    
    print("Activation Relais 2 (3 secondes)...")
    GPIO.output(RELAIS_2, GPIO.LOW)
    time.sleep(3)
    GPIO.output(RELAIS_2, GPIO.HIGH)
    print("✓ Relais 2 OK\n")
    
    print("✅ Test terminé")

except KeyboardInterrupt:
    print("\nInterrompu")

finally:
    GPIO.cleanup()
```

Testez :
```bash
python3 test_relais.py
```

---

### 3.2 Construction du programme de contrôle (avec aide d'une IA)

Nous allons maintenant créer le programme principal qui :
1. Reçoit les SMS
2. Vérifie si le SMS est valide
3. Contrôle les électrovannes

#### 🤖 Utilisation d'une IA pour vous aider

Vous allez utiliser une IA (ChatGPT, Claude, Gemini, etc.) pour vous assister dans la création du programme.

**Prompts suggérés étape par étape :**

---

**📝 Prompt 1 : Structure de base**

```
Je travaille sur un Raspberry Pi avec un module GSM SIM800C et des relais 
pour contrôler des électrovannes d'arrosage. Je veux créer un programme 
Python qui :

1. Lit les SMS reçus sur le port série /dev/ttyS0 à 115200 bauds
2. Vérifie si le SMS vient d'un numéro autorisé : +33612345678
3. Vérifie si le message a le format : "arrosage X = YY" où X=1 ou 2 et YY=on ou off
4. Contrôle les GPIO 16 (relais 1) et 26 (relais 2) en fonction du message
5. Les relais sont actifs BAS (0=fermé, 1=ouvert)

Peux-tu me créer la structure de base du programme avec :
- La fonction de lecture des SMS
- La fonction de validation du numéro
- La fonction de validation du format du message
```

Copiez le code fourni par l'IA et sauvegardez-le dans `arrosage_sms.py`.

---

**📝 Prompt 2 : Amélioration de la validation**

```
Dans le code précédent, améliore la fonction de validation du message pour :
- Accepter des espaces variables (ex: "arrosage 1=on" ou "arrosage  1 = on")
- Être insensible à la casse (ON, On, on)
- Détecter les erreurs de format et afficher un message clair
```

Intégrez les améliorations dans votre `arrosage_sms.py`.

---

**📝 Prompt 3 : Ajout de logs**

```
Ajoute un système de logs au programme pour :
- Enregistrer dans un fichier arrosage.log tous les SMS reçus
- Noter les actions effectuées (activation/désactivation des relais)
- Horodater chaque événement
- Utiliser le module logging de Python
```

---

**📝 Prompt 4 : Gestion d'erreurs robuste**

```
Améliore la gestion d'erreurs pour :
- Gérer les déconnexions du port série
- Réessayer automatiquement en cas d'échec de lecture SMS
- Envoyer un SMS de confirmation après chaque action réussie
- Gérer proprement l'arrêt du programme (Ctrl+C)
```

---

#### Code de référence complet

Voici un exemple de code complet `arrosage_sms.py` :

```python
#!/usr/bin/env python3
"""
Système de contrôle d'arrosage par SMS
Auteur : Votre nom
Date : 2025-01-10
"""

import serial
import time
import sys
import re
import RPi.GPIO as GPIO
import logging
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

# Port série
PORT = "/dev/ttyS0"
BAUDRATE = 115200
TIMEOUT = 1

# GPIO
RELAIS_1 = 16  # GPIO pour électrovanne 1
RELAIS_2 = 26  # GPIO pour électrovanne 2

# Sécurité
NUMERO_AUTORISE = "+33612345678"  # ⚠️ À MODIFIER avec votre numéro

# Logs
LOG_FILE = "/home/pi/arrosage.log"

# ============================================================================
# INITIALISATION DES LOGS
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# ============================================================================
# INITIALISATION DES GPIO
# ============================================================================

def init_gpio():
    """Initialise les GPIO pour les relais"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Configuration en sortie
    GPIO.setup(RELAIS_1, GPIO.OUT)
    GPIO.setup(RELAIS_2, GPIO.OUT)
    
    # État initial : relais ouverts (OFF)
    GPIO.output(RELAIS_1, GPIO.HIGH)
    GPIO.output(RELAIS_2, GPIO.HIGH)
    
    logging.info("GPIO initialisés - État initial : Relais 1=OFF, Relais 2=OFF")

# ============================================================================
# GESTION DU MODULE GSM
# ============================================================================

def init_gsm():
    """
    Initialise la connexion avec le module GSM
    
    Returns:
        serial.Serial: Objet de connexion série ou None si échec
    """
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
        time.sleep(2)
        
        # Test de communication
        ser.write(b'AT\r')
        time.sleep(0.5)
        reponse = ser.read(ser.in_waiting).decode(errors='ignore')
        
        if "OK" not in reponse:
            logging.error("Module GSM ne répond pas")
            return None
        
        # Configuration en mode texte
        ser.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        ser.read(ser.in_waiting)
        
        logging.info("Module GSM initialisé avec succès")
        return ser
        
    except Exception as e:
        logging.error(f"Erreur d'initialisation GSM : {e}")
        return None

def lire_sms(ser):
    """
    Lit tous les SMS non lus
    
    Args:
        ser: Connexion série
    
    Returns:
        list: Liste des SMS non lus
    """
    try:
        ser.write(b'AT+CMGL="REC UNREAD"\r')
        time.sleep(2)
        
        reponse = ser.read(ser.in_waiting).decode(errors='ignore')
        
        # Extraction des SMS
        liste_sms = []
        pattern = r'\+CMGL: (\d+),"([^"]+)","([^"]+)","[^"]*","([^"]+)"\r\n(.+?)(?=\r\n\+CMGL|\r\n\r\nOK)'
        
        matches = re.finditer(pattern, reponse, re.DOTALL)
        
        for match in matches:
            sms = {
                'index': match.group(1),
                'statut': match.group(2),
                'numero': match.group(3),
                'date': match.group(4),
                'message': match.group(5).strip()
            }
            liste_sms.append(sms)
        
        return liste_sms
        
    except Exception as e:
        logging.error(f"Erreur de lecture SMS : {e}")
        return []

def envoyer_sms_confirmation(ser, numero, message):
    """
    Envoie un SMS de confirmation
    
    Args:
        ser: Connexion série
        numero (str): Numéro destinataire
        message (str): Message à envoyer
    """
    try:
        commande = f'AT+CMGS="{numero}"\r'
        ser.write(commande.encode())
        time.sleep(0.5)
        
        ser.write(message.encode())
        ser.write(b'\x1A')
        time.sleep(3)
        
        logging.info(f"SMS de confirmation envoyé à {numero}")
        
    except Exception as e:
        logging.error(f"Erreur d'envoi SMS : {e}")

def effacer_sms(ser, index):
    """
    Efface un SMS par son index
    
    Args:
        ser: Connexion série
        index (str): Index du SMS
    """
    try:
        commande = f'AT+CMGD={index}\r'
        ser.write(commande.encode())
        time.sleep(0.5)
        ser.read(ser.in_waiting)
        
    except Exception as e:
        logging.error(f"Erreur d'effacement SMS : {e}")

# ============================================================================
# VALIDATION ET TRAITEMENT DES SMS
# ============================================================================

def valider_numero(numero):
    """
    Vérifie si le numéro est autorisé
    
    Args:
        numero (str): Numéro à vérifier
    
    Returns:
        bool: True si autorisé, False sinon
    """
    return numero == NUMERO_AUTORISE

def parser_commande(message):
    """
    Parse le message SMS pour extraire la commande
    Format attendu : "arrosage X = YY" où X=1 ou 2 et YY=on ou off
    
    Args:
        message (str): Message SMS
    
    Returns:
        dict: {'valide': bool, 'arrosage': int, 'action': str} ou None
    """
    # Normalisation : minuscules et suppression espaces superflus
    message = message.lower().strip()
    message = re.sub(r'\s+', ' ', message)
    
    # Pattern pour "arrosage X = YY"
    pattern = r'arrosage\s*(\d)\s*=\s*(on|off)'
    match = re.search(pattern, message)
    
    if not match:
        return None
    
    arrosage = int(match.group(1))
    action = match.group(2)
    
    # Vérification des valeurs
    if arrosage not in [1, 2]:
        return None
    
    if action not in ['on', 'off']:
        return None
    
    return {
        'valide': True,
        'arrosage': arrosage,
        'action': action
    }

def executer_commande(commande):
    """
    Execute la commande d'arrosage
    
    Args:
        commande (dict): Commande parsée
    
    Returns:
        str: Message de confirmation
    """
    arrosage = commande['arrosage']
    action = commande['action']
    
    # Sélection du GPIO
    gpio = RELAIS_1 if arrosage == 1 else RELAIS_2
    
    # Action
    if action == 'on':
        GPIO.output(gpio, GPIO.LOW)  # Activer (relais fermé)
        etat = "activé"
        logging.info(f"Arrosage {arrosage} ACTIVÉ")
    else:
        GPIO.output(gpio, GPIO.HIGH)  # Désactiver (relais ouvert)
        etat = "désactivé"
        logging.info(f"Arrosage {arrosage} DÉSACTIVÉ")
    
    return f"Arrosage {arrosage} {etat}"

# ============================================================================
# BOUCLE PRINCIPALE
# ============================================================================

def main():
    """Fonction principale"""
    print("=" * 70)
    print("Système de contrôle d'arrosage par SMS")
    print("=" * 70)
    logging.info("Démarrage du système")
    
    # Initialisation
    init_gpio()
    ser = init_gsm()
    
    if not ser:
        logging.error("Impossible de démarrer le système")
        sys.exit(1)
    
    print(f"\n✅ Système démarré")
    print(f"📱 Numéro autorisé : {NUMERO_AUTORISE}")
    print(f"📝 Logs : {LOG_FILE}")
    print(f"\n⏳ En attente de SMS...\n")
    
    try:
        while True:
            # Lecture des SMS
            sms_liste = lire_sms(ser)
            
            for sms in sms_liste:
                numero = sms['numero']
                message = sms['message']
                index = sms['index']
                
                logging.info(f"SMS reçu de {numero} : {message}")
                print(f"\n📨 Nouveau SMS de {numero}")
                print(f"   Message : {message}")
                
                # Vérification du numéro
                if not valider_numero(numero):
                    logging.warning(f"Numéro non autorisé : {numero}")
                    print(f"   ⚠️  Numéro non autorisé")
                    effacer_sms(ser, index)
                    continue
                
                # Parsing de la commande
                commande = parser_commande(message)
                
                if not commande:
                    logging.warning(f"Format de commande invalide : {message}")
                    print(f"   ✗ Format invalide")
                    msg_erreur = "Erreur: format attendu 'arrosage 1 = on' ou 'arrosage 2 = off'"
                    envoyer_sms_confirmation(ser, numero, msg_erreur)
                    effacer_sms(ser, index)
                    continue
                
                # Exécution de la commande
                confirmation = executer_commande(commande)
                print(f"   ✅ {confirmation}")
                
                # Envoi de la confirmation
                envoyer_sms_confirmation(ser, numero, confirmation)
                
                # Effacement du SMS traité
                effacer_sms(ser, index)
            
            # Attente avant la prochaine vérification
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Arrêt du système...")
        logging.info("Arrêt du système par l'utilisateur")
    
    except Exception as e:
        logging.error(f"Erreur critique : {e}")
        print(f"\n❌ Erreur : {e}")
    
    finally:
        # Nettoyage
        GPIO.cleanup()
        if ser:
            ser.close()
        logging.info("Système arrêté proprement")
        print("✅ Système arrêté")

if __name__ == "__main__":
    main()
```

---

### 3.3 Tests du programme

#### Test 1 : Format valide

Envoyez un SMS à votre carte SIM :
```
arrosage 1 = on
```

**Résultat attendu :**
- Le relais 1 doit se fermer (électrovanne 1 ON)
- Vous recevez un SMS : "Arrosage 1 activé"
- Le log enregistre l'action

---

#### Test 2 : Format invalide

Envoyez :
```
allume arrosage 1
```

**Résultat attendu :**
- Aucune action sur les relais
- Vous recevez un SMS d'erreur expliquant le bon format

---

#### Test 3 : Numéro non autorisé

Demandez à un ami d'envoyer un SMS à votre carte :
```
arrosage 1 = on
```

**Résultat attendu :**
- Aucune action
- SMS supprimé sans réponse
- Log enregistre la tentative

---

### 3.4 Lancement automatique au démarrage

Pour que le programme démarre automatiquement au boot du Raspberry Pi, nous allons créer un service systemd.

#### Création du service

Créez le fichier `/etc/systemd/system/arrosage.service` :

```bash
sudo nano /etc/systemd/system/arrosage.service
```

Contenu du fichier :

```ini
[Unit]
Description=Système de contrôle d'arrosage par SMS
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/arrosage_sms.py
Restart=always
RestartSec=10

# Logs
StandardOutput=append:/home/pi/arrosage_service.log
StandardError=append:/home/pi/arrosage_service.log

[Install]
WantedBy=multi-user.target
```

#### Activation du service

```bash
# Recharger la configuration systemd
sudo systemctl daemon-reload

# Activer le service au démarrage
sudo systemctl enable arrosage.service

# Démarrer le service maintenant
sudo systemctl start arrosage.service
```

#### Vérification

```bash
# Voir le statut
sudo systemctl status arrosage.service

# Voir les logs en temps réel
sudo journalctl -u arrosage.service -f

# Arrêter le service
sudo systemctl stop arrosage.service

# Redémarrer le service
sudo systemctl restart arrosage.service
```

#### Test de démarrage automatique

```bash
# Redémarrez le Raspberry Pi
sudo reboot

# Après redémarrage, vérifiez que le service tourne
sudo systemctl status arrosage.service
```

---

### ✅ Validation Partie 3

Vérifiez que vous avez réussi à :

- [ ] Connecter les relais aux GPIO 16 et 26
- [ ] Tester les relais individuellement
- [ ] Créer le programme `arrosage_sms.py`
- [ ] Tester l'envoi d'un SMS valide
- [ ] Vérifier le contrôle des électrovannes
- [ ] Tester un SMS avec format invalide
- [ ] Tester un SMS d'un numéro non autorisé
- [ ] Créer le service systemd
- [ ] Activer le démarrage automatique
- [ ] Vérifier les logs

---

## 📚 Partie 4 : Application Android avec App Inventor

Dans cette partie, nous allons créer une application Android pour contrôler facilement l'arrosage depuis votre smartphone.

### 4.1 Introduction à MIT App Inventor

**MIT App Inventor** est une plateforme de développement visuelle qui permet de créer des applications Android sans écrire de code complexe.

#### Accès à App Inventor

1. Allez sur : **https://appinventor.mit.edu**
2. Cliquez sur **"Create Apps!"**
3. Connectez-vous avec votre compte Google
4. Acceptez les conditions d'utilisation

---

### 4.2 Création d'un nouveau projet

1. Cliquez sur **"Start new project"**
2. Nommez votre projet : `Arrosage_SMS`
3. Cliquez sur **OK**

Vous êtes maintenant dans l'interface de design !

---

### 4.3 Design de l'interface (Designer)

#### 4.3.1 Configuration de l'écran principal

Dans la colonne de droite (**Properties**), configurez :

| Propriété | Valeur |
|-----------|--------|
| AppName | Contrôle Arrosage |
| Title | Arrosage SMS |
| ScreenOrientation | Portrait |
| BackgroundColor | Light Blue |

---

#### 4.3.2 Ajout d'un arrangement vertical

Dans **Palette** → **Layout** :
1. Glissez un **VerticalArrangement** sur l'écran
2. Propriétés :
   - Width : **Fill parent**
   - Height : **Fill parent**
   - AlignHorizontal : **Center**
   - AlignVertical : **Top**

---

#### 4.3.3 Ajout du titre

Dans **Palette** → **User Interface** :
1. Glissez un **Label** dans le VerticalArrangement
2. Propriétés :
   - Text : `🌱 Contrôle d'Arrosage`
   - FontSize : **24**
   - FontBold : **✓**
   - TextColor : **Green**
   - Width : **Fill parent**
   - TextAlignment : **Center**

---

#### 4.3.4 Ajout d'un séparateur

1. Ajoutez un **HorizontalArrangement**
   - Height : **20 pixels**

---

#### 4.3.5 Section Arrosage 1

Ajoutez un **Label** :
- Text : `Arrosage 1 :`
- FontSize : **18**
- FontBold : **✓**

Ajoutez un **HorizontalArrangement** :
- Width : **Fill parent**
- AlignHorizontal : **Center**

Dans ce HorizontalArrangement, ajoutez deux **Button** :

**Bouton 1 :**
- Text : `✅ ON`
- BackgroundColor : **Green**
- TextColor : **White**
- FontSize : **16**
- Width : **40%**
- Renommez-le : `Btn_Arrosage1_ON`

**Bouton 2 :**
- Text : `❌ OFF`
- BackgroundColor : **Red**
- TextColor : **White**
- FontSize : **16**
- Width : **40%**
- Renommez-le : `Btn_Arrosage1_OFF`

---

#### 4.3.6 Séparateur

Ajoutez un **HorizontalArrangement** : Height = **30 pixels**

---

#### 4.3.7 Section Arrosage 2

Répétez exactement la même structure pour l'Arrosage 2 :
- Label : `Arrosage 2 :`
- Deux boutons : `Btn_Arrosage2_ON` et `Btn_Arrosage2_OFF`

---

#### 4.3.8 Séparateur

Ajoutez un **HorizontalArrangement** : Height = **40 pixels**

---

#### 4.3.9 Section Paramètres

Ajoutez un **Label** :
- Text : `⚙️ Paramètres`
- FontSize : **18**
- FontBold : **✓**

Ajoutez un **Button** :
- Text : `📱 Configurer numéro`
- BackgroundColor : **Blue**
- TextColor : **White**
- Width : **80%**
- Renommez-le : `Btn_Config`

---

#### 4.3.10 Label de statut

Ajoutez un **Label** en bas de l'écran :
- Text : `Prêt`
- FontSize : **14**
- TextColor : **Gray**
- Width : **Fill parent**
- TextAlignment : **Center**
- Renommez-le : `Lbl_Statut`

---

#### 4.3.11 Composants non visibles

Dans **Palette** → **Storage** :
1. Glissez un **TinyDB** sur l'écran (il apparaît en bas)
   - Renommez-le : `TinyDB_Config`

Dans **Palette** → **Social** :
1. Glissez un **Texting** sur l'écran
   - Renommez-le : `SMS_Envoi`

Dans **Palette** → **User Interface** :
1. Glissez un **Notifier** sur l'écran
   - Renommez-le : `Notificateur`

---

### 4.4 Programmation (Blocks)

Cliquez sur **"Blocks"** en haut à droite pour passer en mode programmation.

---

#### 4.4.1 Initialisation de l'application

**Bloc à créer :** Quand l'écran s'initialise, charger le numéro sauvegardé

```
when Screen1.Initialize
do
  set SMS_Envoi.PhoneNumber to 
    call TinyDB_Config.GetValue
      tag: "numero_telephone"
      valueIfTagNotThere: ""
  
  if is empty SMS_Envoi.PhoneNumber
  then
    call Notificateur.ShowAlert
      notice: "Veuillez configurer le numéro de téléphone dans les paramètres"
  end if
end
```

**Comment faire :**
1. **Screen1** → **when Screen1.Initialize**
2. **SMS_Envoi** → **set SMS_Envoi.PhoneNumber to**
3. **TinyDB_Config** → **call TinyDB_Config.GetValue**
4. **Text** → `"numero_telephone"` et `""`
5. **Logic** → **if then**
6. **Text** → **is empty**
7. **Notificateur** → **call Notificateur.ShowAlert**

---

#### 4.4.2 Fonction d'envoi de SMS

**Créer une procédure personnalisée :**

```
procedure Envoyer_Commande (commande)
do
  if is empty SMS_Envoi.PhoneNumber
  then
    call Notificateur.ShowAlert
      notice: "Numéro non configuré !"
  else
    set SMS_Envoi.Message to commande
    call SMS_Envoi.SendMessageDirect
    
    set Lbl_Statut.Text to join("Envoi : " commande)
    set Lbl_Statut.TextColor to color Orange
  end if
end
```

**Comment faire :**
1. **Procedures** → **procedure** (nommez-la `Envoyer_Commande`)
2. Cliquez sur le **⚙️** → **input** → Nommez le paramètre `commande`
3. Ajoutez les blocs comme ci-dessus

---

#### 4.4.3 Bouton Arrosage 1 ON

```
when Btn_Arrosage1_ON.Click
do
  call Envoyer_Commande
    commande: "arrosage 1 = on"
end
```

---

#### 4.4.4 Bouton Arrosage 1 OFF

```
when Btn_Arrosage1_OFF.Click
do
  call Envoyer_Commande
    commande: "arrosage 1 = off"
end
```

---

#### 4.4.5 Bouton Arrosage 2 ON

```
when Btn_Arrosage2_ON.Click
do
  call Envoyer_Commande
    commande: "arrosage 2 = on"
end
```

---

#### 4.4.6 Bouton Arrosage 2 OFF

```
when Btn_Arrosage2_OFF.Click
do
  call Envoyer_Commande
    commande: "arrosage 2 = off"
end
```

---

#### 4.4.7 Configuration du numéro

```
when Btn_Config.Click
do
  set global Nouveau_Numero to 
    call Notificateur.ShowTextDialog
      message: "Entrez le numéro de téléphone (format international) :"
      title: "Configuration"
      cancelable: true
end

when Notificateur.AfterTextInput
do
  if is empty responseText
  then
    call Notificateur.ShowAlert
      notice: "Aucun numéro saisi"
  else
    set SMS_Envoi.PhoneNumber to responseText
    call TinyDB_Config.StoreValue
      tag: "numero_telephone"
      valueToStore: responseText
    
    call Notificateur.ShowAlert
      notice: join("Numéro configuré : " responseText)
    
    set Lbl_Statut.Text to "Numéro configuré ✓"
    set Lbl_Statut.TextColor to color Green
  end if
end
```

---

#### 4.4.8 Confirmation d'envoi

```
when SMS_Envoi.MessageSent
do
  call Notificateur.ShowToast
    message: "SMS envoyé ✓"
  
  set Lbl_Statut.Text to "SMS envoyé ✓"
  set Lbl_Statut.TextColor to color Green
end
```

---

### 4.5 Test de l'application

#### Test avec l'émulateur

1. Cliquez sur **"Connect"** → **AI Companion**
2. Installez **MIT AI2 Companion** sur votre smartphone Android (depuis Google Play Store)
3. Scannez le QR code affiché
4. L'application se charge sur votre téléphone !

#### Test des fonctionnalités

1. **Au premier lancement :**
   - L'application devrait demander de configurer le numéro

2. **Configuration du numéro :**
   - Cliquez sur "📱 Configurer numéro"
   - Entrez votre numéro (celui de la carte SIM du Raspberry Pi)
   - Format : `+33612345678`
   - Validez

3. **Test d'envoi :**
   - Cliquez sur "✅ ON" pour Arrosage 1
   - Vérifiez sur le Raspberry Pi que le relais s'active
   - Vérifiez que vous recevez un SMS de confirmation

4. **Test complet :**
   - Testez les 4 boutons (2 ON, 2 OFF)
   - Vérifiez les logs sur le Raspberry Pi

---

### 4.6 Compilation de l'APK

Pour installer l'application définitivement sur votre téléphone :

1. **Build** → **Android App (.apk)**
2. Attendez quelques minutes
3. Téléchargez l'APK ou scannez le QR code pour l'installer directement

**⚠️ Note :** Vous devrez peut-être autoriser l'installation d'applications provenant de sources inconnues dans les paramètres Android.

---

### 4.7 Améliorations possibles

Voici quelques idées pour améliorer votre application :

1. **Affichage de l'état actuel :**
   - Ajouter des labels pour afficher si chaque arrosage est ON ou OFF

2. **Historique :**
   - Logger les commandes envoyées dans TinyDB

3. **Timer :**
   - Ajouter la possibilité de programmer un arrosage pour une durée limitée

4. **Notifications :**
   - Recevoir les SMS de confirmation et les afficher dans l'app

5. **Multi-utilisateurs :**
   - Gérer plusieurs numéros autorisés

---

### ✅ Validation Partie 4

Vérifiez que vous avez réussi à :

- [ ] Créer le projet sur MIT App Inventor
- [ ] Designer l'interface avec les 4 boutons
- [ ] Ajouter le bouton de configuration
- [ ] Programmer les blocs de chaque bouton
- [ ] Créer la procédure d'envoi de SMS
- [ ] Implémenter le système de sauvegarde du numéro
- [ ] Tester l'application avec AI Companion
- [ ] Compiler l'APK
- [ ] Installer l'application sur votre smartphone
- [ ] Tester le contrôle complet de l'arrosage

---

## 🎓 Évaluation

### Format de l'évaluation

**Oral individuel de 10 minutes :**
- **5 minutes** : Présentation de votre projet
- **5 minutes** : Questions de l'examinateur

---

### Contenu de la présentation (5 min)

Préparez une démonstration en direct qui couvre :

#### 1. Démonstration technique (3 min)
- **Connexion au Raspberry Pi**
  - Montrer la connexion SSH
  - Afficher l'état du service `arrosage.service`
  - Montrer les logs en temps réel

- **Test d'envoi de SMS**
  - Utiliser l'application Android
  - Envoyer une commande (ex : arrosage 1 = on)
  - Montrer l'activation du relais (LED/électrovanne)
  - Afficher le SMS de confirmation reçu

- **Vérification des logs**
  - Afficher le fichier `arrosage.log`
  - Montrer la trace de la commande exécutée

#### 2. Explication du code (2 min)
- Expliquer brièvement le fonctionnement de `arrosage_sms.py`
- Montrer la fonction de validation du SMS
- Expliquer la gestion des GPIO
- Présenter l'interface de l'application Android

---

### Questions possibles de l'examinateur (5 min)

Préparez-vous à répondre à des questions du type :

#### Questions techniques
1. **Pourquoi utilise-t-on GPIO=0 pour fermer le relais ?**
2. **Quelle est la différence entre un SMS en mode texte et en mode PDU ?**
3. **Comment fonctionne la communication série avec le SIM800C ?**
4. **Pourquoi efface-t-on les SMS après traitement ?**
5. **Que fait la commande AT+CREG? ?**

#### Questions sur la sécurité
6. **Comment protéger le système contre des commandes non autorisées ?**
7. **Pourquoi est-il important de valider le numéro de l'expéditeur ?**
8. **Que se passe-t-il si quelqu'un devine le format de commande ?**

#### Questions de dépannage
9. **Que faire si le module GSM ne répond pas à AT ?**
10. **Comment diagnostiquer un problème de signal faible ?**
11. **Pourquoi le relais ne s'active pas alors que le SMS est bien reçu ?**

#### Questions d'amélioration
12. **Comment ajouteriez-vous un système de temporisation automatique ?**
13. **Comment permettre à plusieurs utilisateurs d'envoyer des commandes ?**
14. **Quelle amélioration apporteriez-vous à l'application Android ?**

---

### Grille d'évaluation

| Critère | Points | Détails |
|---------|--------|---------|
| **Fonctionnement du système** | /8 | Installation matérielle, communication GSM, contrôle des relais |
| **Qualité du code Python** | /4 | Structure, commentaires, gestion d'erreurs |
| **Application Android** | /3 | Interface, fonctionnalités, ergonomie |
| **Présentation orale** | /3 | Clarté, structure, démonstration |
| **Réponses aux questions** | /2 | Compréhension technique, capacité d'analyse |
| **TOTAL** | **/20** | |

---

### Conseils pour la présentation

✅ **À faire :**
- Tester tout votre système **avant** l'oral
- Préparer une démo fluide et rapide
- Avoir vos logs ouverts et visibles
- Montrer que vous comprenez ce que vous avez fait
- Expliquer vos choix techniques

❌ **À éviter :**
- Perdre du temps à chercher vos fichiers
- Lire vos notes mot à mot
- Utiliser un jargon incompréhensible
- Ne pas savoir répondre à "Comment ça marche ?"

---

## 📎 Annexes

### Annexe A : Récapitulatif des commandes AT importantes

| Commande | Description | Réponse |
|----------|-------------|---------|
| `AT` | Test de base | `OK` |
| `AT+CPIN?` | État de la SIM | `+CPIN: READY` |
| `AT+CSQ` | Signal (0-31) | `+CSQ: 28,0` |
| `AT+CREG?` | Enregistrement réseau | `+CREG: 0,1` |
| `AT+CMGF=1` | Mode SMS texte | `OK` |
| `AT+CMGS="num"` | Envoyer SMS | `+CMGS: 42` |
| `AT+CMGL="ALL"` | Lire tous SMS | Liste SMS |
| `AT+CMGD=1,4` | Effacer tous SMS | `OK` |
| `ATI` | Infos module | `SIM800C R14.18` |

---

### Annexe B : Pinout Raspberry Pi 3

```
3V3  (1) (2)  5V
GPIO2  (3) (4)  5V
GPIO3  (5) (6)  GND
GPIO4  (7) (8)  GPIO14 (TXD)
GND  (9) (10) GPIO15 (RXD)
...
GPIO16 (36) (37) GPIO26
GND (39) (40) GPIO21
```

---

### Annexe C : Dépannage courant

#### Problème : Le module ne répond pas à AT

**Solutions :**
1. Vérifier l'alimentation (LED allumée ?)
2. Vérifier le câblage TXD/RXD
3. Redémarrer le Raspberry Pi
4. Vérifier avec `ls -l /dev/ttyS0`

---

#### Problème : Pas de signal (CSQ = 99)

**Solutions :**
1. Vérifier l'antenne
2. Déplacer le module près d'une fenêtre
3. Attendre quelques minutes (recherche réseau)
4. Vérifier que la carte SIM a du crédit

---

#### Problème : Le relais ne s'active pas

**Solutions :**
1. Tester avec `test_relais.py`
2. Vérifier le câblage des GPIO
3. Vérifier l'alimentation 5V des relais
4. Utiliser un multimètre pour tester la sortie GPIO

---

#### Problème : SMS non reçus

**Solutions :**
1. Vérifier le crédit SMS
2. Tester avec `recevoir_sms.py`
3. Vérifier `AT+CMGL="ALL"`
4. Attendre quelques secondes (délai réseau)

---

### Annexe D : Ressources supplémentaires

**Documentation :**
- Datasheet SIM800C : [lien fabricant]
- Guide Raspberry Pi GPIO : https://pinout.xyz
- MIT App Inventor : https://appinventor.mit.edu
- Commandes AT : https://www.waveshare.com/wiki/SIM800C_GSM/GPRS_HAT

**Tutoriels vidéo :**
- Installation SIM800C sur Raspberry Pi
- Introduction à MIT App Inventor
- Contrôle de relais avec Python

---

## 📝 Checklist finale

Avant de passer l'évaluation, assurez-vous d'avoir :

### Matériel
- [ ] Raspberry Pi 3 fonctionnel
- [ ] Carte SIM800C connectée
- [ ] Carte SIM avec crédit
- [ ] 2 relais câblés sur GPIO 16 et 26
- [ ] Smartphone Android avec l'application installée

### Logiciel
- [ ] Raspberry Pi OS Legacy Lite installé
- [ ] Port série configuré
- [ ] Python et bibliothèques installés
- [ ] Tous les scripts Python créés et testés
- [ ] Service systemd configuré et actif
- [ ] Application Android fonctionnelle

### Tests validés
- [ ] Communication AT réussie
- [ ] Envoi de SMS fonctionnel
- [ ] Réception de SMS fonctionnelle
- [ ] Contrôle des relais opérationnel
- [ ] Validation du format des commandes
- [ ] Sécurité par numéro autorisé
- [ ] Démarrage automatique testé
- [ ] Application Android testée bout en bout

### Documentation
- [ ] Logs consultables
- [ ] Code commenté
- [ ] Numéro de test configuré
- [ ] Présentation orale préparée

---

## 🎉 Conclusion

Félicitations ! Vous avez créé un système complet de contrôle d'arrosage à distance par SMS.

**Vous avez appris à :**
- ✅ Configurer un module GSM sur Raspberry Pi
- ✅ Communiquer en série avec des commandes AT
- ✅ Développer en Python avec gestion d'erreurs
- ✅ Contrôler des GPIO et des relais
- ✅ Créer un service système Linux
- ✅ Développer une application Android
- ✅ Mettre en place un système de sécurité par SMS

**Ce projet est une base solide** pour de nombreuses applications IoT : alarmes, serres automatisées, contrôle d'éclairage, notifications d'événements, etc.

Bonne chance pour votre évaluation ! 🚀

---

**Version :** 1.0  
**Date :** Janvier 2025  
**Auteur :** Votre établissement
