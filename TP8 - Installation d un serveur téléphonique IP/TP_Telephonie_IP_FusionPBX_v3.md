# TP - Mise en place d'une plateforme de téléphonie IP avec FusionPBX

## Objectifs pédagogiques

- Installer et configurer un serveur de téléphonie IP (IPBX) avec FusionPBX
- Comprendre l'architecture d'un système de téléphonie sur IP
- Câbler et configurer un réseau VoIP complet
- Configurer différents types de terminaux (IP, analogiques, softphone)
- Mettre en place une passerelle SIP vers un réseau principal

## Prérequis

- Connaissances en réseaux informatiques (TCP/IP, routage, NAT)
- Bases Linux (ligne de commande, gestion de services)
- Notions de protocoles VoIP (SIP, RTP)

## Matériel nécessaire

- 1 PC Ubuntu x86_64 (minimum 2 Go RAM) → Serveur FusionPBX
- 1 Routeur TP-LINK TL-WR841N V14
- 1 Switch Ethernet
- 1 Adaptateur SPA112 Cisco (2 ports FXS)
- 2 téléphones IP Grandstream GXV3240
- 2 téléphones analogiques Alcatel
- 1 PC Windows → Administration
- 1 Smartphone Android avec Wi-Fi
- Câbles Ethernet RJ45

## Durée estimée

6 heures (sur 2 séances)

---

## Partie 1 : Raccordement au réseau principal et accès Internet

> Cette étape est indispensable pour permettre l'installation de FusionPBX qui nécessite un accès Internet.

### 1.1 Architecture cible

Le réseau VoIP (192.169.0.0/24) sera raccordé au réseau principal via le routeur TP-LINK. Le port WAN du routeur se connecte au réseau principal, les équipements VoIP se connectent côté LAN.

```
Réseau principal (ex: 192.168.1.0/24)
            |
     [Port WAN du routeur TP-LINK]
            |
     TP-LINK TL-WR841N (192.169.0.1)
            |
     [Port LAN → Switch]
            |
    Réseau VoIP (192.169.0.0/24)
```

### 1.2 Câblage initial

1. **Connecter le port WAN du routeur TP-LINK** au réseau principal (prise murale ou switch du réseau principal)

2. **Connecter au switch VoIP** :
   - PC Ubuntu (serveur FusionPBX)
   - PC Windows (administration)
   - Port LAN du routeur TP-LINK

> Les téléphones IP, SPA112 et smartphone seront connectés en Partie 3 après l'installation.

### 1.3 Configuration du routeur TP-LINK

1. Connecter le PC Windows au switch et accéder à : http://192.168.0.1
   (adresse par défaut du TP-LINK, vérifier sous l'appareil)
2. Login : **admin / admin**

**Configuration WAN**

3. Menu : **Network** → **WAN**
4. WAN Connection Type : **DHCP** (ou Static IP selon le réseau principal)
5. Si Static IP, renseigner une adresse libre sur le réseau principal :
   - IP Address : 192.168.1.50
   - Subnet Mask : 255.255.255.0
   - Default Gateway : 192.168.1.1
   - DNS : 8.8.8.8
6. **Save**

**Configuration LAN**

7. Menu : **Network** → **LAN**
8. Paramètres :
   - IP Address : 192.169.0.1
   - Subnet Mask : 255.255.255.0
9. **Save** (le routeur redémarre)

**Configuration DHCP**

10. Menu : **DHCP** → **DHCP Settings**
11. Paramètres :
    - DHCP Server : **Enable**
    - Start IP : 192.169.0.100
    - End IP : 192.169.0.200
    - Default Gateway : 192.169.0.1
    - DNS : 8.8.8.8
12. **Save**

**Configuration Wi-Fi**

13. Menu : **Wireless** → **Basic Settings**
    - SSID : CEI1
14. Menu : **Wireless** → **Wireless Security**
    - Mot de passe : btsciellllb2a
15. **Save**

**Vérification de l'accès Internet**

16. Depuis le PC Windows (IP obtenue en DHCP), tester :
    ```cmd
    ping 8.8.8.8
    ping google.com
    ```
    Les deux doivent répondre.

**Questions de contrôle :**

1. Quel est le rôle du port WAN du routeur ?
2. Quelle est la différence entre NAT et routage ?
3. Pourquoi le réseau VoIP est-il séparé du réseau principal ?

---

## Partie 2 : Installation du serveur FusionPBX sur PC Ubuntu

### 2.1 Installation d'Ubuntu Server

**Téléchargement**

1. Télécharger Ubuntu Server LTS depuis :
   - https://ubuntu.com/download/server
   - Choisir la version **LTS 22.04 ou 24.04**

2. Flasher la clé USB avec Rufus (Windows) :
   - https://rufus.ie/

**Installation**

3. Démarrer sur la clé USB et suivre l'assistant :
   - Langue : French ou English
   - Disposition clavier : French
   - Type d'installation : **Ubuntu Server (minimized)**
   - Configuration réseau : laisser en **DHCP** pour l'instant
   - Pas de proxy
   - Miroir : laisser par défaut
   - Partitionnement : utiliser le disque entier
   - Profil : définir nom d'utilisateur et mot de passe
   - **Activer OpenSSH server**
   - Pas de snaps supplémentaires
   - Lancer l'installation et redémarrer

4. Se connecter en SSH depuis le PC Windows :
   ```cmd
   ssh utilisateur@<ip_dhcp_du_serveur>
   ```
   > Pour trouver l'IP DHCP du serveur : se connecter directement sur le PC Ubuntu et taper `ip a`

5. Mettre à jour le système :
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo reboot
   ```

### 2.2 Installation de FusionPBX

FusionPBX repose sur **FreeSWITCH** (moteur de téléphonie), **PostgreSQL** (base de données), **Nginx** (serveur web) et **PHP**. Le script officiel installe et configure tous ces composants automatiquement.

**Ressources pédagogiques :**
- FusionPBX : https://docs.fusionpbx.com/
- FreeSWITCH : https://freeswitch.org/
- Qu'est-ce qu'un IPBX : https://fr.wikipedia.org/wiki/IP_PBX

**Installation via le script officiel**

1. Se connecter en root :
   ```bash
   sudo su -
   ```

2. Installer git :
   ```bash
   apt-get install -y git
   ```

3. Cloner le dépôt d'installation :
   ```bash
   cd /tmp
   git clone https://github.com/fusionpbx/fusionpbx-install.sh.git
   ```

4. Lancer le script Ubuntu :
   ```bash
   cd /tmp/fusionpbx-install.sh/ubuntu
   bash install.sh
   ```

   > ⚠️ L'installation prend **15 à 20 minutes**. Ne pas interrompre.

5. À la fin, noter les identifiants affichés :
   ```
   Installation complete.
   URL:      https://<ip_dhcp>
   Username: admin
   Password: XXXXXXXXXXXXXXXX
   ```

**Vérification des services**

6. Vérifier que tous les services sont actifs :
   ```bash
   systemctl status freeswitch
   systemctl status nginx
   systemctl status postgresql
   systemctl status php*-fpm
   ```
   Tous doivent afficher **active (running)**.

7. Accéder à l'interface web depuis le PC Windows :
   - Ouvrir un navigateur : https://\<ip_dhcp_du_serveur\>
   - Accepter l'avertissement de certificat auto-signé
   - Se connecter avec les identifiants fournis

**Questions de contrôle :**

1. Quel est le rôle de FreeSWITCH dans l'architecture FusionPBX ?
2. Quel port est utilisé par le protocole SIP ?
3. Pourquoi utilise-t-on une plage de ports UDP (16384-16394) ?
4. Quelle est la différence entre FusionPBX et FreeSWITCH ?

---

## Partie 3 : Configuration du réseau VoIP

### 3.1 Configuration IP statique du serveur FusionPBX

Maintenant que FusionPBX est installé, on attribue une IP statique au serveur.

1. Sur le PC Ubuntu :
   ```bash
   sudo nano /etc/netplan/00-installer-config.yaml
   ```

2. Modifier comme suit :
   ```yaml
   network:
     version: 2
     ethernets:
       eth0:
         addresses:
           - 192.169.0.2/24
         routes:
           - to: default
             via: 192.169.0.1
         nameservers:
           addresses: [8.8.8.8, 8.8.4.4]
         dhcp4: false
   ```

   > ⚠️ Remplacer `eth0` par le nom réel de l'interface (`ip a` pour le trouver)

3. Appliquer la configuration :
   ```bash
   sudo netplan apply
   ```

4. Vérifier la nouvelle IP :
   ```bash
   ip a
   ping 192.169.0.1
   ```

5. Se reconnecter en SSH avec la nouvelle IP :
   ```cmd
   ssh utilisateur@192.169.0.2
   ```

### 3.2 Câblage complet du réseau VoIP

Compléter le câblage avec tous les équipements :

**Plan d'adressage IP**

| Équipement | Interface | Adresse IP | Passerelle | Remarques |
|------------|-----------|------------|------------|-----------|
| PC Ubuntu | eth0 | 192.169.0.2/24 | 192.169.0.1 | Serveur FusionPBX |
| IP Phone 0 | eth0 | 192.169.0.3/24 | 192.169.0.1 | Grandstream GXV3240 |
| IP Phone 1 | eth0 | 192.169.0.4/24 | 192.169.0.1 | Grandstream GXV3240 |
| PC Windows | eth0 | 192.169.0.5/24 | 192.169.0.1 | Administration |
| SPA112 | eth0 | 192.169.0.6/24 | 192.169.0.1 | Adaptateur analogique |
| Routeur TP-LINK | LAN | 192.169.0.1/24 | - | Passerelle/DHCP |
| Smartphone | wlan0 | DHCP | 192.169.0.1 | Linphone Android |

**Câblage**

1. Connecter au switch :
   - IP Phone 0 et IP Phone 1
   - Adaptateur SPA112

2. Connecter les téléphones analogiques :
   - Téléphone Alcatel 1 → Port FXS 1 du SPA112
   - Téléphone Alcatel 2 → Port FXS 2 du SPA112

3. Connecter le smartphone au Wi-Fi CEI1 (MDP : btsciellllb2a)

**Questions de contrôle :**

1. Pourquoi utilise-t-on un adaptateur SPA112 ?
2. Quelle est la différence entre un téléphone IP et un téléphone analogique ?
3. Pourquoi attribue-t-on des IP statiques aux équipements VoIP ?

---

## Partie 4 : Configuration des terminaux VoIP

### 4.1 Création des extensions dans FusionPBX

1. Depuis le PC Windows : https://192.169.0.2
2. Menu : **Accounts** → **Extensions**

**Créer 5 extensions :**

| Extension | Nom d'affichage | Équipement | Mot de passe |
|-----------|-----------------|------------|--------------|
| 7950 | IP Phone 0 | Grandstream GXV3240 | ipsecure01 |
| 7951 | IP Phone 1 | Grandstream GXV3240 | ipsecure02 |
| 7952 | Analog Phone 0 | Alcatel via SPA112 Line 1 | anasecure01 |
| 7953 | Analog Phone 1 | Alcatel via SPA112 Line 2 | anasecure02 |
| 7954 | Smartphone | Linphone Android | mobilesecure |

**Paramètres pour chaque extension :**
- **Add Extension**
- **Extension** : Numéro
- **Effective Caller ID Name** : Nom d'affichage
- **Effective Caller ID Number** : Numéro
- **Password** : Mot de passe
- **Enabled** : True
- **Voicemail Enabled** : True
- **Save**

### 4.2 Configuration des téléphones IP Grandstream GXV3240

**IP Phone 0 (192.169.0.3)**

1. Connecter au switch et alimenter

2. Configuration IP statique :
   - **Menu** → **Settings** → **Network Settings**
   - IPv4 Address Type : **Static IP**
   - Static IP : 192.169.0.3
   - Subnet Mask : 255.255.255.0
   - Default Gateway : 192.169.0.1
   - DNS : 8.8.8.8

3. Configuration SIP :
   - **Menu** → **Settings** → **Accounts** → **Account 1**
   - Account Active : **Yes**
   - SIP Server : 192.169.0.2
   - SIP User ID : 7950
   - Authenticate ID : 7950
   - Authenticate Password : ipsecure01
   - Name : IP Phone 0
   - **Save and Apply**

4. Redémarrer le téléphone

**IP Phone 1 (192.169.0.4)**

Répéter avec :
- IP : 192.169.0.4
- Extension : 7951 / ipsecure02

**Vérification :** FusionPBX → **Status** → **Registrations** : les deux téléphones doivent être **Registered**

### 4.3 Configuration de l'adaptateur SPA112

1. Accéder à : http://192.169.0.6 → **Admin Login** → **Advanced**

**Configuration réseau**
- **Router** → **Network** → Static IP : 192.169.0.6 / 255.255.255.0 / GW : 192.169.0.1
- **Submit All Changes**

**Line 1 (Alcatel 1)**
- **Voice** → **Line 1**
- Line Enable : Yes / Proxy : 192.169.0.2 / User ID : 7952 / Password : anasecure01
- **Submit All Changes**

**Line 2 (Alcatel 2)**
- **Voice** → **Line 2**
- Line Enable : Yes / Proxy : 192.169.0.2 / User ID : 7953 / Password : anasecure02
- **Submit All Changes**

- **System** → **Reboot**

### 4.4 Configuration de Linphone sur Android

1. Connecter au Wi-Fi : SSID CEI1 / MDP : btsciellllb2a
2. Installer **Linphone** (Google Play Store)
3. **Assistant** → **Use SIP account**
4. Paramètres :
   - Username : 7954 / Password : mobilesecure
   - Domain : 192.169.0.2 / Transport : UDP
5. **Login**

Vérifier dans FusionPBX que l'extension 7954 est **Registered**.

**Questions de contrôle :**

1. Qu'est-ce qu'un codec audio ? Citez-en deux utilisés en VoIP.
2. Quelle est la fonction du protocole RTP ?
3. Comment vérifier qu'un téléphone est bien enregistré sur le serveur SIP ?

---

## Partie 5 : Tests de fonctionnement

### 5.1 Tests d'appels internes

**Tableau de tests à compléter :**

| Depuis | Vers | Sonnerie OK | Conversation OK | Qualité audio | Remarques |
|--------|------|-------------|-----------------|---------------|-----------|
| 7950 | 7951 | ☐ | ☐ | | |
| 7950 | 7952 | ☐ | ☐ | | |
| 7951 | 7953 | ☐ | ☐ | | |
| 7952 | 7950 | ☐ | ☐ | | |
| 7954 | 7951 | ☐ | ☐ | | |

### 5.2 Test de la messagerie vocale

1. Appeler une extension, laisser sonner sans décrocher
2. Laisser un message après le bip
3. Composer `*97` depuis le téléphone destinataire
4. Écouter le message

### 5.3 Capture de trafic SIP avec Wireshark

1. Installer Wireshark sur le PC Windows
2. Lancer une capture sur l'interface Ethernet
3. Filtre : `sip or rtp`
4. Effectuer un appel entre deux extensions
5. Observer : INVITE → 100 Trying → 180 Ringing → 200 OK → ACK → BYE

**Questions d'analyse :**

1. Identifiez les adresses IP source et destination dans les paquets SIP.
2. Quel codec audio est négocié lors de l'établissement d'appel ?
3. Sur quels ports UDP circulent les flux RTP ?
4. Quelle est la différence entre SIP et RTP ?

---

## Partie 6 : Administration et dépannage

### 6.1 Consultation des logs

```bash
# Logs FreeSWITCH en temps réel
tail -f /var/log/freeswitch/freeswitch.log

# Console FreeSWITCH interactive
fs_cli

# Logs Nginx
tail -f /var/log/nginx/error.log

# État des services
systemctl status freeswitch nginx postgresql php*-fpm
```

### 6.2 Dépannage courant

**Extension non enregistrée**
1. Vérifier la configuration SIP sur le terminal
2. Tester : `ping 192.169.0.2`
3. Consulter : `tail -f /var/log/freeswitch/freeswitch.log`

**Pas de son lors d'un appel**
1. Vérifier les ports RTP (16384-16394 UDP)
2. Vérifier la configuration des codecs
3. Vérifier la configuration NAT

**Analyser le trafic SIP**
```bash
sudo apt install sngrep
sudo sngrep
```

### 6.3 Sauvegarde

```bash
# Base de données
pg_dump -U fusionpbx fusionpbx > backup_$(date +%Y%m%d).sql

# Configuration
tar -czf backup_config_$(date +%Y%m%d).tar.gz /etc/freeswitch /var/www/fusionpbx
```

---

## Évaluation

### Critères d'évaluation (sur 20 points)

| Critère | Points | Détail |
|---------|--------|--------|
| **Raccordement réseau principal** | 2 | Accès Internet fonctionnel |
| **Installation serveur** | 4 | Ubuntu installé, FusionPBX accessible |
| **Câblage réseau VoIP** | 2 | Câblage conforme, adressage IP correct |
| **Configuration extensions** | 4 | 5 extensions créées et fonctionnelles |
| **Tests d'appels** | 4 | Tous les appels internes fonctionnent |
| **Capture Wireshark** | 2 | Capture réalisée, questions répondues |
| **Qualité du compte-rendu** | 2 | Document structuré, copies d'écran |

### Livrables attendus

1. **Compte-rendu technique** (PDF) :
   - Copies d'écran de chaque étape
   - Tableau de tests complété
   - Capture Wireshark annotée
   - Réponses aux questions de contrôle

2. **Démonstration pratique** :
   - Appel entre deux terminaux
   - Extensions enregistrées visibles dans FusionPBX
   - Message vocal laissé et écouté

---

## Ressources complémentaires

- FusionPBX : https://docs.fusionpbx.com/
- Script d'installation : https://github.com/fusionpbx/fusionpbx-install.sh
- FreeSWITCH : https://freeswitch.org/confluence/
- Linphone : https://www.linphone.org/
- RFC 3261 (SIP) : https://www.rfc-editor.org/rfc/rfc3261
- RFC 3550 (RTP) : https://www.rfc-editor.org/rfc/rfc3550

---

## Consignes de sécurité

⚠️ **IMPORTANT**

- Ne jamais exposer le serveur SIP directement sur Internet
- Utiliser des mots de passe forts (minimum 12 caractères)
- Mettre à jour régulièrement le système et FusionPBX
- Désactiver les comptes non utilisés
- Activer fail2ban pour bloquer les tentatives d'intrusion SIP

---

## Annexes

### Annexe A : Codecs audio VoIP courants

| Codec | Bande passante | Qualité | Utilisation |
|-------|---------------|---------|-------------|
| G.711 (PCMU/PCMA) | 64 kbit/s | Excellente | Réseau local |
| G.722 | 64 kbit/s | HD | VoIP haute qualité |
| G.729 | 8 kbit/s | Bonne | Lien WAN limité |
| Opus | Variable | Excellente | Standard moderne |

### Annexe B : Codes de réponse SIP

| Code | Signification |
|------|---------------|
| 100 | Trying |
| 180 | Ringing |
| 200 | OK |
| 401 | Unauthorized |
| 404 | Not Found |
| 486 | Busy Here |
| 603 | Decline |

### Annexe C : Commandes fs_cli utiles

```bash
sofia status profile internal reg   # Extensions enregistrées
show calls                           # Appels en cours
sofia profile internal rescan        # Recharger la config SIP
sofia status                         # État des profils SIP
```

---

**Version :** 3.0
**Date :** Février 2026
**Auteur :** Olivier - BTS CIEL
