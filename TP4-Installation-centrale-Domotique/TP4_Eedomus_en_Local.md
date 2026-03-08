# TP4 - Installation d'une Centrale Domotique sans fil au protocole Z-Wave

## Informations générales

**Type d'activité :** Installation  
**Durée :** 10 heures  
**Type d'évaluation :** Présentation "Client" et compte-rendu d'activité

---

## Objectifs

À l'issue de ce TP, vous serez capable de :

- Configurer une centrale domotique Eedomus+
- Ajouter et paramétrer des périphériques Z-Wave (capteurs et actionneurs)
- Créer des règles domotiques automatisées depuis l'interface locale
- Configurer un système d'alarme avec notifications
- Intégrer des capteurs filaires et sans fil
- Présenter une installation domotique à un client

---

## Matériel nécessaire

### Centrale domotique
- **1 Eedomus+** (box domotique Z-Wave)

### Périphériques d'éclairage
- **2 lampes LED Bulb 6** (Aeotec) — Ampoules connectées RGB Z-Wave

### Capteurs multi-fonctions
- **2 Multisensor 7** (Aeotec) — Capteurs 6-en-1 : température, humidité, luminosité, UV, mouvement, vibration

### Capteurs d'intrusion
- **1 capteur ZD206EU** — Capteur d'ouverture de porte/fenêtre sans fil Z-Wave (Raylios)
- **4 capteurs d'intrusion filaire** — Contacts magnétiques câblés
- **1 Everspring ST814-1** — Capteur de température et humidité Z-Wave

---

## Informations de connexion

**Plateforme Eedomus (cloud) :**
- **URL** : [https://secure.eedomus.com/](https://secure.eedomus.com/)
- **Utilisateur** : `email_connexion@xxx.fr`
- **Mot de passe** : `M_D_P`

**Interface locale (réseau du lycée) :**
- **URL** : `http://eedomus.local` ou `http://192.168.x.x` (adresse IP de la box)
- L'adresse IP locale se trouve dans : **Configuration > Ma box > Réseau**

> **Important** : Les identifiants cloud sont partagés entre tous les groupes. Nommez clairement vos périphériques pour les identifier (ex. : suffixe `_GrpX`).

---

## Architecture du système Eedomus

### Deux modes de fonctionnement

L'Eedomus+ fonctionne selon deux modes complémentaires :

**Mode cloud** (`secure.eedomus.com`) :
- Accès depuis n'importe où sur internet
- Inclusion/exclusion des modules Z-Wave
- Configuration avancée des périphériques
- Historique long des données (abonnement Premium)
- Envoi de SMS et notifications push

**Mode local** (`http://IP_box`) :
- Accès direct sur le réseau local (sans internet)
- Pilotage en temps réel des actionneurs
- Lecture des dernières valeurs des capteurs
- Exécution des règles et scénarios
- Création et modification des règles

> **Important** : L'inclusion et l'exclusion des modules Z-Wave nécessitent la connexion internet (interface cloud). Une fois les modules inclus, tout le pilotage peut se faire en local.

---

## Tâches à effectuer

### Tâche 1 : Connexion à la plateforme Eedomus

#### Se connecter à l'interface web cloud

1. Ouvrez un navigateur web
2. Accédez à : [https://secure.eedomus.com/](https://secure.eedomus.com/)
3. Entrez les identifiants fournis par votre enseignant
4. Cliquez sur **"Se connecter"**

#### Interface principale

Vous arrivez sur le **tableau de bord** de votre box Eedomus. Familiarisez-vous avec :
- **Configuration** : Gestion des périphériques, inclusion Z-Wave
- **Règles** : Création des automatisations
- **Graphiques** : Historique des capteurs
- **Ma box** : Paramètres réseau, configuration proxy

#### Accès à l'interface locale

1. Relevez l'adresse IP de la box : **Configuration > Ma box > Réseau**
2. Notez cette adresse (ex. : `192.168.1.42`)
3. Depuis un navigateur sur le réseau local : `http://192.168.1.42`
4. Connectez-vous avec les mêmes identifiants que le portail cloud
5. Ajoutez cette adresse en **favori** pour un accès rapide

**À documenter :**
- Capture d'écran du tableau de bord cloud
- Adresse IP locale de la box
- Capture d'écran de l'interface locale

---

### Tâche 2 : Consulter le site d'aide en ligne

#### Documentation Eedomus

Parcourez la documentation officielle :

**[Aide Eedomus en ligne](https://doc.eedomus.com/)**

**Sections importantes à consulter :**
- Ajouter un périphérique Z-Wave
- Création de règles
- Accéder à la box en local
- API eedomus

**À documenter :**
- Notes sur les fonctionnalités découvertes
- Questions éventuelles

---

### Tâche 3 : Prendre connaissance de la documentation

#### Documentation des fabricants

Consultez les ressources suivantes :

**Aeotec (LED Bulb 6 et Multisensor 7) :**
- **[Site officiel Aeotec](https://aeotec.com/)**
- Recherchez les manuels de vos périphériques

**Capteur ZD206EU (Raylios) :**
- **[Manuel ZD206EU](https://fr.manuals.plus/raylios/raylios-door-sensor-zd2102eu-5-manual#quickstart)**

**Capteur ST814 (Everspring) :**
- **[Configuration ST814](https://e-domotic.fr/blog/z-wave/capteurs-zwave/capteur-temperatureeverspring-st814/configuration-du-capteur-temperature-et-humidite-everspring-st814/)**

**À documenter :**
- Caractéristiques techniques de chaque périphérique
- Procédure d'inclusion propre à chaque module (nombre d'appuis bouton)
- Portée et limitations

---

### Tâche 4 : Vérifier la configuration du proxy

Si vous êtes dans un environnement avec proxy (lycée), vous devez le configurer pour que la box puisse accéder à internet et permettre l'inclusion des modules.

#### Configurer le proxy sur la box

1. Dans l'interface Eedomus cloud, allez dans **Configuration > Ma box**
2. Section **Réseau**
3. Configurez :
   - **Proxy HTTP** : `proxy.lycee:8080` (adapter selon votre réseau)
   - **Port** : `8080`
4. Enregistrez et redémarrez la box si nécessaire

#### Test de connectivité

- Allez dans **Configuration > Ma box**
- Section **État de la box**
- Vérifiez **"Connexion Internet"** : doit être ✅

**En cas de problème :**
- Contactez l'administrateur réseau
- Vérifiez les paramètres proxy
- Redémarrez la box

---

### Tâche 5 : Comprendre le principe d'inclusion/exclusion Z-Wave

Avant d'inclure vos premiers modules, il est indispensable de comprendre le mécanisme d'inclusion Z-Wave sur Eedomus.

#### Principe général

L'inclusion Z-Wave consiste à associer un module à la box Eedomus (le contrôleur). La box et le module doivent tous deux être mis en mode appairage simultanément.

**Règle d'or : toujours exclure avant d'inclure**

Un module Z-Wave d'occasion, ou un module qui a déjà été inclus dans un autre réseau (ou dans le vôtre lors d'un test raté), **doit être exclu avant toute nouvelle inclusion**. Sans exclusion préalable, l'inclusion échouera systématiquement.

> Cette règle s'applique même aux modules neufs sortis d'usine : par précaution, effectuez toujours une exclusion avant la première inclusion.

#### Procédure d'exclusion préalable (à faire avant chaque inclusion)

1. Sur le portail cloud, allez dans **Configuration > Ajouter ou supprimer un périphérique**
2. Cliquez sur **"Supprimer un périphérique (exclusion)"**
3. La box passe en mode exclusion (LED de la box change)
4. Approchez le module à **moins d'1 mètre** de la box
5. Appuyez sur le bouton du module selon sa notice (souvent 3 appuis rapides)
6. Attendez le message de confirmation : *"Périphérique exclu"* ou *"Déjà exclu"*
7. Cliquez sur **"Terminer"**

> Si le message indique *"Déjà exclu"* ou *"Aucun périphérique détecté"*, c'est normal : le module était déjà vierge. Vous pouvez passer à l'inclusion.

#### Procédure d'inclusion générique

1. Sur le portail cloud : **Configuration > Ajouter ou supprimer un périphérique**
2. Cliquez sur **"Ajouter un périphérique"**
3. La box passe en mode inclusion (30 à 60 secondes)
4. Approchez le module à **moins d'1 mètre** de la box
5. Appuyez sur le bouton du module selon sa notice
6. Attendez la détection et la configuration automatique
7. Nommez le périphérique et enregistrez

**Si l'inclusion échoue :**
- Ne relancez pas une nouvelle inclusion immédiatement
- Recommencez par une exclusion (étape ci-dessus), puis retentez l'inclusion
- En cas d'échec répété, redémarrez la box

#### Que se passe-t-il après l'inclusion ?

Une fois le module inclus via le portail cloud, il est opérationnel. Vous pouvez ensuite le piloter et créer des règles aussi bien depuis le portail cloud que depuis l'interface locale, même sans connexion internet.

---

### Tâche 6 : Ajouter les 2 lampes LED Bulb 6

#### Spécifications des LED Bulb 6

- **Fabricant** : Aeotec
- **Type** : Ampoule RGB Z-Wave Plus
- **Puissance** : 6W — Culot : E27
- **Couleurs** : 16 millions (RGB + blanc froid/chaud)
- **Inclusion** : Allumage/extinction rapide 6 fois consécutives

#### Procédure d'ajout

**Étape 1 : Exclusion préalable**

1. Vissez la lampe dans une douille alimentée
2. Sur le portail cloud : **Configuration > Ajouter ou supprimer un périphérique > Supprimer un périphérique**
3. Allumez/éteignez rapidement la lampe **6 fois** (via l'interrupteur mural)
4. Attendez la confirmation d'exclusion
5. Cliquez sur **"Terminer"**

**Étape 2 : Inclusion de la première lampe**

1. Sur le portail cloud : **Configuration > Ajouter ou supprimer un périphérique > Ajouter un périphérique**
2. La box passe en mode inclusion
3. Allumez/éteignez rapidement la lampe **6 fois**
4. La lampe clignote pour confirmer l'appairage
5. Attendez que la box détecte et configure le périphérique

**Étape 3 : Nommer le périphérique**

1. Une fois détectée, nommez-la : `Lampe1_GrpX`
2. **Pièce** : "Salle P18"
3. Cliquez sur **"Enregistrer"**

**Étape 4 : Répéter pour la deuxième lampe**

Recommencez les étapes 1 à 3 (exclusion puis inclusion).  
Nommez la seconde lampe : `Lampe2_GrpX`

**Étape 5 : Tester les lampes depuis l'interface locale**

Depuis `http://IP_box` :
1. Cliquez sur **Lampe1** puis **"Allumer"**
2. Testez les couleurs : Rouge, Vert, Bleu, Blanc
3. Testez la variation d'intensité
4. Répétez pour **Lampe2**

**À documenter :**
- Captures d'écran de l'ajout des périphériques
- Tests de fonctionnement (photos des lampes allumées en différentes couleurs)

---

### Tâche 7 : Ajouter les 2 Multisensor 7

#### Spécifications du Multisensor 7

- **Fabricant** : Aeotec
- **Type** : Capteur 6-en-1 Z-Wave Plus (série 700)
- **Mesures** : Température, humidité, luminosité (lux), UV, mouvement (PIR), vibration
- **Alimentation** : 2 piles CR123A ou USB (mode répéteur si USB)
- **Portée Z-Wave** : ~150m en champ libre
- **Inclusion** : 1 appui sur le bouton

#### Canaux créés dans Eedomus

Lors de l'inclusion, le Multisensor 7 crée automatiquement **plusieurs périphériques** dans Eedomus, un par type de mesure :

| Canal | Description |
|---|---|
| Mouvement | Détection PIR (Oui/Non) |
| Température | Valeur en °C |
| Humidité | Valeur en % |
| Luminosité | Valeur en Lux |
| UV | Indice UV |
| Vibration | Détection de choc/sabotage |

#### Procédure d'ajout

**Étape 1 : Exclusion préalable du premier capteur**

1. Insérez les piles dans le Multisensor 7
2. Sur le portail cloud : **Configuration > Ajouter ou supprimer un périphérique > Supprimer un périphérique**
3. Approchez le capteur à moins d'1 mètre de la box
4. Appuyez **1 fois** sur le bouton du Multisensor 7
5. Attendez la confirmation d'exclusion
6. Cliquez sur **"Terminer"**

**Étape 2 : Inclusion du premier capteur**

1. Sur le portail cloud : **Configuration > Ajouter ou supprimer un périphérique > Ajouter un périphérique**
2. La box passe en mode inclusion
3. Appuyez **1 fois** sur le bouton du Multisensor 7
4. La LED clignote (orange puis vert)
5. Attendez la détection et la configuration automatique (15 à 30 secondes)

**Étape 3 : Nommer le premier capteur**

1. Une fois détecté, nommez le périphérique principal : `Multisensor_Int_GrpX`
2. **Pièce** : "Salle P18"
3. Cliquez sur **"Enregistrer"**
4. Les sous-canaux (Température, Humidité, etc.) sont créés automatiquement sous ce périphérique

**Étape 4 : Vérifier les valeurs**

1. Dans **Configuration > Liste des périphériques**, dépliez le Multisensor
2. Vérifiez que tous les canaux apparaissent
3. Si un canal est vide, appuyez une fois sur le bouton du capteur pour forcer l'envoi des valeurs

> Note : En mode piles, le capteur se met en veille entre deux envois. Les valeurs ne se mettent à jour que toutes les 30 à 60 minutes (selon la configuration). Alimenté en USB, les valeurs sont envoyées en temps réel.

**Étape 5 : Ajouter le canal Température au tableau de bord**

1. Cliquez sur le canal **"Température"** du Multisensor
2. Cliquez sur **"Ajouter au tableau de bord"**
3. La valeur de température est maintenant visible sur la page d'accueil

**Étape 6 : Répéter pour le deuxième capteur**

Recommencez les étapes 1 à 5 (exclusion préalable obligatoire).  
Nommez le second capteur : `Multisensor_Ext_GrpX`

**Étape 7 : Tester les capteurs depuis l'interface locale**

Depuis `http://IP_box` :
1. Vérifiez les températures affichées pour chaque capteur
2. Passez la main devant les capteurs (détection de mouvement)
3. Tapez légèrement sur les capteurs (détection de vibration)

**À documenter :**
- Liste des canaux créés pour chaque capteur
- Captures d'écran des mesures
- Valeurs lues pour chaque canal

---

### Tâche 8 : Ajouter le capteur d'ouverture ZD206EU

#### Spécifications du ZD206EU

- **Fabricant** : Raylios
- **Type** : Capteur d'ouverture porte/fenêtre Z-Wave
- **Composants** : 2 parties (aimant + capteur électronique)
- **Portée** : ~30m en intérieur — **Alimentation** : 1 pile CR2032
- **Inclusion** : 3 appuis rapides sur le bouton

#### Procédure d'ajout

**Étape 1 : Exclusion préalable**

1. Insérez la pile CR2032
2. Sur le portail cloud : **Configuration > Ajouter ou supprimer un périphérique > Supprimer un périphérique**
3. Appuyez **3 fois rapidement** sur le bouton du capteur
4. Attendez la confirmation
5. Cliquez sur **"Terminer"**

**Étape 2 : Inclusion**

1. Sur le portail cloud : **Configuration > Ajouter ou supprimer un périphérique > Ajouter un périphérique**
2. Appuyez **3 fois rapidement** sur le bouton du capteur
3. La LED clignote et Eedomus détecte le périphérique

**Étape 3 : Configurer le capteur**

1. **Nom** : `Porte_P18_GrpX`
2. **Pièce** : "Salle P18"
3. **Type** : Détecteur d'ouverture
4. **Enregistrer**

**Étape 4 : Installation physique**

1. Partie électronique : sur le **cadre de porte** (partie fixe)
2. Aimant : sur la **porte** (partie mobile)
3. Distance maximale entre les deux parties : **10 à 15 mm**
4. Fixation : adhésif double face ou vis

**Étape 5 : Tester depuis l'interface locale**

Depuis `http://IP_box` :
1. Fermez la porte : état = **"Fermé"**
2. Ouvrez la porte : état = **"Ouvert"**

**À documenter :**
- Photo du capteur installé
- Distance mesurée entre capteur et aimant
- Tests d'ouverture/fermeture

---

### Tâche 9 : Ajouter le capteur Everspring ST814-1

#### Spécifications du ST814-1

- **Fabricant** : Everspring
- **Type** : Capteur de température et humidité Z-Wave
- **Plages** : Température -20°C à +60°C / Humidité 0% à 100%
- **Alimentation** : 2 piles AAA — **Inclusion** : 3 appuis sur le bouton

#### Procédure d'ajout

**Étape 1 : Exclusion préalable**

1. Insérez les 2 piles AAA
2. Sur le portail cloud : **Configuration > Ajouter ou supprimer un périphérique > Supprimer un périphérique**
3. Appuyez **3 fois** sur le bouton du ST814
4. Attendez la confirmation
5. Cliquez sur **"Terminer"**

**Étape 2 : Inclusion**

1. Sur le portail cloud : **Configuration > Ajouter ou supprimer un périphérique > Ajouter un périphérique**
2. Appuyez **3 fois** sur le bouton du ST814
3. Attendez la détection (15 à 30 secondes)

**Étape 3 : Configurer le capteur**

1. **Nom** : `TempHum_GrpX`
2. **Pièce** : selon l'emplacement choisi
3. Le capteur apparaît avec 2 canaux : Température et Humidité
4. **Enregistrer**

**Étape 4 : Configuration avancée (optionnelle)**

Consultez la documentation pour configurer :
- **Intervalle de rapport** : Fréquence d'envoi des données (ex. : toutes les 10 min)
- **Seuils d'alerte** : Température min/max, humidité min/max

**À documenter :**
- Valeurs mesurées par le capteur
- Configuration de l'intervalle de rapport

---

### Tâche 10 : Créer les règles domotiques depuis l'interface locale

Les règles (ou scènes) permettent d'automatiser des actions en fonction de conditions. Elles peuvent être créées depuis le portail cloud **ou depuis l'interface locale** — les deux sont équivalents pour cette fonction.

Dans ce TP, vous allez **créer et tester les règles depuis l'interface locale** (`http://IP_box`) afin de travailler en autonomie, sans dépendre de la connexion internet.

#### Accès à la création de règles en local

1. Ouvrez `http://IP_box` dans votre navigateur
2. Connectez-vous avec vos identifiants
3. Allez dans **Règles** (ou **Scènes** selon la version)
4. Cliquez sur **"Ajouter une règle"**

---

#### Règle 1 : Gestion de la couleur des lampes selon la température

**Objectif** : Changer automatiquement la couleur des lampes en fonction de la température mesurée par le Multisensor intérieur.

| Température | Couleur |
|---|---|
| < 19°C | Bleu |
| 19°C à 22°C | Vert |
| > 22°C | Rouge |

**Créer la règle "Température Froide - Bleu"**

1. Depuis l'interface locale : **Règles > Ajouter une règle**
2. **Nom** : `Temp_Froide_GrpX`
3. **Condition** : SI Température de `Multisensor_Int_GrpX` **< 19**
4. **Action** :
   - `Lampe1_GrpX` : Allumer en Bleu (RGB : 0, 0, 255)
   - `Lampe2_GrpX` : Allumer en Bleu (RGB : 0, 0, 255)
5. **Enregistrer**

**Créer la règle "Température Normale - Vert"**

1. **Règles > Ajouter une règle**
2. **Nom** : `Temp_Normale_GrpX`
3. **Condition** :
   - SI Température de `Multisensor_Int_GrpX` **>= 19**
   - ET Température de `Multisensor_Int_GrpX` **<= 22**
4. **Action** :
   - `Lampe1_GrpX` : Allumer en Vert (RGB : 0, 255, 0)
   - `Lampe2_GrpX` : Allumer en Vert (RGB : 0, 255, 0)
5. **Enregistrer**

**Créer la règle "Température Chaude - Rouge"**

1. **Règles > Ajouter une règle**
2. **Nom** : `Temp_Chaude_GrpX`
3. **Condition** : SI Température de `Multisensor_Int_GrpX` **> 22**
4. **Action** :
   - `Lampe1_GrpX` : Allumer en Rouge (RGB : 255, 0, 0)
   - `Lampe2_GrpX` : Allumer en Rouge (RGB : 255, 0, 0)
5. **Enregistrer**

**Tests :**

| Test | Méthode | Résultat attendu |
|---|---|---|
| Froid | Approcher le capteur d'une fenêtre ouverte ou glaçons | Lampes bleues |
| Normal | Température ambiante (19-22°C) | Lampes vertes |
| Chaud | Approcher le capteur d'une source de chaleur (main, radiateur) | Lampes rouges |

---

#### Règle 2 : Alarme d'intrusion à l'ouverture de porte

**Objectif** : Quand le capteur ZD206EU détecte une ouverture, les lampes clignotent en rouge et un SMS est envoyé.

> Note : L'envoi de SMS nécessite un abonnement Premium actif. Si ce n'est pas le cas, remplacez l'action SMS par une notification dans l'interface uniquement.

**Créer la règle "Alarme Intrusion - Porte"**

1. Depuis l'interface locale : **Règles > Ajouter une règle**
2. **Nom** : `Alarme_Porte_GrpX`
3. **Condition** : SI `Porte_P18_GrpX` passe à **"Ouvert"**
4. **Actions** :
   - `Lampe1_GrpX` : Allumer en Rouge (100%)
   - `Lampe2_GrpX` : Allumer en Rouge (100%)
   - Attendre 0,5 seconde
   - `Lampe1_GrpX` : Éteindre
   - `Lampe2_GrpX` : Éteindre
   - Attendre 0,5 seconde
   - Répéter 10 fois
   - Envoyer SMS : `ALERTE : Intrusion détectée - Porte P18 ouverte !`
5. **Enregistrer**

**Créer la règle "Arrêt Alarme - Porte Fermée"**

1. **Règles > Ajouter une règle**
2. **Nom** : `ArretAlarme_Porte_GrpX`
3. **Condition** : SI `Porte_P18_GrpX` passe à **"Fermé"**
4. **Actions** :
   - `Lampe1_GrpX` : Éteindre
   - `Lampe2_GrpX` : Éteindre
5. **Enregistrer**

**Tests :**
1. Ouvrez la porte → vérifiez le clignotement rouge des lampes
2. Vérifiez la réception du SMS
3. Refermez la porte → vérifiez l'extinction des lampes

---

#### Règle 3 : Alarme de vibration (tentative d'effraction)

**Objectif** : Utiliser le canal Vibration du Multisensor 7 pour déclencher une alarme.

**Étape préalable : Activer la détection de vibration sur le capteur**

1. Sur le portail cloud ou en local : **Configuration > Périphériques**
2. Sélectionnez le canal **"Vibration"** du `Multisensor_Int_GrpX`
3. Dans les paramètres experts, activez la détection de vibration
4. Réglez la sensibilité (commencez par "Élevée" pour les tests)

**Créer la règle "Alarme Vibration"**

1. Depuis l'interface locale : **Règles > Ajouter une règle**
2. **Nom** : `Alarme_Vibration_GrpX`
3. **Condition** : SI Vibration de `Multisensor_Int_GrpX` détectée (valeur = 1 ou "Oui")
4. **Actions** :
   - `Lampe1_GrpX` : Allumer en Rouge
   - `Lampe2_GrpX` : Allumer en Rouge
   - Envoyer SMS : `ALERTE : Vibration détectée - Intrusion possible !`
5. **Enregistrer**

**Tests :**
1. Tapez légèrement sur le Multisensor 7
2. Vérifiez le déclenchement des lampes
3. Ajustez la sensibilité si nécessaire (trop de faux positifs → diminuez)

---

### Tâche 11 : Schéma de câblage pour capteurs d'ouverture filaires

#### Principe de fonctionnement

Un capteur d'ouverture filaire est un **contact sec** :
- **Porte fermée** : Contact fermé (continuité électrique)
- **Porte ouverte** : Contact ouvert (pas de continuité)

#### Module Z-Wave pour contacts filaires

Utilisez un module comme :
- **Fibaro Universal Binary Sensor (FGBS-001)**
- **Aeotec Dry Contact Sensor**
- **Philio PAN04** (4 entrées)

#### Schéma de câblage — 1 capteur

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

#### Schéma détaillé — 4 capteurs (Philio PAN04)

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

#### Procédure d'installation

**Étape 1 : Câblage**

1. Coupez l'alimentation (sécurité)
2. Connectez un fil du capteur à **IN1** du module
3. Connectez l'autre fil à **GND** du module
4. Vérifiez les connexions (pas de court-circuit)

**Étape 2 : Installation physique**

1. Fixez la partie électronique sur le **cadre de porte** (partie fixe)
2. Fixez l'aimant sur la **porte** (partie mobile)
3. Distance maximale : **10 à 15 mm**

**Étape 3 : Inclusion du module Z-Wave dans Eedomus**

1. Effectuez d'abord l'**exclusion préalable** du module (voir Tâche 5)
2. Puis procédez à l'**inclusion** (voir Tâche 5)
3. Nommez chaque entrée :
   - IN1 : `Porte_Entree_GrpX`
   - IN2 : `Fenetre_Salon_GrpX`
   - etc.

**Étape 4 : Test**

1. Fermez la porte : Eedomus affiche "Fermé"
2. Ouvrez la porte : Eedomus affiche "Ouvert"
3. Vérifiez pour chaque capteur

#### Comparatif capteurs filaires / sans fil

| Critère | Capteurs filaires | Capteurs Z-Wave sans fil |
|---|---|---|
| Autonomie | Illimitée (secteur) | Piles (1 à 2 ans) |
| Fiabilité | Maximale | Très bonne |
| Coût unitaire | Faible | Plus élevé |
| Installation | Câblage nécessaire | Simple, non-invasive |
| Modification bâtiment | Oui (passage de câbles) | Non |

**À documenter :**
- Schéma de câblage détaillé (dessiné ou sur ordinateur)
- Photos du montage réel
- Tests de fonctionnement pour chaque capteur

---

## Présentation "Client"

### Objectif

Présenter l'installation domotique comme si vous étiez devant un client réel.

### Structure de la présentation (10 minutes)

**1. Introduction (1 min)**
- Présentation du projet domotique
- Besoins du client : confort, sécurité, économies d'énergie

**2. Système installé (3 min)**

- Centrale Eedomus+ : hub Z-Wave, interface web locale et cloud
- Éclairage intelligent : 2 ampoules RGB connectées, changement automatique selon température
- Capteurs multi-fonctions : 2 Multisensor 7 (température, humidité, luminosité, UV, mouvement, vibration)
- Sécurité : capteurs d'ouverture (sans fil + filaires), détection de vibration, notifications SMS

**3. Démonstration live (4 min)**

- Scène 1 : Montrer le changement de couleur des lampes selon la température
- Scène 2 : Ouvrir la porte → clignotement rouge des lampes
- Scène 3 : Tapoter le Multisensor → déclenchement de l'alarme vibration

**4. Avantages du système (1 min)**
- Confort, sécurité, économies, évolutivité

**5. Questions/Réponses (1 min)**

### Support de présentation

Créez un support visuel (PowerPoint/PDF) avec :
- Architecture du système (schéma)
- Photos des périphériques
- Captures d'écran de l'interface
- Démonstration des règles

---

## Compte-rendu d'activité

### Structure du compte-rendu

**1. Page de garde** — Titre, nom, classe, date

**2. Sommaire**

**3. Introduction** — Contexte et objectifs, présentation de la domotique Z-Wave, matériel utilisé

**4. Partie technique**

- 4.1 Présentation du système Eedomus : box, interface cloud et locale, protocole Z-Wave
- 4.2 Procédure d'inclusion/exclusion Z-Wave : principe, exclusion préalable, inclusions réalisées
- 4.3 Installation des périphériques : pour chaque module, caractéristiques techniques, procédure d'appairage, configuration, tests
- 4.4 Création des règles : règle température/couleur, alarme porte, alarme vibration, captures d'écran
- 4.5 Schéma de câblage filaire : schéma détaillé, matériel, procédure, tests

**5. Présentation client** — Script, support visuel, retours

**6. Analyse** — Avantages/inconvénients Z-Wave, différences cloud vs local, difficultés rencontrées, améliorations possibles

**7. Conclusion**

**8. Annexes** — Documentation périphériques, configurations complètes

---

## Checklist finale

### Inclusion des périphériques (portail cloud)
- [ ] Exclusion préalable effectuée pour chaque module
- [ ] 2 LED Bulb 6 incluses et nommées
- [ ] 2 Multisensor 7 inclus et tous leurs canaux vérifiés
- [ ] Capteur ZD206EU inclus
- [ ] Capteur ST814 inclus
- [ ] Module contacts filaires inclus et entrées nommées

### Règles (interface locale)
- [ ] Règle Température < 19°C → Lampes bleues
- [ ] Règle Température 19-22°C → Lampes vertes
- [ ] Règle Température > 22°C → Lampes rouges
- [ ] Règle Alarme ouverture porte (clignotement + SMS)
- [ ] Règle Arrêt alarme porte fermée
- [ ] Règle Alarme vibration

### Tests
- [ ] Changement couleur selon température
- [ ] Alarme ouverture porte
- [ ] Réception SMS
- [ ] Détection vibration
- [ ] Capteur ST814 (température et humidité)
- [ ] Capteurs filaires (ouverture/fermeture)

### Documentation
- [ ] Schéma câblage capteurs filaires
- [ ] Compte-rendu complet avec captures d'écran
- [ ] Présentation client préparée
- [ ] Support visuel créé

---

## Ressources

### Documentation officielle

- **[Documentation Eedomus](https://doc.eedomus.com/)**
- **[Accès local à la box](https://doc.eedomus.com/view/Accéder_à_sa_box_eedomus_localement)**
- **[Ajouter un périphérique Z-Wave](https://doc.eedomus.com/view/Ajouter_un_périphérique_Z-Wave)**
- **[Site Aeotec](https://aeotec.com/)**
- **[Manuel ZD206EU](https://fr.manuals.plus/raylios/raylios-door-sensor-zd2102eu-5-manual#quickstart)**
- **[Configuration ST814](https://e-domotic.fr/blog/z-wave/capteurs-zwave/capteur-temperatureeverspring-st814/configuration-du-capteur-temperature-et-humidite-everspring-st814/)**

### Protocole Z-Wave

- [Z-Wave Alliance](https://z-wavealliance.org/)
- [Liste des périphériques certifiés](https://products.z-wavealliance.org/)

---

**Bon courage pour ce TP de domotique !**
