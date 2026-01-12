# TP3 - Installation de Linux sur PC

## 📋 Informations générales

**Type d'activité :** Installation  
**Durée :** 10 heures  
**Type d'évaluation :** Présentation "Client" et compte-rendu d'activité

---

## 🎯 Objectifs

À l'issue de ce TP, vous serez capable de :

- Installer Ubuntu 22.04 LTS sur un PC physique
- Créer et gérer des utilisateurs avec différents niveaux de privilèges
- Configurer un proxy réseau
- Installer et configurer une stack LAMP complète
- Mettre en place un serveur FTP avec gestion multi-utilisateurs
- Présenter professionnellement une installation à un client

---

## 🛠️ Matériel nécessaire

- **1 PC** (configuration minimale : 2 Go RAM, 25 Go disque)
- **1 clé USB** (minimum 4 Go pour l'image Ubuntu)
- **Connexion internet** (pour téléchargements et mises à jour)

---

## 📝 Tâches à effectuer

### Tâche 1 : Installation d'Ubuntu 22.04.3 LTS

#### Objectif
Installer Ubuntu 22.04.3 LTS avec deux utilisateurs :
- **Professeur** (administrateur) - Mot de passe : `LeProf`
- **Etudiant** (utilisateur standard) - Mot de passe : `llbajaccio`

#### Prérequis

**Télécharger Ubuntu :**
- Rendez-vous sur [ubuntu.com/download/desktop](https://ubuntu.com/download/desktop)
- Téléchargez **Ubuntu 22.04.3 LTS** (version Desktop)

**Créer la clé USB bootable :**
- Utilisez **Rufus** (Windows) ou **Balena Etcher** (multiplateforme)
- Suivez le [tutoriel officiel](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows) ou en français [Créer flasher une clé USB bootable](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)

#### Procédure d'installation

**Étape 1 : Démarrer sur la clé USB**

1. Insérez la clé USB sur le PC
2. Redémarrez le PC
3. Appuyez sur `F2`, `F12`, `Suppr` ou `Échap` (selon le PC) pour accéder au BIOS/UEFI
4. Sélectionnez la clé USB comme périphérique de démarrage
5. Choisissez "Try or Install Ubuntu"

**Étape 2 : Lancer l'installation**

1. Sélectionnez la langue : **Français**
2. Cliquez sur **"Installer Ubuntu"**
3. **Disposition du clavier** : Français (AZERTY)
4. **Mises à jour et logiciels** :
   - Cochez "Installation normale"
   - Cochez "Télécharger les mises à jour pendant l'installation"
   - Cochez "Installer des logiciels tiers" (pour les pilotes)

**Étape 3 : Partitionnement**

- **Option recommandée** : "Effacer le disque et installer Ubuntu"
- Ou configurez manuellement les partitions si vous savez ce que vous faites

**Étape 4 : Création du premier utilisateur (Administrateur)**

- **Votre nom** : Professeur
- **Nom de l'ordinateur** : ubuntu-tp3 (ou autre)
- **Nom d'utilisateur** : `professeur`
- **Mot de passe** : `LeProf`
- **Confirmer** : `LeProf`

**Étape 5 : Finalisation**

1. L'installation démarre (10-20 minutes)
2. Une fois terminé, cliquez sur **"Redémarrer maintenant"**
3. Retirez la clé USB quand demandé
4. Le PC redémarre sur Ubuntu

**Étape 6 : Premier démarrage**

1. Connectez-vous avec l'utilisateur **Professeur** / `LeProf`
2. Configurez les paramètres initiaux (compte en ligne, etc.) - vous pouvez passer
3. Effectuez les mises à jour :

```bash
sudo apt update
sudo apt upgrade -y
```

**Étape 7 : Création du deuxième utilisateur (Etudiant)**

Créez l'utilisateur non-administrateur :

```bash
# Créer l'utilisateur
sudo adduser etudiant
```

Quand demandé :
- **Mot de passe** : `llbajaccio`
- **Confirmer** : `llbajaccio`
- **Informations** : Appuyez sur Entrée pour chaque champ (optionnel)
- Confirmez avec `O` (Oui)

**Vérifier que l'utilisateur n'est PAS administrateur :**

```bash
# Lister les groupes de l'utilisateur
groups etudiant
```

L'utilisateur ne doit **PAS** apparaître dans le groupe `sudo`.

**Test des comptes :**

1. Déconnectez-vous (en haut à droite)
2. Connectez-vous avec **etudiant** / `llbajaccio`
3. Essayez une commande sudo (devrait échouer) :
```bash
sudo apt update
# Erreur attendue : "etudiant n'est pas dans le fichier sudoers"
```
4. Reconnectez-vous avec **Professeur**

**À documenter dans le compte-rendu :**
- Captures d'écran des étapes d'installation
- Preuve de création des deux utilisateurs
- Test de connexion pour chaque utilisateur

---

### Tâche 2 : Configuration du proxy

#### Configurer le proxy système

**Via l'interface graphique :**

1. Ouvrir **Paramètres** (Settings)
2. Aller dans **Réseau** (Network)
3. Cliquer sur **Proxy réseau** (Network Proxy)
4. Sélectionner **Manuel** (Manual)
5. Configurer :
   - **Proxy HTTP** : `proxy.lycee` (ou l'adresse fournie)
   - **Port** : `8080` (ou le port fourni)
   - Cocher "Utiliser ce proxy pour HTTPS"
6. Cliquer sur **Appliquer**

**Via la ligne de commande :**

Éditer le fichier d'environnement :

```bash
sudo nano /etc/environment
```

Ajouter ces lignes (adapter selon votre configuration) :

```bash
http_proxy="http://proxy.lycee:8080/"
https_proxy="http://proxy.lycee:8080/"
ftp_proxy="http://proxy.lycee:8080/"
no_proxy="localhost,127.0.0.1,::1"

HTTP_PROXY="http://proxy.lycee:8080/"
HTTPS_PROXY="http://proxy.lycee:8080/"
FTP_PROXY="http://proxy.lycee:8080/"
NO_PROXY="localhost,127.0.0.1,::1"
```

**Configurer le proxy pour APT :**

```bash
sudo nano /etc/apt/apt.conf.d/proxy.conf
```

Ajouter :

```
Acquire::http::Proxy "http://proxy.lycee:8080/";
Acquire::https::Proxy "http://proxy.lycee:8080/";
```

**Redémarrer pour appliquer :**

```bash
sudo reboot
```

**Tester la connexion :**

```bash
sudo apt update
ping -c 3 google.com
```

---

### Tâche 3 : Installation de Apache, PHP, MariaDB et phpMyAdmin

#### Utiliser le tutoriel LAMP

Pour cette tâche, suivez le tutoriel complet :

**📚 [Tutoriel Installation LAMP](https://github.com/oliv2a/guides-etudiants/blob/main/tuto-lamp-ubuntu.md)**

Ce tutoriel couvre :
- ✅ Installation d'Apache2
- ✅ Installation de PHP et modules
- ✅ Installation de MariaDB
- ✅ Création de base de données et utilisateurs
- ✅ Installation de phpMyAdmin
- ✅ Configuration de PHP
- ✅ (Optionnel) Configuration HTTPS

**Résumé des commandes principales :**

```bash
# Mise à jour
sudo apt update && sudo apt upgrade -y

# Installation Apache
sudo apt install -y apache2

# Installation PHP
sudo apt install -y php libapache2-mod-php php-mysql php-cli php-curl php-gd php-mbstring php-xml php-zip

# Installation MariaDB
sudo apt install -y mariadb-server
sudo mysql_secure_installation

# Installation phpMyAdmin
sudo apt install -y phpmyadmin

# Redémarrage des services
sudo systemctl restart apache2
sudo systemctl restart mariadb
```

**Tests à effectuer :**

1. **Test Apache** : `http://localhost/`
2. **Test PHP** : Créer `/var/www/html/info.php` avec `<?php phpinfo(); ?>`
3. **Test phpMyAdmin** : `http://localhost/phpmyadmin`
4. **Test base de données** : Créer une base et un utilisateur

**À documenter :**
- Captures d'écran de chaque service fonctionnel
- Preuve de création d'une base de données
- Connexion réussie à phpMyAdmin

---

### Tâche 4 : Installation de VSFTPD avec 9 utilisateurs + accès anonyme

#### Utiliser le tutoriel VSFTPD

Pour cette tâche, suivez le tutoriel complet :

**📚 [Tutoriel Installation VSFTPD](https://github.com/oliv2a/guides-etudiants/blob/main/tuto-vsftpd-linux.md)**

Ce tutoriel couvre :
- ✅ Installation de VSFTPD
- ✅ Configuration multi-utilisateurs (etudiant1 à etudiant9)
- ✅ Configuration de l'accès anonyme
- ✅ Sécurisation avec liste d'utilisateurs
- ✅ Tests de connexion

**Résumé de la configuration :**

```bash
# Installation
sudo apt install -y vsftpd

# Création des 9 utilisateurs (script automatisé)
for i in {1..9}; do
    sudo useradd -m -d /home/etudiant$i -s /bin/bash etudiant$i
    echo "etudiant$i:motdepasse$i" | sudo chpasswd
done

# Configuration dans /etc/vsftpd.conf
anonymous_enable=YES
local_enable=YES
write_enable=YES
chroot_local_user=YES
allow_writeable_chroot=YES
anon_root=/anonyme/
userlist_enable=YES
userlist_file=/etc/vsftpd.userlist
userlist_deny=NO

# Création du répertoire anonyme
sudo mkdir /anonyme
sudo chown nobody:nogroup /anonyme
sudo chmod 555 /anonyme

# Redémarrage
sudo systemctl restart vsftpd
```

**Tests à effectuer :**

1. **Connexion anonyme** :
```bash
ftp localhost
# User: anonymous / Pass: (vide)
```

2. **Connexion utilisateur** :
```bash
ftp localhost
# User: etudiant1 / Pass: motdepasse1
```

3. **Test depuis un autre PC** (avec FileZilla ou ligne de commande)

**À documenter :**
- Liste des 9 utilisateurs créés
- Configuration du fichier vsftpd.conf
- Captures de connexion FTP (anonyme et utilisateur)
- Test d'upload/download

---

### Tâche 5 : Préparer une démonstration "Client"

#### Objectif

Préparer une présentation professionnelle comme si vous présentiez l'installation à un client.

#### Contenu de la présentation

**1. Introduction (2 minutes)**
- Contexte du projet
- Besoins du client (serveur web + FTP)
- Technologies choisies et justifications

**2. Démonstration du système (5 minutes)**

**a) Système d'exploitation**
- Présentation d'Ubuntu 22.04 LTS
- Gestion des utilisateurs (Professeur administrateur, Etudiant standard)
- Connexion avec les deux comptes

**b) Serveur Web (Apache + PHP + MariaDB)**
- Accès à la page par défaut d'Apache
- Démonstration d'une page PHP fonctionnelle
- Accès à phpMyAdmin
- Création rapide d'une base de données en direct

**c) Serveur FTP (VSFTPD)**
- Connexion anonyme (lecture seule)
- Connexion avec un utilisateur (etudiant1)
- Upload d'un fichier
- Vérification depuis l'explorateur de fichiers

**3. Sécurité et bonnes pratiques (2 minutes)**
- Séparation des privilèges (admin vs utilisateur)
- Confinement FTP (chroot)
- Configuration du pare-feu (si applicable)
- Sauvegardes recommandées

**4. Maintenance et support (1 minute)**
- Mises à jour du système
- Surveillance des logs
- Documentation fournie

**5. Questions/Réponses**

#### Support de présentation

Créez un support visuel (PowerPoint, LibreOffice Impress, ou PDF) contenant :

- **Slide 1** : Titre, nom, date
- **Slide 2** : Sommaire
- **Slide 3-4** : Architecture technique (schéma)
- **Slide 5-8** : Captures d'écran des services
- **Slide 9** : Sécurité
- **Slide 10** : Conclusion et recommandations

#### Script de démonstration

Préparez un script détaillé de ce que vous allez dire et faire pendant la démo.

**Exemple :**

```
1. "Bonjour, je vais vous présenter l'installation du serveur Ubuntu..."
2. Afficher l'écran de connexion Ubuntu
3. "Deux utilisateurs ont été créés selon vos spécifications..."
4. Se connecter avec Professeur
5. "Voici l'interface du système..."
6. Ouvrir Firefox -> localhost
7. "Le serveur web Apache est opérationnel..."
etc.
```

---

## 📊 Compte-rendu d'activité

### Structure du compte-rendu

**1. Page de garde**
- Titre : Installation de Linux sur PC
- Nom, prénom, classe
- Date

**2. Sommaire**

**3. Introduction**
- Objectifs du TP
- Matériel utilisé
- Environnement de travail

**4. Partie technique**

**4.1 Installation d'Ubuntu 22.04**
- Préparation de la clé USB
- Étapes d'installation (avec captures)
- Création des utilisateurs
- Problèmes rencontrés et solutions

**4.2 Configuration du proxy**
- Méthode utilisée
- Fichiers modifiés
- Tests de fonctionnement

**4.3 Installation LAMP**
- Apache : version, configuration
- PHP : version, modules installés
- MariaDB : version, utilisateurs créés
- phpMyAdmin : configuration, accès
- Captures d'écran de chaque service

**4.4 Installation VSFTPD**
- Configuration choisie
- Création des utilisateurs
- Configuration de l'accès anonyme
- Tests de connexion
- Captures d'écran des tests

**5. Présentation client**
- Script de présentation
- Support visuel (annexé)
- Retours et améliorations

**6. Analyse et discussion**
- Difficultés rencontrées
- Solutions apportées
- Améliorations possibles
- Compétences acquises

**7. Conclusion**
- Objectifs atteints
- Bilan personnel

**8. Annexes**
- Fichiers de configuration
- Scripts utilisés
- Captures d'écran supplémentaires
- Support de présentation

---

## 🔧 Dépannage

### Problèmes d'installation Ubuntu

**Le PC ne démarre pas sur la clé USB**
- Vérifier que Secure Boot est désactivé dans le BIOS
- Essayer une autre clé USB
- Recréer la clé avec Rufus en mode "DD Image"

**Erreur de partitionnement**
- Sauvegarder vos données importantes avant !
- Utiliser l'option "Effacer le disque" si le PC est dédié à Ubuntu
- Consulter un enseignant en cas de doute

### Problèmes de proxy

**apt ne fonctionne pas après configuration proxy**

Vérifier la syntaxe dans `/etc/apt/apt.conf.d/proxy.conf` :
```bash
sudo nano /etc/apt/apt.conf.d/proxy.conf
```

Tester sans le proxy temporairement :
```bash
sudo apt -o Acquire::http::Proxy=false update
```

### Problèmes LAMP

**Apache ne démarre pas**
```bash
sudo apache2ctl configtest
sudo systemctl status apache2
```

**MariaDB refuse les connexions**
```bash
sudo systemctl restart mariadb
sudo mysql -u root -p
```

### Problèmes VSFTPD

**Utilisateurs ne peuvent pas se connecter**
- Vérifier `/etc/vsftpd.userlist`
- Vérifier les mots de passe : `sudo passwd etudiant1`
- Consulter les logs : `sudo tail -f /var/log/vsftpd.log`

---

## 📚 Ressources

### Tutoriels du dépôt guides-etudiants

- **[Installation LAMP complète](https://github.com/oliv2a/guides-etudiants/blob/main/tuto-lamp-ubuntu.md)**
- **[Installation VSFTPD complète](https://github.com/oliv2a/guides-etudiants/blob/main/tuto-vsftpd-linux.md)**

### Documentation officielle

- [Ubuntu Desktop](https://ubuntu.com/desktop)
- [Installation Ubuntu - Guide officiel](https://ubuntu.com/tutorials/install-ubuntu-desktop)
- [Documentation Apache](https://httpd.apache.org/docs/)
- [Documentation PHP](https://www.php.net/manual/fr/)
- [Documentation MariaDB](https://mariadb.com/kb/en/)
- [Documentation VSFTPD](https://security.appspot.com/vsftpd.html)

### Tutoriels vidéo

- [Installation Ubuntu 22.04 (YouTube)](https://www.youtube.com/watch?v=M9mKh1mdaiQ)
- [Configuration serveur LAMP (YouTube)](https://www.youtube.com/watch?v=l0Bl79rFQmo)
- [Configuration VSFTPD (YouTube)](https://www.youtube.com/watch?v=6KiMdLlH5iM)

### Sites francophones

- [Le Crabe Info - Guide Ubuntu](https://lecrabeinfo.net/installer-ubuntu-20-04-lts-le-guide-complet.html)
- [Ubuntu-fr.org - Documentation](https://doc.ubuntu-fr.org/)
- [Ubuntu-fr - LAMP](https://doc.ubuntu-fr.org/lamp)
- [Ubuntu-fr - VSFTPD](https://doc.ubuntu-fr.org/vsftpd)

---

## ✅ Checklist finale

Avant de rendre le TP, vérifiez que :

### Installation et configuration
- [ ] Ubuntu 22.04 LTS installé et fonctionnel
- [ ] Utilisateur Professeur (admin) créé avec mot de passe `LeProf`
- [ ] Utilisateur Etudiant (standard) créé avec mot de passe `llbajaccio`
- [ ] Proxy configuré et fonctionnel
- [ ] Apache installé et accessible
- [ ] PHP fonctionnel (test avec phpinfo())
- [ ] MariaDB installé et sécurisé
- [ ] phpMyAdmin accessible et opérationnel
- [ ] VSFTPD installé avec 9 utilisateurs (etudiant1-9)
- [ ] Accès FTP anonyme fonctionnel sur /anonyme/

### Tests effectués
- [ ] Connexion avec les deux comptes utilisateurs
- [ ] Accès aux pages web (Apache)
- [ ] Connexion à phpMyAdmin
- [ ] Création d'une base de données de test
- [ ] Connexion FTP anonyme
- [ ] Connexion FTP avec etudiant1
- [ ] Upload/download de fichiers via FTP

### Documentation
- [ ] Compte-rendu rédigé et complet
- [ ] Captures d'écran de toutes les installations
- [ ] Fichiers de configuration documentés
- [ ] Script de présentation préparé
- [ ] Support de présentation créé

### Présentation
- [ ] Démonstration testée et fonctionnelle
- [ ] Timing respecté (10 minutes max)
- [ ] Support visuel professionnel
- [ ] Réponses aux questions anticipées

---

**Bon courage pour ce TP d'installation système ! 🚀**
