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

## Partie 1 : Installation du serveur FusionPBX sur PC Ubuntu

### 1.1 Installation d'Ubuntu Server (sans interface graphique)

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
   - Configuration réseau : laisser en DHCP pour l'instant
   - Pas de proxy
   - Miroir : laisser par défaut
   - Partitionnement : utiliser le disque entier
   - Profil : définir nom d'utilisateur et mot de passe
   - **Activer OpenSSH server**
   - Pas de snaps supplémentaires
   - Lancer l'installation et redémarrer

**Configuration IP statique**

4. Se connecter en SSH depuis le PC Windows :
   ```bash
   ssh utilisateur@<ip_dhcp_du_serveur>
   ```

5. Configurer l'IP statique avec Netplan :
   ```bash
   sudo nano /etc/netplan/00-installer-config.yaml
   ```

   Modifier comme suit :
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

6. Appliquer la configuration :
   ```bash
   sudo netplan apply
   ```

7. Vérifier la connectivité :
   ```bash
   ping 8.8.8.8
   ```

**Mise à jour du système**

8. Mettre à jour :
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo reboot
   ```

---

### 1.2 Installation de FusionPBX

FusionPBX repose sur **FreeSWITCH** (moteur de téléphonie), **PostgreSQL** (base de données), **Nginx** (serveur web) et **PHP**. Le script officiel installe et configure tous ces composants automatiquement.

**Ressources pédagogiques :**
- FusionPBX : https://docs.fusionpbx.com/
- FreeSWITCH : https://freeswitch.org/
- Qu'est-ce qu'un IPBX ? https://fr.wikipedia.org/wiki/IP_PBX

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
   URL:      https://192.169.0.2
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
   - Ouvrir un navigateur : https://192.169.0.2
   - Accepter l'avertissement de certificat auto-signé
   - Se connecter avec les identifiants fournis

**Commandes d'administration utiles**

```bash
# Redémarrer FreeSWITCH
systemctl restart freeswitch

# Accéder à la console FreeSWITCH
fs_cli

# Voir les logs FreeSWITCH
tail -f /var/log/freeswitch/freeswitch.log

# Redémarrer Nginx
systemctl restart nginx

# Voir les logs Nginx
tail -f /var/log/nginx/error.log
```

**Questions de contrôle :**

1. Quel est le rôle de FreeSWITCH dans l'architecture FusionPBX ?
2. Quel port est utilisé par le protocole SIP ?
3. Pourquoi utilise-t-on une plage de ports UDP (16384-16394) ?
4. Quelle est la différence entre FusionPBX et FreeSWITCH ?

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
         +----------+--+-----+------+-----------+
         |             |     |      |
    Smartphone    WRT841N  PC      PC Windows
      DHCP        Gateway  Ubuntu   192.169.0.5
    SSID:CEI1     .0.1     .0.2
    MDP:btsciellllb2a
                              SPA112 (192.169.0.6)
                                |           |
                           Alcatel 1    Alcatel 2
```

### 2.2 Plan d'adressage IP

| Équipement | Interface | Adresse IP | Passerelle | Remarques |
|------------|-----------|------------|------------|-----------|
| PC Ubuntu | eth0 | 192.169.0.2/24 | 192.169.0.1 | Serveur FusionPBX |
| IP Phone 0 | eth0 | 192.169.0.3/24 | 192.169.0.1 | Grandstream GXV3240 |
| IP Phone 1 | eth0 | 192.169.0.4/24 | 192.169.0.1 | Grandstream GXV3240 |
| PC Windows | eth0 | 192.169.0.5/24 | 192.169.0.1 | Administration |
| SPA112 | eth0 | 192.169.0.6/24 | 192.169.0.1 | Adaptateur analogique |
| Routeur TP-LINK | LAN | 192.169.0.1/24 | - | Passerelle/DHCP |
| Smartphone | wlan0 | DHCP | 192.169.0.1 | Linphone Android |

### 2.3 Instructions de câblage

1. **Connecter tous les équipements au switch** :
   - PC Ubuntu (serveur FusionPBX)
   - IP Phone 0 et IP Phone 1
   - PC Windows
   - Adaptateur SPA112
   - Port LAN du routeur TP-LINK

2. **Connecter les téléphones analogiques** :
   - Téléphone Alcatel 1 → Port FXS 1 du SPA112
   - Téléphone Alcatel 2 → Port FXS 2 du SPA112

3. **Configurer le routeur TP-LINK** :
   - Accéder à http://192.169.0.1 (admin/admin)
   - IP LAN : 192.169.0.1 / 255.255.255.0
   - Serveur DHCP : Activé (plage 192.169.0.100-200)
   - SSID Wi-Fi : CEI1
   - Mot de passe Wi-Fi : btsciellllb2a

**Questions de contrôle :**

1. Pourquoi utilise-t-on un adaptateur SPA112 ?
2. Quelle est la différence entre un téléphone IP et un téléphone analogique ?
3. Quel équipement fait office de passerelle par défaut ?

---

## Partie 3 : Configuration des terminaux VoIP

### 3.1 Création des extensions dans FusionPBX

**Accès à l'interface web**

1. Depuis le PC Windows : https://192.169.0.2
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
- **Password** : Mot de passe
- **Enabled** : True
- **Voicemail Enabled** : True
- Cliquer sur **Save**

### 3.2 Configuration des téléphones IP Grandstream GXV3240

**IP Phone 0 (192.169.0.3)**

1. Connecter le téléphone au switch et l'alimenter

2. Configuration IP statique :
   - **Menu** → **Settings** → **Network Settings**
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

**Vérification**

Dans FusionPBX : **Status** → **Registrations**
- Les deux téléphones doivent apparaître comme **Registered**

### 3.3 Configuration de l'adaptateur SPA112

**Accès à l'interface web**

1. Depuis le PC Windows : http://192.169.0.6
2. **Admin Login** → **Advanced**

**Configuration réseau**

- **Router** → **Network**
- Connection Type : Static IP
- Static IP : 192.169.0.6
- NetMask : 255.255.255.0
- Gateway : 192.169.0.1
- **Submit All Changes**

**Configuration Line 1 (Alcatel 1)**

- **Voice** → **Line 1**
- Line Enable : Yes
- Proxy : 192.169.0.2
- Display Name : Analog Phone 0
- User ID : 7952
- Password : anasecure01
- **Submit All Changes**

**Configuration Line 2 (Alcatel 2)**

- **Voice** → **Line 2**
- Line Enable : Yes
- Proxy : 192.169.0.2
- Display Name : Analog Phone 1
- User ID : 7953
- Password : anasecure02
- **Submit All Changes**

- **System** → **Reboot**

### 3.4 Installation et configuration de Linphone sur Android

1. Connecter le smartphone au Wi-Fi CEI1 (MDP : btsciellllb2a)
2. Installer **Linphone** depuis Google Play Store
3. Ouvrir Linphone → **Assistant** → **Use SIP account**
4. Paramètres :
   - Username : 7954
   - Password : mobilesecure
   - Domain : 192.169.0.2
   - Transport : UDP
5. **Login**

Vérifier dans FusionPBX que l'extension 7954 est **Registered**.

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

1. Appeler une extension, laisser sonner sans décrocher
2. Laisser un message après le bip
3. Depuis le téléphone destinataire, composer `*97`
4. Écouter le message

### 4.3 Capture de trafic SIP avec Wireshark

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

1. Accéder à : http://192.169.0.1
2. Menu : **Network** → **WAN**
3. WAN Connection Type : **Static IP**
4. Paramètres :
   - IP Address : 192.168.1.50
   - Subnet Mask : 255.255.255.0
   - Default Gateway : 192.168.1.1
   - DNS : 8.8.8.8
5. **Save**

**Vérification depuis le PC Windows :**
```cmd
ping 8.8.8.8
ping 192.168.1.1
```

### 5.2 Configuration NAT sur FusionPBX

1. Dans FusionPBX : **Advanced** → **SIP Profiles** → **Internal**
2. Paramètres NAT :
   - ext-rtp-ip : 192.168.1.50
   - ext-sip-ip : 192.168.1.50
3. **Save** puis redémarrer FreeSWITCH :
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
3. Créer un **Outbound Route** pour router les numéros vers ce trunk

**Questions de contrôle :**

1. Qu'est-ce que le NAT et pourquoi pose-t-il problème en VoIP ?
2. À quoi sert un trunk SIP ?
3. Expliquez la différence entre un appel interne et un appel via trunk.

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
2. Tester la connectivité : `ping 192.169.0.2`
3. Consulter les logs : `tail -f /var/log/freeswitch/freeswitch.log`

**Pas de son lors d'un appel**
1. Vérifier que les ports RTP (16384-16394 UDP) ne sont pas bloqués
2. Vérifier la configuration des codecs dans FusionPBX
3. Vérifier la configuration NAT

**Analyser le trafic SIP sur le serveur**
```bash
sudo tcpdump -i eth0 port 5060 -vvv
# ou avec sngrep (plus lisible)
sudo apt install sngrep
sudo sngrep
```

### 6.3 Sauvegarde de la configuration

```bash
# Sauvegarde base de données
pg_dump -U fusionpbx fusionpbx > backup_fusionpbx_$(date +%Y%m%d).sql

# Sauvegarde configuration FusionPBX
tar -czf backup_config_$(date +%Y%m%d).tar.gz /etc/freeswitch /var/www/fusionpbx
```

---

## Évaluation

### Critères d'évaluation (sur 20 points)

| Critère | Points | Détail |
|---------|--------|--------|
| **Installation serveur** | 4 | Ubuntu installé, FusionPBX accessible |
| **Câblage réseau** | 2 | Câblage conforme, adressage IP correct |
| **Configuration extensions** | 4 | 5 extensions créées et fonctionnelles |
| **Tests d'appels** | 4 | Tous les appels internes fonctionnent |
| **Passerelle externe** | 3 | Routage configuré, test externe réussi |
| **Capture Wireshark** | 2 | Capture réalisée, questions répondues |
| **Qualité du compte-rendu** | 1 | Document structuré, copies d'écran |

### Livrables attendus

1. **Compte-rendu technique** (format PDF) :
   - Copies d'écran de chaque étape
   - Tableau de tests complété
   - Capture Wireshark annotée
   - Réponses aux questions de contrôle

2. **Fichiers de configuration** :
   - Export des paramètres réseau

3. **Démonstration pratique** devant le formateur :
   - Appel entre deux terminaux
   - Extensions enregistrées visibles dans FusionPBX
   - Message vocal laissé et écouté

---

## Ressources complémentaires

- FusionPBX Documentation : https://docs.fusionpbx.com/
- Script d'installation : https://github.com/fusionpbx/fusionpbx-install.sh
- FreeSWITCH : https://freeswitch.org/confluence/
- Linphone : https://www.linphone.org/
- RFC 3261 (SIP) : https://www.rfc-editor.org/rfc/rfc3261
- RFC 3550 (RTP) : https://www.rfc-editor.org/rfc/rfc3550

---

## Consignes de sécurité

⚠️ **IMPORTANT**

- Ne jamais exposer le serveur SIP directement sur Internet sans protection
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
# Lister les extensions enregistrées
sofia status profile internal reg

# Voir les appels en cours
show calls

# Recharger la configuration SIP
sofia profile internal rescan

# Voir l'état des profils SIP
sofia status
```

---

**Version :** 2.0
**Date :** Février 2026
**Auteur :** Olivier - BTS CIEL
