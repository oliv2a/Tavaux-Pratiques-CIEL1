# TP - Mise en place d'une plateforme de téléphonie IP avec FreePBX

## Objectifs pédagogiques

- Configurer un serveur de téléphonie IP (IPBX) avec FreePBX
- Comprendre l'architecture d'un système de téléphonie sur IP
- Câbler et configurer un réseau VoIP complet
- Configurer différents types de terminaux (IP, analogiques, softphone)
- Mettre en place une passerelle SIP vers un réseau principal

## Prérequis

- Connaissances en réseaux informatiques (TCP/IP, routage, NAT)
- Bases Linux (ligne de commande, gestion de services)
- Notions de protocoles VoIP (SIP, RTP)

## Matériel nécessaire

- 1 PC Sangoma/FreePBX (préinstallé) → Serveur IPBX
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

> Cette étape permet de raccorder le réseau VoIP au réseau principal et de disposer d'un accès Internet pour les mises à jour.

### 1.1 Architecture cible

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

1. Connecter le **port WAN** du routeur TP-LINK au réseau principal
2. Connecter au **switch** :
   - PC FreePBX/Sangoma
   - PC Windows (administration)
   - Port LAN du routeur TP-LINK

### 1.3 Configuration du routeur TP-LINK

1. Connecter le PC Windows au switch
2. Accéder à l'interface du routeur : **http://192.168.0.1**
   (adresse par défaut, vérifier sous l'appareil)
3. Login : **admin / admin**

**Configuration WAN**

4. Menu : **Network** → **WAN**
5. WAN Connection Type : **DHCP** (ou Static IP selon le réseau principal)
6. Si Static IP :
   - IP Address : 192.168.1.50
   - Subnet Mask : 255.255.255.0
   - Default Gateway : 192.168.1.1
   - DNS : 8.8.8.8
7. **Save**

**Configuration LAN**

8. Menu : **Network** → **LAN**
   - IP Address : **192.169.0.1**
   - Subnet Mask : 255.255.255.0
9. **Save** (le routeur redémarre)

**Configuration DHCP**

10. Menu : **DHCP** → **DHCP Settings**
    - DHCP Server : **Enable**
    - Start IP : 192.169.0.100
    - End IP : 192.169.0.200
    - Default Gateway : 192.169.0.1
    - DNS : 8.8.8.8
11. **Save**

**Configuration Wi-Fi**

12. Menu : **Wireless** → **Basic Settings**
    - SSID : **CIEL1**
13. Menu : **Wireless** → **Wireless Security**
    - Mot de passe : **btsciellllb2a**
14. **Save**

**Vérification**

15. Depuis le PC Windows, tester l'accès Internet :
    ```cmd
    ping 8.8.8.8
    ping google.com
    ```

**Questions de contrôle :**

1. Quel est le rôle du port WAN du routeur ?
2. Quelle est la différence entre NAT et routage ?
3. Pourquoi le réseau VoIP est-il séparé du réseau principal ?

---

## Partie 2 : Configuration du réseau VoIP

### 2.1 Configuration IP statique du serveur FreePBX

1. Se connecter en SSH sur le serveur FreePBX depuis le PC Windows :
   ```cmd
   ssh root@<ip_actuelle_du_serveur>
   ```

2. Configurer l'IP statique :
   ```bash
   nmcli con show
   ```
   Noter le nom de la connexion (ex: `enp3s0` ou `eth0`)

3. Configurer l'IP statique :
   ```bash
   nmcli con mod "enp3s0" ipv4.addresses 192.169.0.2/24
   nmcli con mod "enp3s0" ipv4.gateway 192.169.0.1
   nmcli con mod "enp3s0" ipv4.dns 8.8.8.8
   nmcli con mod "enp3s0" ipv4.method manual
   nmcli con up "enp3s0"
   ```

4. Vérifier la nouvelle IP :
   ```bash
   ip a
   ping 192.169.0.1
   ```

5. Se reconnecter en SSH avec la nouvelle IP :
   ```cmd
   ssh root@192.169.0.2
   ```

### 2.2 Câblage complet du réseau VoIP

Compléter le câblage avec tous les équipements :

**Plan d'adressage IP**

| Équipement | Interface | Adresse IP | Passerelle | Remarques |
|------------|-----------|------------|------------|-----------|
| PC FreePBX | eth0 | 192.169.0.2/24 | 192.169.0.1 | Serveur IPBX |
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
   - Téléphone Alcatel 1 → Port **FXS 1** du SPA112
   - Téléphone Alcatel 2 → Port **FXS 2** du SPA112

3. Connecter le smartphone au Wi-Fi :
   - SSID : **CEI1**
   - Mot de passe : **btsciellllb2a**

**Questions de contrôle :**

1. Pourquoi utilise-t-on un adaptateur SPA112 ?
2. Quelle est la différence entre un téléphone IP et un téléphone analogique ?
3. Pourquoi attribue-t-on des IP statiques aux équipements VoIP ?

---

## Partie 3 : Configuration de FreePBX

### 3.1 Accès à l'interface web

1. Depuis le PC Windows, ouvrir un navigateur
2. Accéder à : **http://192.169.0.2**
3. Login : **admin**
4. Mot de passe : **laetitia**

### 3.2 Configuration SIP

1. Menu : **Admin** → **SIP Settings**
2. Onglet **General SIP Settings** :
   - Bind Port : **5060**
3. Onglet **Firewall / NAT Settings** :
   - External IP : laisser vide (réseau local)
   - Local Networks : **192.169.0.0/24**
4. **Save** puis **Apply Config**

### 3.3 Création des extensions

**Accès**

1. Menu : **Applications** → **Extensions**
2. Cliquer sur **Add Extension** → **Add New SIP [chan_pjsip] Extension**

**Créer 5 extensions :**

| Extension | Nom d'affichage | Équipement | Secret (mot de passe SIP) |
|-----------|-----------------|------------|--------------------------|
| 7950 | IP Phone 0 | Grandstream GXV3240 | ipsecure01 |
| 7951 | IP Phone 1 | Grandstream GXV3240 | ipsecure02 |
| 7952 | Analog Phone 0 | Alcatel via SPA112 Line 1 | anasecure01 |
| 7953 | Analog Phone 1 | Alcatel via SPA112 Line 2 | anasecure02 |
| 7954 | Smartphone | Linphone Android | mobilesecure |

**Paramètres pour chaque extension :**
- **User Extension** : Numéro (ex: 7950)
- **Display Name** : Nom d'affichage
- **Secret** : Mot de passe SIP
- **Voicemail** : Enabled
- **Voicemail Password** : même que l'extension (ex: 7950)
- Cliquer sur **Submit**

3. Après chaque création : cliquer sur **Apply Config** (bandeau orange en haut)

**Questions de contrôle :**

1. Qu'est-ce qu'une extension SIP ?
2. Quel est le rôle du "Secret" dans la configuration d'une extension ?
3. Quelle est la différence entre chan_sip et chan_pjsip ?

---

## Partie 4 : Configuration des terminaux VoIP

### 4.1 Configuration des téléphones IP Grandstream GXV3240

**IP Phone 0 (192.169.0.3)**

1. Connecter le téléphone au switch et l'alimenter

2. Configuration IP statique sur le téléphone :
   - **Menu** → **Settings** → **Network Settings**
   - IPv4 Address Type : **Static IP**
   - Static IP : **192.169.0.3**
   - Subnet Mask : 255.255.255.0
   - Default Gateway : 192.169.0.1
   - DNS : 8.8.8.8
   - Valider

3. Configuration du compte SIP :
   - **Menu** → **Settings** → **Accounts** → **Account 1**
   - Account Active : **Yes**
   - Account Name : IP Phone 0
   - SIP Server : **192.169.0.2**
   - SIP User ID : **7950**
   - Authenticate ID : **7950**
   - Authenticate Password : **ipsecure01**
   - Name : IP Phone 0
   - **Save and Apply**

4. Redémarrer le téléphone

**IP Phone 1 (192.169.0.4)**

Répéter la procédure avec :
- IP : 192.169.0.4
- SIP User ID : 7951
- Authenticate Password : ipsecure02

**Vérification**

Dans FreePBX : **Admin** → **Asterisk Logfiles** ou **Reports** → **Asterisk Logfiles**
- Les téléphones doivent apparaître comme enregistrés

### 4.2 Configuration de l'adaptateur SPA112

**Accès à l'interface web**

1. Depuis le PC Windows : **http://192.169.0.6**
2. Cliquer sur **Admin Login** → **Advanced**

**Configuration réseau**

3. Menu : **Router** → **Network**
   - Connection Type : **Static IP**
   - Static IP : **192.169.0.6**
   - NetMask : 255.255.255.0
   - Gateway : 192.169.0.1
4. **Submit All Changes**

**Configuration Line 1 (Alcatel 1)**

5. Menu : **Voice** → **Line 1**
   - Line Enable : **Yes**
   - SIP Port : 5060
   - Proxy : **192.169.0.2**
   - Display Name : Analog Phone 0
   - User ID : **7952**
   - Password : **anasecure01**
6. **Submit All Changes**

**Configuration Line 2 (Alcatel 2)**

7. Menu : **Voice** → **Line 2**
   - Line Enable : **Yes**
   - SIP Port : 5060
   - Proxy : **192.169.0.2**
   - Display Name : Analog Phone 1
   - User ID : **7953**
   - Password : **anasecure02**
8. **Submit All Changes**

9. **System** → **Reboot**

### 4.3 Installation et configuration de Linphone sur Android

1. Connecter le smartphone au Wi-Fi :
   - SSID : **CEI1**
   - Mot de passe : **btsciellllb2a**

2. Installer **Linphone** depuis Google Play Store

3. Ouvrir Linphone → **Assistant** → **Use SIP account**

4. Paramètres :
   - Username : **7954**
   - Password : **mobilesecure**
   - Domain : **192.169.0.2**
   - Transport : **UDP**

5. **Login**

**Vérification**

- L'icône en haut de Linphone doit afficher **Connected**
- Dans FreePBX : **Reports** → **Asterisk Logfiles**, vérifier l'enregistrement de l'extension 7954

**Questions de contrôle :**

1. Qu'est-ce qu'un codec audio ? Citez-en deux utilisés en VoIP.
2. Quelle est la fonction du protocole RTP ?
3. Comment vérifier qu'un téléphone est bien enregistré sur le serveur SIP ?

---

## Partie 5 : Tests de fonctionnement

### 5.1 Tests d'appels internes

Réaliser les appels suivants et compléter le tableau :

| Depuis | Vers | Sonnerie OK | Conversation OK | Qualité audio | Remarques |
|--------|------|-------------|-----------------|---------------|-----------|
| 7950 | 7951 | ☐ | ☐ | | |
| 7950 | 7952 | ☐ | ☐ | | |
| 7951 | 7953 | ☐ | ☐ | | |
| 7952 | 7950 | ☐ | ☐ | | |
| 7954 | 7951 | ☐ | ☐ | | |
| 7953 | 7954 | ☐ | ☐ | | |

### 5.2 Test de la messagerie vocale

1. Appeler une extension sans décrocher
2. Laisser un message après le bip
3. Depuis le téléphone destinataire, composer **`*97`**
4. Entrer le mot de passe de la messagerie (numéro de l'extension)
5. Écouter le message

### 5.3 Capture de trafic SIP avec Wireshark

1. Installer Wireshark sur le PC Windows : https://www.wireshark.org/
2. Lancer une capture sur l'interface Ethernet
3. Appliquer le filtre : `sip or rtp`
4. Effectuer un appel entre deux extensions
5. Observer les messages SIP :
   - **INVITE** → Demande d'appel
   - **100 Trying** → En cours de traitement
   - **180 Ringing** → Sonnerie
   - **200 OK** → Appel accepté
   - **ACK** → Confirmation
   - **BYE** → Fin d'appel

**Questions d'analyse :**

1. Identifiez les adresses IP source et destination dans les paquets SIP.
2. Quel codec audio est négocié lors de l'établissement d'appel ?
3. Sur quels ports UDP circulent les flux RTP ?
4. Quelle est la différence entre SIP et RTP ?

---

## Partie 6 : Administration et dépannage

### 6.1 Outils d'administration FreePBX

**Tableau de bord**
- **Admin** → **Dashboard** : vue d'ensemble du système

**Vérification des enregistrements SIP**
- **Reports** → **Asterisk Logfiles**
- Ou en ligne de commande :
  ```bash
  asterisk -rx "pjsip show registrations"
  asterisk -rx "pjsip show endpoints"
  ```

**Appels en cours**
```bash
asterisk -rx "core show channels"
```

**Logs en temps réel**
```bash
asterisk -rvvv
tail -f /var/log/asterisk/full
```

### 6.2 Dépannage courant

**Extension non enregistrée**
1. Vérifier la configuration SIP sur le terminal (IP serveur, login, mot de passe)
2. Tester la connectivité : `ping 192.169.0.2`
3. Vérifier l'extension dans FreePBX : **Applications** → **Extensions**
4. Consulter les logs : `asterisk -rvvv`

**Pas de son lors d'un appel**
1. Vérifier les codecs dans FreePBX : **Admin** → **SIP Settings** → **Codec Settings**
2. Vérifier que les ports RTP (10000-20000 UDP) ne sont pas bloqués
3. Vérifier la configuration NAT

**Analyser le trafic SIP sur le serveur**
```bash
# Installer sngrep
yum install sngrep   # sur Sangoma/CentOS
# ou
apt install sngrep   # sur Debian/Ubuntu

# Lancer sngrep
sngrep
```

### 6.3 Sauvegarde de la configuration

1. Dans FreePBX : **Admin** → **Backup & Restore**
2. Cliquer sur **Add Backup**
3. Configurer :
   - Backup Name : backup_voip
   - Items to backup : cocher tout
4. **Save** puis **Backup Now**

---

## Évaluation

### Critères d'évaluation (sur 20 points)

| Critère | Points | Détail |
|---------|--------|--------|
| **Raccordement réseau principal** | 2 | Accès Internet fonctionnel, routeur configuré |
| **Configuration réseau VoIP** | 2 | Câblage conforme, adressage IP correct |
| **Configuration extensions** | 4 | 5 extensions créées et fonctionnelles |
| **Configuration terminaux** | 3 | Téléphones IP, SPA112 et Linphone configurés |
| **Tests d'appels** | 4 | Tableau de tests complété, tous les appels fonctionnent |
| **Capture Wireshark** | 3 | Capture réalisée, questions d'analyse répondues |
| **Qualité du compte-rendu** | 2 | Document structuré, copies d'écran pertinentes |

### Livrables attendus

1. **Compte-rendu technique** (PDF) :
   - Copies d'écran de chaque étape de configuration
   - Tableau de tests complété
   - Capture Wireshark annotée
   - Réponses aux questions de contrôle

2. **Démonstration pratique** devant le formateur :
   - Appel entre deux terminaux au choix
   - Extensions enregistrées visibles dans FreePBX
   - Message vocal laissé et écouté

---

## Ressources complémentaires

- FreePBX Documentation : https://wiki.freepbx.org/
- Asterisk Documentation : https://docs.asterisk.org/
- Grandstream GXV3240 : https://www.grandstream.com/support
- Cisco SPA112 : https://www.cisco.com/c/en/us/support/unified-communications/spa112-2-port-phone-adapter/
- Linphone : https://www.linphone.org/
- RFC 3261 (SIP) : https://www.rfc-editor.org/rfc/rfc3261
- RFC 3550 (RTP) : https://www.rfc-editor.org/rfc/rfc3550

---

## Consignes de sécurité

⚠️ **IMPORTANT**

- Ne jamais exposer le serveur SIP directement sur Internet sans protection
- Utiliser des mots de passe forts pour les extensions SIP (minimum 12 caractères)
- Mettre à jour régulièrement FreePBX : **Admin** → **Module Admin** → **Check Online**
- Désactiver les extensions non utilisées
- Surveiller les logs pour détecter les tentatives d'intrusion SIP

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

### Annexe C : Commandes Asterisk utiles

```bash
# Accéder à la console Asterisk
asterisk -rvvv

# Lister les extensions enregistrées
pjsip show registrations

# Voir les appels en cours
core show channels

# Recharger la configuration
core reload

# Quitter la console
exit
```

---

**Version :** 4.0
**Date :** Février 2026
**Auteur :** Olivier - BTS CIEL
