# TP4 - Installation d'une Centrale Domotique sans fil au protocole Z-Wave

## 📋 Informations générales

**Type d'activité :** Installation  
**Durée :** 10 heures  
**Type d'évaluation :** Présentation "Client" et compte-rendu d'activité

---

## 🎯 Objectifs

À l'issue de ce TP, vous serez capable de :

- Configurer une centrale domotique Eedomus+
- Ajouter et paramétrer des périphériques Z-Wave
- Créer des scènes domotiques automatisées
- Configurer un système d'alarme avec notifications
- Intégrer des capteurs filaires et sans fil
- Présenter une installation domotique à un client

---

## 🛠️ Matériel nécessaire

### Centrale domotique
- **1 Eedomus+** (box domotique Z-Wave)

### Périphériques d'éclairage
- **2 lampes LED Bulb 6** (Aeotec) - Ampoules connectées RGB Z-Wave

### Capteurs multi-fonctions
- **2 Multisensor 7** (Aeotec) - Capteurs 6-en-1 : température, humidité, luminosité, UV, mouvement, vibration

### Capteurs d'intrusion
- **1 capteur ZD206EU** - Capteur d'ouverture de porte/fenêtre sans fil Z-Wave (Raylios)
- **4 capteurs d'intrusion filaire** - Contacts magnétiques câblés
- **1 Everspring ST814-1** - Capteur de température et humidité Z-Wave

---

## 📡 Informations de connexion

**Plateforme Eedomus :**
- **URL** : [https://secure.eedomus.com/](https://secure.eedomus.com/)
- **Utilisateur** : `olivier.wailly@yahoo.fr`
- **Mot de passe** : `btsciel1llb`

⚠️ **Important** : Ces identifiants sont partagés. Nommez clairement vos périphériques pour les identifier.

---

## 📝 Tâches à effectuer

### Tâche 1 : Connexion à la plateforme Eedomus

#### Se connecter à l'interface web

1. Ouvrez un navigateur web
2. Accédez à : [https://secure.eedomus.com/](https://secure.eedomus.com/)
3. Entrez les identifiants :
   - **Email** : `olivier.wailly@yahoo.fr`
   - **Mot de passe** : `btsciel1llb`
4. Cliquez sur **"Se connecter"**

#### Interface principale

Vous arrivez sur le **tableau de bord** de votre box Eedomus. Familiarisez-vous avec :
- **Configuration** : Gestion des périphériques
- **Scènes** : Automatisations
- **Règles** : Programmations avancées
- **Graphiques** : Historique des capteurs
- **Store** : Ajout de périphériques

**À documenter :**
- Capture d'écran du tableau de bord
- Liste des périphériques déjà présents (si applicable)

---

### Tâche 2 : Consulter le site d'aide en ligne

#### Documentation Eedomus

Parcourez la documentation officielle :

**🔗 [Aide Eedomus en ligne](https://secure.eedomus.com/help/)**

**Sections importantes à consulter :**
- Guide de démarrage
- Ajout de périphériques Z-Wave
- Création de scènes
- Configuration des alertes
- API et intégrations

**À documenter :**
- Notes sur les fonctionnalités découvertes
- Questions éventuelles

---

### Tâche 3 : Prendre connaissance de la documentation

#### Documentation des fabricants

Consultez les ressources suivantes :

**Aeotec (LED Bulb 6 et Multisensor 7) :**
- **🔗 [Site officiel Aeotec](https://aeotec.com/)**
- Recherchez les manuels de vos périphériques

**Capteur ZD206EU (Raylios) :**
- **🔗 [Manuel ZD206EU](https://fr.manuals.plus/raylios/raylios-door-sensor-zd2102eu-5-manual#quickstart)**

**Capteur ST814 (Everspring) :**
- **🔗 [Configuration ST814](https://e-domotic.fr/blog/z-wave/capteurs-zwave/capteur-temperatureeverspring-st814/configuration-du-capteur-temperature-et-humidite-everspring-st814/)**

**À documenter :**
- Caractéristiques techniques de chaque périphérique
- Spécificités du protocole Z-Wave
- Portée et limitations

---

### Tâche 4 : Vérifier la configuration du proxy

Si vous êtes dans un environnement avec proxy (lycée), vous devez le configurer.

#### Vérifier la configuration réseau de la box

1. Dans l'interface Eedomus, allez dans **Configuration** > **Ma box**
2. Vérifiez la section **Réseau**
3. Si nécessaire, configurez :
   - **Proxy HTTP** : `proxy.lycee:8080` (adapter selon votre réseau)
   - **Port** : `8080`

#### Test de connectivité

Vérifiez que la box peut accéder à internet :
- Allez dans **Configuration** > **Ma box**
- Section **État de la box**
- Vérifiez **"Connexion Internet"** : doit être ✅

**En cas de problème :**
- Contactez l'administrateur réseau
- Vérifiez les paramètres proxy
- Redémarrez la box si nécessaire

---

### Tâche 5 : Ajouter les 2 lampes LED Bulb 6

#### Spécifications des LED Bulb 6

- **Fabricant** : Aeotec
- **Type** : Ampoule RGB Z-Wave
- **Puissance** : 6W
- **Culot** : E27
- **Couleurs** : 16 millions (RGB + blanc froid/chaud)
- **Protocole** : Z-Wave Plus

#### Procédure d'ajout

**Étape 1 : Activer le mode inclusion**

1. Dans l'interface Eedomus, allez dans **Configuration** > **Ajouter ou supprimer un périphérique**
2. Cliquez sur **"Ajouter un périphérique"**
3. La box passe en mode inclusion (30 secondes)

**Étape 2 : Appairer la première lampe**

1. Vissez la lampe LED Bulb 6 dans une douille alimentée
2. **Méthode d'inclusion** (selon le modèle) :
   - Allumer/éteindre rapidement 6 fois
   - Ou maintenir un bouton physique (si présent)
3. La lampe clignote pour confirmer l'appairage
4. Attendez que Eedomus détecte le périphérique

**Étape 3 : Nommer le périphérique**

1. Une fois détecté, cliquez sur le périphérique
2. **Nom** : `Lampe 1`
3. **Pièce** : Choisissez une pièce (ex : "Salon", "Bureau")
4. Cliquez sur **"Enregistrer"**

**Étape 4 : Répéter pour la deuxième lampe**

1. Répétez les étapes 1 à 3
2. Nommez la seconde lampe : `Lampe 2`

**Étape 5 : Tester les lampes**

Dans le tableau de bord :
1. Cliquez sur **Lampe 1** puis **"Allumer"**
2. Testez les couleurs : Rouge, Vert, Bleu, Blanc
3. Testez la variation d'intensité
4. Répétez pour **Lampe 2**

**À documenter :**
- Captures d'écran de l'ajout des périphériques
- Tests de fonctionnement (photos des lampes allumées en différentes couleurs)

---

### Tâche 6 : Ajouter les 2 Multisensor 7

#### Spécifications du Multisensor 7

- **Fabricant** : Aeotec
- **Type** : Capteur 6-en-1 Z-Wave Plus
- **Mesures** :
  - Température
  - Humidité relative
  - Luminosité (lux)
  - Rayonnement UV
  - Détection de mouvement (PIR)
  - Détection de vibrations (accéléromètre)
- **Alimentation** : Piles ou USB
- **Portée Z-Wave** : ~100m en champ libre

#### Procédure d'ajout

**Étape 1 : Préparer le premier capteur**

1. Insérez les piles (ou connectez l'USB)
2. Localisez le bouton d'appairage (généralement à l'arrière)

**Étape 2 : Activer le mode inclusion**

1. Dans Eedomus : **Configuration** > **Ajouter ou supprimer un périphérique**
2. Cliquez sur **"Ajouter un périphérique"**

**Étape 3 : Appairer le capteur**

1. Appuyez **1 fois** sur le bouton du Multisensor 7
2. Une LED clignote (orange/vert)
3. Attendez la détection par Eedomus (15-30 secondes)

**Étape 4 : Configurer le premier capteur**

1. Une fois détecté, nommez-le : `Intérieur P18`
2. **Pièce** : "Salle P18" ou similaire
3. **Icône** : Choisissez une icône appropriée
4. Cliquez sur **"Enregistrer"**

**Étape 5 : Vérifier les valeurs**

Le Multisensor 7 crée **plusieurs périphériques** dans Eedomus :
- Température
- Humidité
- Luminosité
- UV
- Mouvement
- Vibration

Vérifiez que toutes les valeurs apparaissent.

**Étape 6 : Répéter pour le deuxième capteur**

1. Répétez les étapes 1 à 5
2. Nommez-le : `Extérieur P18`

**Étape 7 : Tester les capteurs**

1. Vérifiez les températures affichées
2. Passez la main devant les capteurs (détection de mouvement)
3. Tapez légèrement sur les capteurs (détection de vibration)
4. Consultez les graphiques d'historique

**À documenter :**
- Liste des valeurs mesurées par chaque capteur
- Captures d'écran des mesures
- Graphiques d'évolution de la température

---

### Tâche 7 : Configurer une scène de gestion de température

#### Objectif

Créer une scène qui change automatiquement la couleur des lampes en fonction de la température :
- 🔵 **Bleu** : Température < 19°C
- 🟢 **Vert** : Température entre 19°C et 22°C
- 🔴 **Rouge** : Température > 22°C

#### Procédure

**Étape 1 : Créer la première règle (Température < 19°C)**

1. Allez dans **Scènes** > **Ajouter une scène**
2. **Nom** : `Température Froide - Bleu`
3. **Condition** :
   - **SI** : Température du capteur `Intérieur P18` **< 19°C**
4. **Action** :
   - **Lampe 1** : Allumer en **Bleu** (RGB: 0, 0, 255)
   - **Lampe 2** : Allumer en **Bleu**
5. Cliquez sur **"Enregistrer"**

**Étape 2 : Créer la deuxième règle (19°C ≤ Température ≤ 22°C)**

1. **Scènes** > **Ajouter une scène**
2. **Nom** : `Température Normale - Vert`
3. **Condition** :
   - **SI** : Température `Intérieur P18` **≥ 19°C**
   - **ET** : Température `Intérieur P18` **≤ 22°C**
4. **Action** :
   - **Lampe 1** : Allumer en **Vert** (RGB: 0, 255, 0)
   - **Lampe 2** : Allumer en **Vert**
5. **Enregistrer**

**Étape 3 : Créer la troisième règle (Température > 22°C)**

1. **Scènes** > **Ajouter une scène**
2. **Nom** : `Température Chaude - Rouge`
3. **Condition** :
   - **SI** : Température `Intérieur P18` **> 22°C**
4. **Action** :
   - **Lampe 1** : Allumer en **Rouge** (RGB: 255, 0, 0)
   - **Lampe 2** : Allumer en **Rouge**
5. **Enregistrer**

**Étape 4 : Tester le système**

**Test 1 : Simulation de froid**
- Placez le capteur près d'une source froide (fenêtre ouverte, glaçons dans un sac)
- Attendez que la température descende sous 19°C
- Vérifiez que les lampes passent au **bleu**

**Test 2 : Température normale**
- Laissez le capteur à température ambiante (19-22°C)
- Les lampes doivent être **vertes**

**Test 3 : Simulation de chaleur**
- Placez le capteur près d'une source chaude (radiateur, lampe, main)
- Attendez que la température dépasse 22°C
- Vérifiez que les lampes passent au **rouge**

**À documenter :**
- Captures d'écran des 3 scènes configurées
- Photos des tests avec les différentes couleurs
- Tableau de correspondance température/couleur observée

---

### Tâche 8 : Ajouter le capteur d'ouverture ZD206EU

#### Spécifications du ZD206EU

- **Fabricant** : Raylios
- **Type** : Capteur d'ouverture de porte/fenêtre Z-Wave
- **Composants** : 2 parties (aimant + capteur)
- **Portée** : ~30m en intérieur
- **Alimentation** : 1 pile CR2032

#### Procédure d'ajout

**Étape 1 : Préparer le capteur**

1. Insérez la pile CR2032
2. Vérifiez que le capteur s'allume (LED)

**Étape 2 : Activer le mode inclusion**

1. Eedomus : **Configuration** > **Ajouter un périphérique**
2. La box passe en mode inclusion

**Étape 3 : Appairer le capteur**

1. Appuyez **3 fois rapidement** sur le bouton du capteur (ou selon la documentation)
2. Une LED clignote
3. Attendez la détection

**Étape 4 : Configurer le capteur**

1. **Nom** : `Capteur Porte P18` (ou selon votre utilisation)
2. **Pièce** : "Entrée", "Salle P18", etc.
3. **Type** : Détecteur d'ouverture
4. **Enregistrer**

**Étape 5 : Installation physique**

1. **Partie avec électronique** : Sur le cadre de porte (partie fixe)
2. **Aimant** : Sur la porte (partie mobile)
3. **Distance maximale** : 10-15 mm entre les deux parties
4. Fixation : Adhésif double-face ou vis

**Étape 6 : Tester le capteur**

1. Fermez la porte : état = **"Fermé"** dans Eedomus
2. Ouvrez la porte : état = **"Ouvert"**
3. Vérifiez les notifications dans le tableau de bord

**À documenter :**
- Photo du capteur installé
- Distance entre capteur et aimant
- Tests d'ouverture/fermeture

---

### Tâche 9 : Configurer l'alarme d'intrusion avec notification SMS

#### Objectif

Quand le capteur ZD206EU détecte une ouverture :
- Les lampes clignotent en **rouge**
- Un **SMS** est envoyé sur votre téléphone

#### Prérequis

**Configurer l'envoi de SMS :**

1. Allez dans **Configuration** > **Ma box** > **SMS**
2. Achetez des crédits SMS si nécessaire (ou utilisez les crédits gratuits)
3. Enregistrez votre **numéro de téléphone**

#### Procédure

**Étape 1 : Créer la scène d'alarme**

1. **Scènes** > **Ajouter une scène**
2. **Nom** : `Alarme Intrusion - Porte`
3. **Condition** :
   - **SI** : `Capteur Porte P18` passe à **"Ouvert"**
4. **Actions** :

   **Action 1 : Clignotement rouge**
   - Créer une boucle de clignotements :
     - **Lampe 1** : Allumer en **Rouge** (100%)
     - **Lampe 2** : Allumer en **Rouge** (100%)
     - **Attendre** : 0,5 seconde
     - **Lampe 1** : Éteindre
     - **Lampe 2** : Éteindre
     - **Attendre** : 0,5 seconde
     - **Répéter** : 10 fois

   **Action 2 : Envoi SMS**
   - **Type d'action** : Envoyer un SMS
   - **Numéro** : Votre numéro de téléphone
   - **Message** : `🚨 ALERTE : Intrusion détectée - Porte P18 ouverte !`

5. **Enregistrer**

**Étape 2 : Tester l'alarme**

1. Ouvrez la porte (ou activez le capteur)
2. Vérifiez :
   - ✅ Les lampes clignotent en rouge
   - ✅ Vous recevez le SMS sur votre téléphone

**Étape 3 : Ajouter une désactivation**

Créez une scène pour arrêter l'alarme quand la porte se referme :

1. **Scènes** > **Ajouter une scène**
2. **Nom** : `Arrêt Alarme - Porte Fermée`
3. **Condition** :
   - **SI** : `Capteur Porte P18` passe à **"Fermé"**
4. **Actions** :
   - **Lampe 1** : Éteindre
   - **Lampe 2** : Éteindre
5. **Enregistrer**

**À documenter :**
- Capture d'écran de la scène d'alarme
- Photo du SMS reçu
- Vidéo du clignotement des lampes (si possible)

---

### Tâche 10 : Configurer le capteur de vibration (alarme intrusion)

#### Objectif

Utiliser le **Multisensor 7 Intérieur P18** en mode détection de vibration pour déclencher une alarme d'intrusion.

#### Procédure

**Étape 1 : Activer la détection de vibration**

1. Allez dans **Configuration** > **Périphériques**
2. Sélectionnez **Multisensor 7 Intérieur P18**
3. Cherchez le paramètre **"Vibration"** ou **"Tamper"**
4. **Activez** la détection de vibration
5. Réglez la **sensibilité** (faible, moyenne, élevée)

**Étape 2 : Créer la scène d'alarme vibration**

1. **Scènes** > **Ajouter une scène**
2. **Nom** : `Alarme Intrusion - Vibration P18`
3. **Condition** :
   - **SI** : Vibration détectée sur `Multisensor 7 Intérieur P18`
4. **Actions** :
   - **Lampe 1** : Clignoter en **Rouge**
   - **Lampe 2** : Clignoter en **Rouge**
   - **Notification** : Envoyer SMS `🚨 Vibration détectée - Intrusion possible !`
   - (Optionnel) **Sirène** : Déclencher une sirène Z-Wave si disponible
5. **Enregistrer**

**Étape 3 : Tester la détection**

1. Tapez légèrement sur le Multisensor 7
2. Vérifiez le déclenchement de l'alarme
3. Ajustez la sensibilité si nécessaire

**À documenter :**
- Configuration de la sensibilité choisie
- Tests de déclenchement
- Faux positifs éventuels

---

### Tâche 11 : Ajouter le capteur Everspring ST814-1

#### Spécifications du ST814-1

- **Fabricant** : Everspring
- **Type** : Capteur de température et humidité Z-Wave
- **Plage température** : -20°C à +60°C
- **Plage humidité** : 0% à 100%
- **Alimentation** : 2 piles AAA

#### Procédure d'ajout

**Étape 1 : Préparer le capteur**

1. Insérez les 2 piles AAA
2. Vérifiez que le capteur s'allume

**Étape 2 : Activer le mode inclusion**

1. Eedomus : **Configuration** > **Ajouter un périphérique**

**Étape 3 : Appairer le capteur**

1. Appuyez **3 fois** sur le bouton du ST814
2. Attendez la détection (15-30 secondes)

**Étape 4 : Configurer le capteur**

1. **Nom** : `Capteur Temp/Hum Extérieur` (ou selon l'emplacement)
2. **Pièce** : Selon l'utilisation
3. Le capteur apparaît avec 2 valeurs :
   - Température
   - Humidité
4. **Enregistrer**

**Étape 5 : Configuration avancée**

Consultez la documentation pour configurer :
- **Intervalle de rapport** : Fréquence d'envoi des données (ex : toutes les 10 minutes)
- **Seuils d'alerte** : Température min/max, humidité min/max

**Étape 6 : Utilisation**

Créez des scènes ou des alertes basées sur :
- Température basse/élevée
- Humidité basse/élevée (risque de moisissures)

**Exemple de scène :**
- **SI** Humidité > 70% **ALORS** Envoyer notification "Humidité élevée - Risque moisissures"

**À documenter :**
- Valeurs mesurées par le capteur
- Configuration des intervalles
- Graphiques d'évolution

---

### Tâche 12 : Schéma de câblage pour capteur d'ouverture filaire

#### Objectif

Proposer un schéma de câblage pour connecter un **capteur d'ouverture filaire** (contact magnétique) à un module Z-Wave compatible.

#### Principe de fonctionnement

Un capteur d'ouverture filaire est un **contact sec** (switch) :
- **Porte fermée** : Contact fermé (continuité électrique)
- **Porte ouverte** : Contact ouvert (pas de continuité)

#### Module Z-Wave pour contacts filaires

Utilisez un module comme :
- **Fibaro Universal Binary Sensor (FGBS-001)**
- **Aeotec Dry Contact Sensor**
- **Philio PAN04** (4 entrées)

#### Schéma de câblage

```
┌─────────────────────────────────┐
│  Module Z-Wave (ex: Fibaro UBS) │
│                                  │
│   IN1 ●─────┐                   │
│             │                   │
│   GND ●─────┼───────┐           │
│             │       │           │
└─────────────┼───────┼───────────┘
              │       │
              │   ┌───┴───┐
              │   │ Capteur│
              │   │ filaire│
              │   │(contact│
              │   │  sec)  │
              └───┤        │
                  └────────┘
```

#### Schéma détaillé pour 4 capteurs

Si vous utilisez un module avec 4 entrées (comme le Philio PAN04) :

```
Module Philio PAN04
─────────────────────
IN1 ●───[ Capteur 1 (Porte entrée) ]───┐
                                        │
IN2 ●───[ Capteur 2 (Fenêtre salon) ]──┤
                                        │
IN3 ●───[ Capteur 3 (Fenêtre chambre) ]┤
                                        │
IN4 ●───[ Capteur 4 (Garage) ]─────────┤
                                        │
GND ●───────────────────────────────────┘
```

#### Liste du matériel nécessaire

**Pour 1 capteur :**
- 1x Module Z-Wave avec entrée contact sec
- 1x Capteur d'ouverture filaire (contact magnétique)
- 2x Fils électriques (0,5 mm² minimum)
- Dominos ou borniers de connexion

**Pour 4 capteurs :**
- 1x Module Z-Wave 4 entrées (Philio PAN04)
- 4x Capteurs d'ouverture filaires
- 10x Fils électriques (8 pour les capteurs + 2 pour GND commun)

#### Procédure d'installation

**Étape 1 : Câblage du premier capteur**

1. **Couper l'alimentation** (sécurité)
2. Connecter un fil du capteur à **IN1** du module
3. Connecter l'autre fil du capteur à **GND** du module
4. Vérifier les connexions (pas de court-circuit)

**Étape 2 : Installation physique du capteur**

1. Fixer le capteur (partie avec fils) sur le **cadre de porte** (partie fixe)
2. Fixer l'aimant sur la **porte** (partie mobile)
3. Distance maximale : **10-15 mm**

**Étape 3 : Configuration dans Eedomus**

1. Ajouter le module Z-Wave (Fibaro UBS ou Philio PAN04)
2. Le module détecte automatiquement les capteurs connectés
3. Nommer chaque entrée :
   - IN1 : "Porte Entrée"
   - IN2 : "Fenêtre Salon"
   - etc.

**Étape 4 : Test**

1. Fermer la porte : Eedomus affiche "Fermé"
2. Ouvrir la porte : Eedomus affiche "Ouvert"
3. Vérifier pour chaque capteur

**À documenter :**
- Schéma de câblage détaillé (dessiné à la main ou sur ordinateur)
- Photos du montage réel
- Liste du matériel utilisé
- Tests de fonctionnement

#### Avantages/Inconvénients

| Capteurs filaires | Capteurs sans fil (Z-Wave) |
|-------------------|----------------------------|
| ✅ Pas de piles à changer | ❌ Piles à remplacer (1-2 ans) |
| ✅ Fiabilité maximale | ❌ Portée limitée (~30m) |
| ✅ Coût unitaire faible | ✅ Installation simple |
| ❌ Installation complexe (câblage) | ✅ Pas de câblage |
| ❌ Modifications structure bâtiment | ✅ Installation non-invasive |

---

## 📊 Présentation "Client"

### Objectif

Présenter l'installation domotique comme si vous étiez devant un client réel.

### Structure de la présentation (10 minutes)

**1. Introduction (1 min)**
- Présentation du projet domotique
- Besoins du client : confort, sécurité, économies d'énergie

**2. Système installé (3 min)**

**a) Centrale Eedomus+**
- Hub central Z-Wave
- Interface web accessible partout
- Compatible avec 200+ périphériques

**b) Éclairage intelligent**
- 2 ampoules RGB connectées
- Changement automatique selon température
- Contrôle à distance et programmation

**c) Capteurs multi-fonctions**
- 2 Multisensor 7 (intérieur/extérieur)
- Mesures : température, humidité, luminosité, UV, mouvement, vibration

**d) Sécurité**
- Capteurs d'ouverture (sans fil + filaires)
- Détection de vibration (tentative d'effraction)
- Notifications SMS en temps réel

**3. Démonstration live (4 min)**

**Scène 1 : Gestion de température**
- Montrer le changement de couleur des lampes selon température
- Expliquer le confort visuel

**Scène 2 : Alarme d'intrusion**
- Ouvrir la porte (capteur ZD206EU)
- Montrer le clignotement rouge des lampes
- Montrer la réception du SMS

**Scène 3 : Détection de vibration**
- Tapoter le Multisensor 7
- Montrer le déclenchement de l'alarme

**4. Avantages du système (1 min)**
- **Confort** : Automatisation, contrôle à distance
- **Sécurité** : Alarmes, notifications temps réel
- **Économies** : Optimisation chauffage/éclairage
- **Évolutivité** : Ajout facile de nouveaux périphériques

**5. Questions/Réponses (1 min)**

### Support de présentation

Créez un support visuel (PowerPoint/PDF) avec :
- Architecture du système (schéma)
- Photos des périphériques
- Captures d'écran de l'interface
- Démonstration des scènes

---

## 📋 Compte-rendu d'activité

### Structure du compte-rendu

**1. Page de garde**
- Titre, nom, classe, date

**2. Sommaire**

**3. Introduction**
- Contexte et objectifs
- Présentation de la domotique Z-Wave
- Matériel utilisé

**4. Partie technique**

**4.1 Présentation du système Eedomus**
- Caractéristiques de la box
- Interface web
- Protocole Z-Wave

**4.2 Installation des périphériques**
Pour chaque périphérique :
- Caractéristiques techniques
- Procédure d'appairage
- Configuration
- Tests

**4.3 Création des scènes**
- Scène gestion température
- Alarme intrusion (porte)
- Alarme vibration
- Captures d'écran

**4.4 Schéma de câblage filaire**
- Schéma détaillé
- Matériel nécessaire
- Procédure d'installation

**5. Présentation client**
- Script de présentation
- Support visuel
- Retours

**6. Analyse**
- Avantages/inconvénients Z-Wave
- Difficultés rencontrées
- Améliorations possibles

**7. Conclusion**

**8. Annexes**
- Documentation périphériques
- Configurations complètes

---

## ✅ Checklist finale

### Installation
- [ ] Connexion à l'interface Eedomus réussie
- [ ] 2 LED Bulb 6 ajoutées et nommées
- [ ] 2 Multisensor 7 ajoutés et configurés
- [ ] Capteur ZD206EU ajouté
- [ ] Capteur ST814 ajouté

### Scènes et automatisations
- [ ] Scène température < 19°C (Bleu)
- [ ] Scène température 19-22°C (Vert)
- [ ] Scène température > 22°C (Rouge)
- [ ] Alarme ouverture porte (clignotement + SMS)
- [ ] Alarme vibration configurée

### Tests
- [ ] Test changement couleur selon température
- [ ] Test alarme ouverture porte
- [ ] Test réception SMS
- [ ] Test détection vibration
- [ ] Test capteur ST814

### Documentation
- [ ] Schéma câblage capteurs filaires
- [ ] Compte-rendu complet avec captures
- [ ] Présentation client préparée
- [ ] Support visuel créé

---

## 📚 Ressources

### Documentation officielle

- **[Aide Eedomus en ligne](https://secure.eedomus.com/help/)**
- **[Site Aeotec](https://aeotec.com/)**
- **[Manuel ZD206EU](https://fr.manuals.plus/raylios/raylios-door-sensor-zd2102eu-5-manual#quickstart)**
- **[Configuration ST814](https://e-domotic.fr/blog/z-wave/capteurs-zwave/capteur-temperatureeverspring-st814/configuration-du-capteur-temperature-et-humidite-everspring-st814/)**

### Protocole Z-Wave

- [Z-Wave Alliance](https://z-wavealliance.org/)
- [Liste des périphériques certifiés](https://products.z-wavealliance.org/)

### Vidéos tutoriels

- Recherchez sur YouTube : "Eedomus tutoriel"
- Chaînes spécialisées domotique

---

**Bon courage pour ce TP de domotique ! 🏠🔌**