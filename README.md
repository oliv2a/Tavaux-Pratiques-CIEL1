# 🎓 Travaux Pratiques - BTS CIEL 1

Bienvenue dans le dépôt des travaux pratiques du BTS CIEL première année. Ce dépôt contient l'ensemble des TPs organisés par thématique.

---

## 📋 Liste des Travaux Pratiques

### Raspberry Pi & Systèmes Embarqués

| TP | Titre | Thème | Durée estimée |
|----|-------|-------|---------------|
| [TP1](TP1-Temperature-Raspberry/) | Capteur de température et humidité connecté | Capteur BME680, I2C, BDD, Web | 10h |
| [TP2](TP2-Vitesse-Vent-Raspberry/) | Mesure de vitesse du vent avec interruption | Anémomètre, GPIO, Interruptions | 10h |
| [TP10](TP2-SMS_avec_le_Raspberry/) | Module GSM SIM800C et contrôle d'arrosage par SMS | Emission & réception de SMS, programmes python, application Androïd | 10h |

### Développement & Programmation

| TP | Titre | Thème | Durée estimée |
|----|-------|-------|---------------|
| À venir | - | - | - |

### Réseaux & Communication

| TP | Titre | Thème | Durée estimée |
|----|-------|-------|---------------|
| [TP5](TP5-Capteur-de-temperature-sans-fils-Xbee/) | Capteur de température avec liaison sans fil XBee | UART, I2C, XBee, Communication série | 10h |

### Systèmes & Infrastructure

| TP | Titre | Thème | Durée estimée |
|----|-------|-------|---------------|
| [TP3](TP3-Installation-de-Linux/) | Installation de Linux sur PC | Ubuntu, LAMP, VSFTPD, Multi-utilisateurs | 10h |

### Domotique & IoT

| TP | Titre | Thème | Durée estimée |
|----|-------|-------|---------------|
| [TP4](TP4-Installation-centrale-Domotique/) | Installation centrale domotique Z-Wave | Eedomus, Capteurs, Automatisation, Sécurité | 10h |

### Électronique & Instrumentation

| TP | Titre | Thème | Durée estimée |
|----|-------|-------|---------------|
| [TP6](TP6-Soudage-kit/) | Soudage et vérification d'un kit électronique | Soudage THT, Multimètre, Oscilloscope | 10h |

## 📁 Structure d'un TP

Chaque TP suit la même organisation :

```
TPX-Nom-Du-TP/
├── README.md          # Énoncé et instructions du TP
├── Fichiers/          # Fichiers de départ, templates, code source
├── Documents/         # Documentation, PDF, schémas
└── Correction/        # Solutions et corrigés (accès enseignant)
```

---

## 🎯 Objectifs pédagogiques

Les travaux pratiques de ce dépôt permettent de développer les compétences suivantes :

- **Systèmes embarqués** : Configuration et administration de Raspberry Pi
- **Développement web** : Mise en place de serveurs web (Apache, PHP, MySQL)
- **Automatisation** : Planification de tâches avec Cron
- **Programmation** : Python, Shell scripting
- **Documentation** : Rédaction technique, utilisation de Git/GitHub

---

## 📚 Prérequis

### Matériel
- Raspberry Pi (version 3 ou supérieure recommandée)
- Carte SD (minimum 16 Go)
- Alimentation 5V
- Connexion réseau (Ethernet ou WiFi)
- Analog Discovery 2 (ou 3)

### Logiciels
- Raspberry Pi OS (anciennement Raspbian)
- Connexion SSH configurée
- Éditeur de texte (nano, vim, ou VSCode avec Remote SSH)
- Visual Studio Code
- Waveform

### Connaissances
- Bases de Linux/terminal
- Notions de réseau
- Bases de programmation (Python recommandé)

---

## 🚀 Comment utiliser ce dépôt

### Pour les étudiants

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/oliv2a/Travaux-Pratiques-CIEL1.git
   cd Travaux-Pratiques-CIEL1
   ```

2. **Accéder à un TP** :
   ```bash
   cd TP1-Services-Web-Raspberry
   ```

3. **Lire le README** du TP pour suivre les instructions

4. **Utiliser les fichiers fournis** dans le dossier `Fichiers/`

5. **Consulter la documentation** dans le dossier `Documents/` si nécessaire

### Pour mettre à jour le dépôt

```bash
git pull origin main
```

---

## 📖 Ressources complémentaires

### Documentation officielle
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [Documentation Apache](https://httpd.apache.org/docs/)
- [Documentation PHP](https://www.php.net/manual/fr/)
- [Documentation MySQL](https://dev.mysql.com/doc/)

### Tutoriels
- [Guides GitHub pour étudiants](https://github.com/oliv2a/guides-etudiants)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

### Outils utiles
- [Raspberry Pi Imager](https://www.raspberrypi.org/software/) - Pour installer l'OS
- [PuTTY](https://www.putty.org/) - Client SSH pour Windows
- [WinSCP](https://winscp.net/) - Transfert de fichiers SFTP

---

## 💡 Conseils pour réussir les TPs

✅ **Lisez entièrement le TP** avant de commencer  
✅ **Suivez les étapes dans l'ordre** indiqué  
✅ **Testez régulièrement** votre travail  
✅ **Prenez des notes** sur les commandes utilisées  
✅ **Sauvegardez votre travail** régulièrement  
✅ **N'hésitez pas à expérimenter** une fois le TP terminé  
✅ **Consultez la correction** uniquement après avoir tenté le TP  

---

## 🆘 Besoin d'aide ?

Si vous rencontrez des difficultés :

1. **Relisez attentivement** les instructions du TP
2. **Vérifiez** que vous avez bien suivi toutes les étapes
3. **Consultez** la section "Dépannage" si elle existe
4. **Recherchez** l'erreur sur internet (très formateur !)
5. **Demandez de l'aide** à vos camarades ou à votre enseignant

---

## 📝 Évaluation

Certains TPs peuvent faire l'objet d'une évaluation. Les critères d'évaluation seront précisés dans chaque TP concerné.

**Critères généraux :**
- Respect des consignes
- Qualité du travail réalisé
- Compréhension des concepts
- Capacité à résoudre les problèmes
- Documentation du travail effectué

---

## 👨‍🏫 À propos

**Établissement** : BTS CIEL - Lycée Laetitia Bonaparte  
**Année** : 2025-2026  
**Enseignant** : [Olivier WAILLY]

---

## 📜 Licence

Ce contenu pédagogique est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le partager à des fins éducatives.

---

**Bon courage et bon apprentissage ! 🚀**
