# TP - Mise en place d'une plateforme de téléphonie IP avec FusionPBX

## Objectifs pédagogiques

- Installer et configurer un serveur de téléphonie IP (IPBX) avec FusionPBX
- Comprendre l'architecture d'un système de téléphonie sur IP
- Câbler et configurer un réseau VoIP complet
- Configurer différents types de terminaux (IP, analogiques, softphone)
- Mettre en place une passerelle SIP vers un réseau externe

## Prérequis

- Connaissances en réseaux informatiques (TCP/IP, routage, NAT)
- Bases Linux (ligne de commande, gestion de services)
- Notions de protocoles VoIP (SIP, RTP)

## Matériel nécessaire

- 1 Raspberry Pi 4 (minimum 2 Go RAM)
- 1 Routeur TP-LINK TL-WR841N V14
- 1 Switch Ethernet
- 1 Adaptateur SPA112 Cisco (2 ports FXS)
- 2 téléphones IP Grandstream GXV3240
- 2 téléphones analogiques Alcatel
- 1 PC Windows
- 1 Smartphone Android avec Wi-Fi
- Câbles Ethernet RJ45

## Durée estimée

6 heures (sur 2 séances)

---

## Partie 1 : Installation du serveur FusionPBX sur Raspberry Pi

### 1.1 Installation de Debian Trixie (sans interface graphique)

**Téléchargement et préparation**

1. Télécharger l'image Raspberry Pi OS Lite (Debian Trixie) depuis :
   - https://www.raspberrypi.com/software/operating-systems/

2. Flasher la carte SD avec Raspberry Pi Imager :
   - https://www.raspberrypi.com/software/

3. Avant le premier démarrage, configurer SSH via Raspberry Pi Imager :
   - Cliquer sur l'icône engrenage (paramètres avancés)
   - Activer SSH
   - Définir nom d'utilisateur et mot de passe

**Premier démarrage et configuration de base**

4. Insérer la carte SD et démarrer le Raspberry Pi

5. Se connecter en SSH :
   ```bash
   ssh pi@192.169.0.2
   ```

6. Mettre à jour le système :
   ```bash
   sudo apt update
   sudo apt upgrade -y
   sudo reboot
   ```

7. Configurer une IP statique :
   ```bash
   sudo nano /etc/network/interfaces
   ```

   Ajouter :
   ```
   auto eth0
   iface eth0 inet static
       address 192.169.0.2
       netmask 255.255.255.0
       gateway 192.169.0.1
       dns-nameservers 8.8.8.8
   ```

8. Redémarrer le service réseau :
   ```bash
   sudo systemctl restart networking
   ```

---

### 1.2 - VARIANTE A : Installation de FusionPBX avec Docker

**Qu'est-ce que Docker ?**

Docker est une plateforme de conteneurisation qui permet d'isoler des applications dans des conteneurs légers. Contrairement aux machines virtuelles, les conteneurs partagent le noyau du système hôte, ce qui les rend plus rapides et moins gourmands en ressources.

**Ressources pédagogiques :**
- Introduction à Docker : https://docs.docker.com/get-started/overview/
- Docker pour débutants : https://docker-curriculum.com/

**Installation de Docker**

1. Installer les dépendances :
   ```bash
   sudo apt install -y ca-certificates curl gnupg lsb-release
   ```

2. Ajouter la clé GPG officielle de Docker :
   ```bash
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg
   ```

3. Ajouter le dépôt Docker :
   ```bash
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

4. Installer Docker :
   ```bash
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```

5. Ajouter l'utilisateur au groupe docker :
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

6. Vérifier l'installation :
   ```bash
   docker --version
   docker compose version
   ```

**Déploiement de FusionPBX**

1. Créer le répertoire du projet :
   ```bash
   mkdir ~/fusionpbx
   cd ~/fusionpbx
   ```

2. Créer le fichier `docker-compose.yml` :
   ```bash
   nano docker-compose.yml
   ```

3. Copier la configuration suivante :
   ```yaml
   version: '3.8'

   services:
     postgres:
       image: postgres:15-alpine
       container_name: fusionpbx-postgres
       restart: unless-stopped
       environment:
         POSTGRES_DB: fusionpbx
         POSTGRES_USER: fusionpbx
         POSTGRES_PASSWORD: fusionpbx123
       volumes:
         - postgres_data:/var/lib/postgresql/data
       networks:
         - fusionpbx

     fusionpbx:
       image: fusionpbx/fusionpbx:latest
       container_name: fusionpbx
       restart: unless-stopped
       ports:
         - "80:80"
         - "443:443"
         - "5060:5060/udp"
         - "5060:5060/tcp"
         - "5080:5080/udp"
         - "5080:5080/tcp"
         - "16384-16394:16384-16394/udp"
       environment:
         DATABASE_HOST: postgres
         DATABASE_NAME: fusionpbx
         DATABASE_USERNAME: fusionpbx
         DATABASE_PASSWORD: fusionpbx123
       depends_on:
         - postgres
       volumes:
         - fusionpbx_data:/var/www/fusionpbx
       networks:
         - fusionpbx

   networks:
     fusionpbx:
       driver: bridge

   volumes:
     postgres_data:
     fusionpbx_data:
   ```

4. Démarrer les conteneurs :
   ```bash
   docker compose up -d
   ```

5. Vérifier que les conteneurs sont actifs :
   ```bash
   docker compose ps
   ```

6. Accéder à l'interface web depuis le PC Windows :
   - Ouvrir un navigateur : http://192.169.0.2
   - Suivre l'assistant de configuration initial
   - Identifiants par défaut : admin / fusionpbx

---

### 1.2 - VARIANTE B : Installation de FusionPBX sans Docker (installation native)

Cette variante installe FusionPBX directement sur le système Debian, sans couche de conteneurisation. Elle est plus proche d'une installation en production et permet de mieux comprendre les composants du système.

**Composants installés :**
- FreeSWITCH (moteur de téléphonie)
- FusionPBX (interface web de gestion)
- PostgreSQL (base de données)
- Nginx (serveur web)
- PHP (moteur de scripts)

**Installation automatisée via le script officiel**

FusionPBX fournit un script d'installation officiel qui installe et configure tous les composants automatiquement.

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

4. Rendre le script exécutable et le lancer :
   ```bash
   chmod +x /tmp/fusionpbx-install.sh/debian/install.sh
   /tmp/fusionpbx-install.sh/debian/install.sh
   ```

5. Le script pose quelques questions :
   - Confirmer le nom de domaine ou l'adresse IP du serveur : **192.169.0.2**
   - Le script installe automatiquement tous les composants (durée : 10 à 20 minutes)

6. À la fin de l'installation, le script affiche les identifiants générés :
   ```
   Installation complete.
   URL:      https://192.169.0.2
   Username: admin
   Password: XXXXXXXXXXXXXXXX  ← noter ce mot de passe !
   ```

> ⚠️ **Important :** Noter impérativement le mot de passe affiché à la fin du script.

**Vérification des services**

7. Vérifier que FreeSWITCH est actif :
   ```bash
   systemctl status freeswitch
   ```

8. Vérifier que Nginx est actif :
   ```bash
   systemctl status nginx
   ```

9. Vérifier que PostgreSQL est actif :
   ```bash
   systemctl status postgresql
   ```

10. Accéder à l'interface web depuis le PC Windows :
    - Ouvrir un navigateur : https://192.169.0.2
    - Accepter l'avertissement de certificat auto-signé
    - Se connecter avec les identifiants fournis par le script

**Commandes utiles pour la variante native**

```bash
# Redémarrer FreeSWITCH
systemctl restart freeswitch

# Voir les logs FreeSWITCH en temps réel
fs_cli -x "console loglevel debug"

# Accéder à la console FreeSWITCH
fs_cli

# Redémarrer Nginx
systemctl restart nginx

# Voir les logs Nginx
tail -f /var/log/nginx/error.log
```

**Comparaison des deux variantes**

| Critère | Variante A (Docker) | Variante B (Native) |
|---------|---------------------|---------------------|
| Facilité d'installation | ★★★★☆ | ★★★☆☆ |
| Compréhension du système | ★★☆☆☆ | ★★★★★ |
| Isolation des services | ★★★★★ | ★★☆☆☆ |
| Consommation mémoire | Plus élevée | Plus faible |
| Mise à jour | Facile (image Docker) | Manuelle |
| Recommandé pour | Déploiement rapide | Apprentissage approfondi |

**Questions de contrôle (communes aux deux variantes) :**

1. Quelle est la différence entre une machine virtuelle et un conteneur Docker ?
2. Quel port est utilisé par le protocole SIP ?
3. Pourquoi ouvre-t-on une plage de ports UDP (16384-16394) ?
4. Quel est l'avantage de l'installation native par rapport à Docker pour comprendre le système ?

---

## Partie 2 : Câblage du réseau VoIP

### 2.1 Schéma de câblage

Réaliser le câblage selon le schéma fourni :

```
                    IP Phone 0          IP Phone 1
                   192.169.0.3         192.169.0.4
                        |                   |
                        |                   |
                    +---+-------------------+---+
                    |                           |
                    |         Switch            |
                    |                           |
         +----------+--+-----+------+-----------+--------+
         |             |     |      |                    |
    Smartphone    WRT841N  RPI4   PC Windows        SPA112
      DHCP        Gateway  .0.2    .0.5             .0.6
    SSID:CEI1                                         |
    MDP:btsciellllb2a                       Alcatel 1 + Alcatel 2
```

### 2.2 Plan d'adressage IP

| Équipement | Interface | Adresse IP | Passerelle | Remarques |
|------------|-----------|------------|------------|-----------|
| Raspberry Pi 4 | eth0 | 192.169.0.2/24 | 192.169.0.1 | Serveur FusionPBX |
| IP Phone 0 | eth0 | 192.169.0.3/24 | 192.169.0.1 | Grandstream GXV3240 |
| IP Phone 1 | eth0 | 192.169.0.4/24 | 192.169.0.1 | Grandstream GXV3240 |
| PC Windows | eth0 | 192.169.0.5/24 | 192.169.0.1 | Administration |
| SPA112 | eth0 | 192.169.0.6/24 | 192.169.0.1 | Adaptateur analogique |
| Routeur TP-LINK | LAN | 192.169.0.1/24 | - | Passerelle/DHCP |
| Smartphone | wlan0 | DHCP | 192.169.0.1 | Linphone Android |

### 2.3 Instructions de câblage

1. **Connecter tous les équipements au switch** :
   - Raspberry Pi 4
   - IP Phone 0 et IP Phone 1
   - PC Windows
   - Adaptateur SPA112
   - Port LAN du routeur TP-LINK

2. **Connecter les téléphones analogiques** :
   - Téléphone Alcatel 1 → Port FXS 1 du SPA112
   - Téléphone Alcatel 2 → Port FXS 2 du SPA112

3. **Configurer le routeur TP-LINK** :
   - IP LAN : 192.169.0.1
   - Masque : 255.255.255.0
   - Serveur DHCP : Activé (plage 192.169.0.100-200)
   - SSID Wi-Fi : CEI1
   - Mot de passe : btsciellllb2a

**Questions de contrôle :**

1. Pourquoi utilise-t-on un adaptateur SPA112 ?
2. Quelle est la différence entre un téléphone IP et un téléphone analogique ?
3. Quel équipement fait office de passerelle par défaut ?

---

## Partie 3 : Configuration des terminaux VoIP

### 3.1 Création des extensions dans FusionPBX

**Accès à l'interface web**

1. Se connecter à FusionPBX : http://192.169.0.2
2. Menu : **Accounts** → **Extensions**

**Création des extensions**

Créer 5 extensions selon ce tableau :

| Extension | Nom d'affichage | Équipement | Mot de passe |
|-----------|-----------------|------------|--------------|
| 7950 | IP Phone 0 | Grandstream GXV3240 | ipsecure01 |
| 7951 | IP Phone 1 | Grandstream GXV3240 | ipsecure02 |
| 7952 | Analog Phone 0 | Alcatel via SPA112 Line 1 | anasecure01 |
| 7953 | Analog Phone 1 | Alcatel via SPA112 Line 2 | anasecure02 |
| 7954 | Smartphone | Linphone Android | mobilesecure |

**Paramètres pour chaque extension :**
- Cliquer sur **Add Extension**
- **Extension** : Numéro (ex: 7950)
- **Effective Caller ID Name** : Nom d'affichage
- **Effective Caller ID Number** : Numéro de l'extension
- **Password** : Mot de passe fort
- **Enabled** : True
- **Voicemail Enabled** : True
- Cliquer sur **Save**

### 3.2 Configuration des téléphones IP Grandstream GXV3240

**IP Phone 0 (192.169.0.3)**

1. Connecter le téléphone au switch et l'alimenter (PoE ou adaptateur)

2. Configuration IP statique :
   - Sur le téléphone : **Menu** → **Settings** → **Network Settings**
   - IPv4 Address Type : **Static IP**
   - Static IP : 192.169.0.3
   - Subnet Mask : 255.255.255.0
   - Default Gateway : 192.169.0.1
   - DNS Server : 8.8.8.8

3. Configuration du compte SIP :
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

Répéter la procédure avec :
- IP : 192.169.0.4
- Extension : 7951
- Mot de passe : ipsecure02

**Vérification de l'enregistrement**

Dans FusionPBX : **Status** → **Registrations**
- Les deux téléphones doivent apparaître comme "Registered"

### 3.3 Configuration de l'adaptateur SPA112

**Accès à l'interface web**

1. Depuis le PC Windows, accéder à : http://192.169.0.6
2. Cliquer sur **Admin Login** puis **Advanced**

**Configuration réseau**

- **Router** → **Network**
- Connection Type : Static IP
- Static IP : 192.169.0.6
- NetMask : 255.255.255.0
- Gateway : 192.169.0.1
- **Submit All Changes**

**Configuration Line 1 (Port FXS 1)**

- **Voice** → **Line 1**
- Line Enable : Yes
- SIP Port : 5060
- Proxy : 192.169.0.2
- Display Name : Analog Phone 0
- User ID : 7952
- Password : anasecure01
- **Submit All Changes**

**Configuration Line 2 (Port FXS 2)**

- **Voice** → **Line 2**
- Line Enable : Yes
- SIP Port : 5060
- Proxy : 192.169.0.2
- Display Name : Analog Phone 1
- User ID : 7953
- Password : anasecure02
- **Submit All Changes**

**Redémarrage**

- Cliquer sur **System** → **Reboot**

### 3.4 Installation et configuration de Linphone sur Android

**Installation**

1. Sur le smartphone, se connecter au Wi-Fi :
   - SSID : CEI1
   - Mot de passe : btsciellllb2a

2. Télécharger Linphone depuis Google Play Store

**Configuration du compte SIP**

1. Ouvrir Linphone → **Assistant**
2. Choisir **Use SIP account**
3. Paramètres :
   - Username : 7954
   - Password : mobilesecure
   - Domain : 192.169.0.2
   - Transport : UDP
4. **Login**

**Vérification**

- L'icône en haut doit afficher "Connected"
- Dans FusionPBX, vérifier que l'extension 7954 est enregistrée

**Questions de contrôle :**

1. Qu'est-ce qu'un codec audio ? Citez-en deux utilisés en VoIP.
2. Quelle est la fonction du protocole RTP ?
3. Comment vérifier qu'un téléphone est bien enregistré sur le serveur SIP ?

---

## Partie 4 : Tests de fonctionnement

### 4.1 Tests d'appels internes

**Tableau de tests à compléter :**

| Depuis | Vers | Sonnerie OK | Conversation OK | Qualité audio | Remarques |
|--------|------|-------------|-----------------|---------------|-----------|
| 7950 | 7951 | ☐ | ☐ | | |
| 7950 | 7952 | ☐ | ☐ | | |
| 7951 | 7953 | ☐ | ☐ | | |
| 7952 | 7950 | ☐ | ☐ | | |
| 7954 | 7951 | ☐ | ☐ | | |

### 4.2 Test de la messagerie vocale

1. Depuis FusionPBX : **Apps** → **Voicemail**
2. Appeler une extension, laisser sonner sans décrocher
3. Laisser un message après le bip
4. Depuis le téléphone destinataire, composer `*97`
5. Écouter le message

### 4.3 Capture de trafic SIP avec Wireshark (depuis le PC)

1. Installer Wireshark sur le PC Windows
2. Lancer une capture sur l'interface Ethernet
3. Appliquer le filtre : `sip or rtp`
4. Effectuer un appel entre deux extensions
5. Observer les messages SIP : INVITE → 100 Trying → 180 Ringing → 200 OK → ACK → BYE

**Questions d'analyse :**

1. Identifiez les adresses IP source et destination dans les paquets SIP.
2. Quel codec audio est négocié lors de l'établissement d'appel ?
3. Sur quels ports UDP circulent les flux RTP ?
4. Quelle est la différence entre SIP et RTP ?

---

## Partie 5 : Création d'une passerelle vers le réseau principal

### 5.1 Configuration du routeur TP-LINK en mode passerelle

**Accès à l'interface**

1. Depuis le PC, accéder à : http://192.169.0.1
2. Login : admin / admin

**Configuration WAN**

1. Menu : **Network** → **WAN**
2. WAN Connection Type : **Static IP**
3. Paramètres :
   - IP Address : 192.168.1.50
   - Subnet Mask : 255.255.255.0
   - Default Gateway : 192.168.1.1
   - DNS : 8.8.8.8
4. **Save**

**Vérification**

Depuis le PC Windows :
```cmd
ping 8.8.8.8
ping 192.168.1.1
```

### 5.2 Configuration NAT sur FusionPBX

1. Dans FusionPBX : **Advanced** → **SIP Profiles** → **Internal**
2. Éditer les paramètres NAT :
   - ext-rtp-ip : 192.168.1.50
   - ext-sip-ip : 192.168.1.50
3. **Save** et redémarrer FreeSWITCH

**Avec Docker :**
```bash
docker compose restart fusionpbx
```

**Avec installation native :**
```bash
sudo systemctl restart freeswitch
```

### 5.3 Trunk SIP vers un autre IPBX

1. **Apps** → **Gateways** → **Add**
2. Paramètres :
   - Gateway : Nom du trunk
   - Username : Identifiant fourni par l'autre IPBX
   - Password : Mot de passe
   - Proxy : IP de l'autre IPBX
3. Créer un **Outbound Route** pour router certains numéros vers ce trunk

**Questions de contrôle :**

1. Qu'est-ce que le NAT et pourquoi pose-t-il problème en VoIP ?
2. À quoi sert un trunk SIP ?
3. Expliquez la différence entre un appel interne et un appel via trunk.

---

## Partie 6 : Administration et dépannage

### 6.1 Consultation des logs

**Avec Docker :**
```bash
docker compose logs -f fusionpbx
docker compose logs -f postgres
```

**Avec installation native :**
```bash
tail -f /var/log/freeswitch/freeswitch.log
tail -f /var/log/nginx/error.log
journalctl -u freeswitch -f
```

### 6.2 Dépannage courant

**Problème : Extension non enregistrée**

1. Vérifier la configuration SIP sur le terminal
2. Vérifier l'extension dans FusionPBX : **Accounts** → **Extensions**
3. Tester la connectivité réseau : `ping 192.169.0.2`
4. Consulter les logs FreeSWITCH

**Problème : Pas de son lors d'un appel**

1. Vérifier que les ports RTP (16384-16394) ne sont pas bloqués
2. Vérifier la configuration des codecs
3. Désactiver temporairement le pare-feu

**Problème : Appels externes ne fonctionnent pas**

1. Vérifier la configuration NAT
2. Tester avec tcpdump :
   ```bash
   sudo tcpdump -i eth0 port 5060 -vvv
   ```

### 6.3 Sauvegarde de la configuration

**Avec Docker :**
```bash
cd ~/fusionpbx
docker compose exec postgres pg_dump -U fusionpbx fusionpbx > backup_$(date +%Y%m%d).sql
```

**Avec installation native :**
```bash
pg_dump -U fusionpbx fusionpbx > backup_$(date +%Y%m%d).sql
```

---

## Évaluation

### Critères d'évaluation (sur 20 points)

| Critère | Points | Détail |
|---------|--------|--------|
| **Installation serveur** | 4 | Debian installée, FusionPBX accessible |
| **Câblage réseau** | 2 | Câblage conforme, adressage IP correct |
| **Configuration extensions** | 4 | 5 extensions créées et fonctionnelles |
| **Tests d'appels** | 4 | Tous les appels internes fonctionnent |
| **Passerelle externe** | 3 | Routage configuré, test externe réussi |
| **Capture Wireshark** | 2 | Capture réalisée, questions répondues |
| **Qualité du compte-rendu** | 1 | Document structuré, copies d'écran |

### Livrables attendus

1. **Compte-rendu technique** (format PDF) incluant :
   - Copies d'écran de chaque étape
   - Tableau de tests complété
   - Capture Wireshark annotée
   - Réponses aux questions de contrôle

2. **Fichiers de configuration** :
   - `docker-compose.yml` (variante A)
   - Export des paramètres réseau

3. **Démonstration pratique** devant le formateur

---

## Ressources complémentaires

- FusionPBX : https://docs.fusionpbx.com/
- Script d'installation FusionPBX : https://github.com/fusionpbx/fusionpbx-install.sh
- Docker : https://docs.docker.com/
- FreeSWITCH : https://freeswitch.org/confluence/
- RFC 3261 (SIP) : https://www.rfc-editor.org/rfc/rfc3261
- RFC 3550 (RTP) : https://www.rfc-editor.org/rfc/rfc3550

---

## Consignes de sécurité

⚠️ **IMPORTANT**

- Ne jamais partager les mots de passe des comptes SIP sur Internet
- Utiliser des mots de passe forts (minimum 12 caractères)
- Isoler le réseau VoIP du réseau principal en production
- Mettre à jour régulièrement le système et FusionPBX
- Désactiver les comptes non utilisés

---

## Annexes

### Annexe A : Commandes Docker utiles

```bash
docker compose ps           # Voir les conteneurs actifs
docker compose logs -f      # Logs en temps réel
docker compose restart fusionpbx  # Redémarrer un service
docker compose down         # Arrêter tous les services
docker compose up -d        # Démarrer tous les services
docker compose exec fusionpbx /bin/bash  # Shell dans le conteneur
```

### Annexe B : Codecs audio VoIP courants

| Codec | Bande passante | Qualité | Utilisation |
|-------|---------------|---------|-------------|
| G.711 (PCMU/PCMA) | 64 kbit/s | Excellente | Réseau local |
| G.722 | 64 kbit/s | HD | VoIP haute qualité |
| G.729 | 8 kbit/s | Bonne | Lien WAN limité |
| Opus | Variable | Excellente | Standard moderne |

### Annexe C : Codes de réponse SIP

| Code | Signification |
|------|---------------|
| 100 | Trying |
| 180 | Ringing |
| 200 | OK |
| 401 | Unauthorized |
| 404 | Not Found |
| 486 | Busy Here |
| 603 | Decline |

---

**Version :** 1.1  
**Date :** Février 2025  
**Auteur :** Olivier - BTS CIEL
