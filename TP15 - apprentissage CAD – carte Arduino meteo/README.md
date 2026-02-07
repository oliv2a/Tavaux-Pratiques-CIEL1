# TP : Initiation à KiCad - Station Météo Arduino Nano

**Durée estimée :** 4-6 heures  
**Niveau :** Débutant  
**Objectifs pédagogiques :**
- Installer et configurer KiCad
- Créer un projet KiCad
- Dessiner un schéma électronique
- Créer des symboles et empreintes personnalisés
- Concevoir un circuit imprimé (PCB)
- Générer les fichiers de fabrication

---

## Table des matières

1. [Introduction](#1-introduction)
2. [Installation de KiCad](#2-installation-de-kicad)
3. [Concepts de base](#3-concepts-de-base)
4. [Création du projet](#4-création-du-projet)
5. [Dessin du schéma](#5-dessin-du-schéma)
6. [Création de symboles personnalisés](#6-création-de-symboles-personnalisés)
7. [Vérification électrique (ERC)](#7-vérification-électrique-erc)
8. [Création d'empreintes personnalisées](#8-création-dempreintes-personnalisées)
9. [Conception du PCB](#9-conception-du-pcb)
10. [Génération des fichiers de fabrication](#10-génération-des-fichiers-de-fabrication)

---

## 1. Introduction

Ce TP vous guide dans la conception complète d'une **station météo basée sur Arduino Nano** avec :
- **Arduino Nano** : microcontrôleur principal
- **AHT10** : capteur de température et humidité (I²C)
- **Écran OLED 0.96" (SSD1306)** : affichage des données (I²C)
- Connecteur d'alimentation et résistances de pull-up I²C

Les composants **AHT10** et **OLED** n'existent pas dans les bibliothèques standard de KiCad. Vous allez donc apprendre à créer vos propres symboles et empreintes à partir des datasheets.

---

## 2. Installation de KiCad

### 2.1 Téléchargement

Rendez-vous sur le site officiel : [https://www.kicad.org/download/](https://www.kicad.org/download/)

Téléchargez la dernière version stable de KiCad pour votre système d'exploitation :
- **Windows** : Téléchargez l'installateur `.exe`
- **Linux** : Utilisez le gestionnaire de paquets de votre distribution
- **macOS** : Téléchargez le fichier `.dmg`

### 2.2 Installation

#### Windows
1. Exécutez l'installateur téléchargé
2. Suivez les instructions à l'écran
3. Assurez-vous de cocher l'option d'installation des bibliothèques par défaut

#### Linux (Ubuntu/Debian)
```bash
sudo add-apt-repository ppa:kicad/kicad-9.0-releases
sudo apt update
sudo apt install kicad
```

#### macOS
1. Ouvrez le fichier `.dmg` téléchargé
2. Glissez l'application KiCad dans le dossier Applications

### 2.3 Premier lancement

Au premier lancement de KiCad, vous serez invité à configurer les **tables de bibliothèques de symboles et d'empreintes**.

**Configuration de la table de bibliothèques de symboles :**
- Sélectionnez l'option **"Copy default global symbol library table (recommended)"**
- Si cette option est grisée, sélectionnez **"Copy custom global symbol library table"** et naviguez vers :
  - Windows : `C:\Program Files\KiCad\9.0\share\kicad\template\sym-lib-table`
  - Linux : `/usr/share/kicad/template/sym-lib-table`
  - macOS : `/Applications/KiCad/KiCad.app/Contents/SharedSupport/template/sym-lib-table`

**Configuration de la table de bibliothèques d'empreintes :**
- Même procédure, mais pour le fichier `fp-lib-table`

---

## 3. Concepts de base

### 3.1 Workflow typique dans KiCad

1. **Schéma électronique** : représentation symbolique du circuit
2. **Symboles** : représentations graphiques des composants (résistances, ICs, etc.)
3. **Empreintes (Footprints)** : dispositions physiques des pads sur le PCB
4. **Circuit imprimé (PCB)** : disposition physique des composants et routage des pistes

### 3.2 Structure d'un projet KiCad

Un projet KiCad contient :
- `.kicad_pro` : fichier de projet
- `.kicad_sch` : fichier de schéma
- `.kicad_pcb` : fichier de PCB
- `.kicad_sym` : bibliothèque de symboles (optionnel)
- `.kicad_mod` : empreintes (optionnel)

### 3.3 Navigation

- **Panoramique** : clic molette ou clic droit et déplacer
- **Zoom** : molette de la souris ou `F1`/`F2`
- **Grille** : Les symboles utilisent une grille de **50 mil (1.27 mm)**

---

## 4. Création du projet

### 4.1 Créer un nouveau projet

1. Lancez **KiCad** depuis le menu Démarrer (Windows) ou Applications (Linux/macOS)
2. Dans le **Gestionnaire de projet**, cliquez sur **Fichier → Nouveau projet**
3. Naviguez vers un emplacement approprié (ex : `Documents/KiCad_Projects/`)
4. Nommez le projet `station_meteo_nano`
5. Cochez **"Create a new folder for the project"**
6. Cliquez sur **Enregistrer**

### 4.2 Structure du projet

Vous devriez voir dans le panneau de gauche :
```
station_meteo_nano/
├── station_meteo_nano.kicad_pro
├── station_meteo_nano.kicad_sch
└── station_meteo_nano.kicad_pcb
```

---

## 5. Dessin du schéma

### 5.1 Ouvrir l'éditeur de schéma

1. Dans le Gestionnaire de projet, cliquez sur **Éditeur de schéma**
2. L'éditeur s'ouvre avec une page vierge

### 5.2 Configuration de la page

1. Cliquez sur **Fichier → Propriétés de la page**
2. Remplissez les champs :
   - **Titre** : Station Météo Arduino Nano
   - **Date** : (date actuelle)
   - **Révision** : v1.0
   - **Taille du papier** : A4
3. Cliquez sur **OK**

### 5.3 Ajouter les composants standards

#### 5.3.1 Arduino Nano

1. Cliquez sur le bouton **Ajouter un symbole** ![icône](A) dans la barre d'outils de droite ou appuyez sur `A`
2. Dans la boîte de recherche, tapez `Arduino Nano`
3. Sélectionnez `MCU_Module:Arduino_Nano_v3.x`
4. Cliquez sur **OK** et placez le composant au centre du schéma
5. Appuyez sur `Échap` pour sortir du mode placement

#### 5.3.2 Résistances de pull-up I²C

1. Appuyez sur `A` pour ajouter un symbole
2. Recherchez et sélectionnez `Device:R` (résistance)
3. Placez deux résistances à droite de l'Arduino Nano
4. Sélectionnez chaque résistance et appuyez sur `R` pour la faire pivoter si nécessaire

#### 5.3.3 Connecteur d'alimentation

1. Appuyez sur `A`
2. Recherchez `Connector:Barrel_Jack_Switch`
3. Placez le connecteur en haut à gauche du schéma

#### 5.3.4 Symboles d'alimentation

1. Cliquez sur le bouton **Ajouter un symbole d'alimentation** ![icône](P) ou appuyez sur `P`
2. Recherchez et ajoutez :
   - **VCC** (plusieurs instances nécessaires)
   - **GND** (plusieurs instances nécessaires)
3. Placez-les stratégiquement près des composants qui en ont besoin

### 5.4 Annotation des composants

Par défaut, KiCad annote automatiquement les composants lors de leur ajout. Vous pouvez vérifier ou modifier l'annotation :

1. Cliquez sur ![icône annotation](A) dans la barre d'outils supérieure
2. Vérifiez que l'annotation automatique est activée

### 5.5 Éditer les valeurs des composants

#### Résistances de pull-up
1. Sélectionnez la première résistance, clic droit → **Propriétés** (ou appuyez sur `E`)
2. Dans le champ **Valeur**, entrez `4.7k`
3. Répétez pour la seconde résistance

---

## 6. Création de symboles personnalisés

Les composants **AHT10** et **OLED SSD1306** n'existent pas dans les bibliothèques standard. Nous allons les créer.

### 6.1 Créer une bibliothèque de symboles du projet

1. Ouvrez l'**Éditeur de symboles** depuis le Gestionnaire de projet
2. Cliquez sur **Fichier → Nouvelle bibliothèque**
3. Sélectionnez **Projet** (pour une bibliothèque spécifique au projet)
4. Nommez la bibliothèque `station_meteo.kicad_sym`
5. Enregistrez-la dans le dossier du projet

### 6.2 Créer le symbole du capteur AHT10

#### 6.2.1 Informations du composant

Le **AHT10** est un capteur I²C avec 6 broches :
- **Pin 1 (VDD)** : Alimentation (2.0-5.5V)
- **Pin 2 (SDA)** : Ligne de données I²C
- **Pin 3 (GND)** : Masse
- **Pin 4 (GND)** : Masse
- **Pin 5 (SCL)** : Ligne d'horloge I²C  
- **Pin 6 (GND)** : Masse

#### 6.2.2 Création du symbole

1. Dans l'**Éditeur de symboles**, sélectionnez la bibliothèque `station_meteo`
2. Cliquez sur **Fichier → Nouveau symbole**
3. Remplissez les champs :
   - **Nom du symbole** : `AHT10`
   - **Désignateur de référence par défaut** : `U`
   - Cochez **Créer un symbole avec des unités de De Morgan** : Non
   - **Nombre d'unités par paquet** : 1
4. Cliquez sur **OK**

#### 6.2.3 Dessiner le rectangle du symbole

1. Sélectionnez l'outil **Rectangle** ![icône](R) dans la barre de droite
2. Dessinez un rectangle centré sur l'origine, environ 600 mil × 400 mil

**Conseil** : Utilisez les coordonnées suivantes pour les coins du rectangle :
- Coin supérieur gauche : `(-300, 200)`
- Coin inférieur droit : `(300, -200)`

#### 6.2.4 Ajouter les broches

**Important** : Les broches doivent être placées sur une grille de 50 mil !

1. Cliquez sur **Ajouter une broche** ![icône](P) dans la barre de droite
2. Configurez la première broche :
   - **Nom de la broche** : `VDD`
   - **Numéro de broche** : `1`
   - **Type électrique** : `Power input`
   - **Orientation** : `Right` (vers la droite)
   - **Position X** : `-400 mil`
   - **Position Y** : `150 mil`
3. Cliquez sur **OK** et placez la broche

4. Appuyez sur `Insert` pour créer rapidement les broches suivantes :
   - **Broche 2 - SDA** : Position `(-400, 50)`, Type `Bidirectional`
   - **Broche 3 - GND** : Position `(-400, -50)`, Type `Power input`
   - **Broche 4 - GND** : Position `(400, -50)`, Type `Power input`, Orientation `Left`
   - **Broche 5 - SCL** : Position `(400, 50)`, Type `Input`, Orientation `Left`
   - **Broche 6 - GND** : Position `(400, 150)`, Type `Power input`, Orientation `Left`

#### 6.2.5 Ajouter les labels

1. Sélectionnez l'outil **Texte** ![icône](T)
2. Ajoutez le texte `AHT10` au centre du rectangle
3. Positionnez le texte **Value** sous le symbole

#### 6.2.6 Propriétés du symbole

1. Double-cliquez sur la zone vide du symbole (ou **Fichier → Propriétés du symbole**)
2. Remplissez les champs :
   - **Valeur** : `AHT10`
   - **Mots-clés** : `temperature humidity sensor i2c aht10`
   - **Description** : `Capteur de température et humidité I2C`
   - **Afficher le nom de broche** : Oui
   - **Afficher le numéro de broche** : Oui

3. Enregistrez le symbole (**Ctrl+S**)

### 6.3 Créer le symbole de l'écran OLED SSD1306

#### 6.3.1 Informations du composant

L'**écran OLED 0.96"** (SSD1306) possède 4 broches en I²C :
- **Pin 1 (GND)** : Masse
- **Pin 2 (VCC)** : Alimentation (3.3-5V)
- **Pin 3 (SCL)** : Ligne d'horloge I²C
- **Pin 4 (SDA)** : Ligne de données I²C

#### 6.3.2 Création du symbole

1. Dans l'**Éditeur de symboles**, sélectionnez la bibliothèque `station_meteo`
2. Cliquez sur **Fichier → Nouveau symbole**
3. Remplissez :
   - **Nom du symbole** : `OLED_0.96_I2C`
   - **Désignateur de référence** : `DS` (Display)
4. Cliquez sur **OK**

#### 6.3.3 Dessiner le symbole

1. Dessinez un **rectangle** représentant l'écran : environ 800 mil × 400 mil
2. Ajoutez les **4 broches** :
   - **Broche 1 - GND** : Position `(-400, 150)`, Orientation `Right`, Type `Power input`
   - **Broche 2 - VCC** : Position `(-400, 50)`, Orientation `Right`, Type `Power input`
   - **Broche 3 - SCL** : Position `(-400, -50)`, Orientation `Right`, Type `Input`
   - **Broche 4 - SDA** : Position `(-400, -150)`, Orientation `Right`, Type `Bidirectional`

3. Ajoutez le texte **"OLED 0.96"** au centre du rectangle
4. Configurez les propriétés du symbole :
   - **Valeur** : `OLED_0.96_I2C`
   - **Mots-clés** : `oled display ssd1306 i2c 0.96`
   - **Description** : `Écran OLED 0.96 pouces I2C SSD1306`

5. Enregistrez le symbole

### 6.4 Utiliser les symboles personnalisés dans le schéma

1. Retournez dans l'**Éditeur de schéma**
2. Appuyez sur `A` pour ajouter un symbole
3. Dans la boîte de recherche, tapez `AHT10`
4. Sélectionnez le symbole dans la bibliothèque `station_meteo`
5. Placez-le dans le schéma
6. Répétez pour l'écran `OLED_0.96_I2C`

---

## 5.6 Câblage du schéma

### 5.6.1 Connexions I²C

Le bus I²C nécessite :
- **SDA** (données) : connecté à A4 sur l'Arduino Nano
- **SCL** (horloge) : connecté à A5 sur l'Arduino Nano
- Résistances de pull-up de 4.7kΩ vers VCC sur SDA et SCL

#### Étapes :

1. Cliquez sur **Ajouter un fil** ![icône](W) ou appuyez sur `W`
2. Connectez les broches suivantes :

**Connexions AHT10 :**
- `AHT10 VDD` → `VCC`
- `AHT10 SDA` → `Arduino A4`
- `AHT10 SCL` → `Arduino A5`
- `AHT10 GND (broches 3, 4, 6)` → `GND`

**Connexions OLED :**
- `OLED VCC` → `VCC`
- `OLED SDA` → `Arduino A4` (sur le même fil que AHT10 SDA)
- `OLED SCL` → `Arduino A5` (sur le même fil que AHT10 SCL)
- `OLED GND` → `GND`

**Résistances de pull-up :**
- `R1 (4.7k)` : une extrémité sur `SDA`, l'autre sur `VCC`
- `R2 (4.7k)` : une extrémité sur `SCL`, l'autre sur `VCC`

**Alimentation Arduino :**
- `Barrel Jack +` → `Arduino VIN`
- `Barrel Jack GND` → `GND`

### 5.6.2 Ajouter des labels de nets

Pour clarifier le schéma, ajoutez des labels sur les fils :

1. Cliquez sur **Dessiner des labels de nets** ![icône](L) ou appuyez sur `L`
2. Ajoutez les labels :
   - `SDA` sur le fil de données I²C
   - `SCL` sur le fil d'horloge I²C
   - `VCC` sur les fils d'alimentation
   - `GND` sur les fils de masse

**Conseil** : Les labels avec le même nom sont connectés électriquement, même sans fil visible.

---

## 7. Vérification électrique (ERC)

### 7.1 Lancer l'ERC

1. Cliquez sur ![icône ERC](E) dans la barre d'outils supérieure
2. Cliquez sur **Lancer ERC**
3. Examinez les erreurs et avertissements

### 7.2 Corriger les erreurs courantes

#### Erreur : "Input Power pin not driven"

Cette erreur apparaît souvent pour `VCC` et `GND` car KiCad ne détecte pas de source d'alimentation.

**Solution :** Ajouter un symbole `PWR_FLAG`

1. Appuyez sur `P` pour ajouter un symbole d'alimentation
2. Recherchez `PWR_FLAG`
3. Placez un `PWR_FLAG` sur les nets `VCC` et `GND`
4. Relancez l'ERC

Lorsque l'ERC ne signale plus d'erreurs, le schéma est validé électriquement.

---

## 8. Création d'empreintes personnalisées

Les empreintes définissent la disposition physique des pads sur le PCB.

### 8.1 Créer une bibliothèque d'empreintes du projet

1. Ouvrez l'**Éditeur d'empreintes** depuis le Gestionnaire de projet
2. Cliquez sur **Fichier → Nouvelle bibliothèque**
3. Sélectionnez **Projet**
4. Nommez la bibliothèque `station_meteo.pretty`
5. Enregistrez-la dans le dossier du projet

### 8.2 Créer l'empreinte de l'AHT10

#### 8.2.1 Informations du datasheet

Le **AHT10** est un composant **SMD** (montage en surface) avec un boîtier **DFN-6** :
- **Dimensions** : 3 mm × 3 mm
- **Espacement des pads** : 0.65 mm
- **Taille des pads** : 0.35 mm × 0.9 mm

**Note** : Ces valeurs sont approximatives. Consultez le datasheet réel fourni par le professeur pour les dimensions exactes.

#### 8.2.2 Création de l'empreinte

1. Dans l'**Éditeur d'empreintes**, sélectionnez la bibliothèque `station_meteo.pretty`
2. Cliquez sur **Fichier → Nouvelle empreinte**
3. Remplissez :
   - **Nom de l'empreinte** : `AHT10_DFN-6_3x3mm_P0.65mm`
   - **Valeur** : `AHT10`
   - **Type de composant** : `Surface mount`
4. Cliquez sur **OK**

#### 8.2.3 Configurer la grille

Pour faciliter le placement des pads :
1. Cliquez droit sur ![icône grille](G) dans la barre de gauche
2. Sélectionnez **Éditer les grilles**
3. Ajoutez une nouvelle grille avec le bouton `+` :
   - **Taille X** : `0.65 mm`
   - **Taille Y** : `0.9 mm`
4. Sélectionnez cette grille dans le menu déroulant en haut

#### 8.2.4 Ajouter les pads

1. Cliquez sur **Ajouter un pad** ![icône](P) dans la barre de droite
2. Placez le premier pad à la position `(-0.65, -0.95)`
3. Double-cliquez sur le pad pour éditer ses propriétés :
   - **Numéro de pad** : `1`
   - **Type de pad** : `SMD`
   - **Forme** : `Rectangulaire`
   - **Taille X** : `0.35 mm`
   - **Taille Y** : `0.9 mm`
   - **Couche** : `F.Cu` (cuivre avant)
4. Cliquez sur **OK**

5. Ajoutez les pads suivants avec l'outil pad ou `Insert` :
   - **Pad 2** : Position `(0, -0.95)`
   - **Pad 3** : Position `(0.65, -0.95)`
   - **Pad 4** : Position `(0.65, 0.95)`
   - **Pad 5** : Position `(0, 0.95)`
   - **Pad 6** : Position `(-0.65, 0.95)`

#### 8.2.5 Dessiner le contour (couche F.Fab)

1. Sélectionnez la couche **F.Fab** dans le panneau Couches à droite
2. Utilisez l'outil **Rectangle** ![icône](R)
3. Dessinez un rectangle de 3 mm × 3 mm centré à l'origine :
   - Coin supérieur gauche : `(-1.5, -1.5)`
   - Coin inférieur droit : `(1.5, 1.5)`

#### 8.2.6 Ajouter la sérigraphie (couche F.Silkscreen)

1. Sélectionnez la couche **F.Silkscreen**
2. Dessinez un contour légèrement plus grand que le boîtier (ex : 3.2 mm × 3.2 mm)
3. Ajoutez une marque (petit cercle ou ligne) au coin du pin 1 pour identifier l'orientation

#### 8.2.7 Ajouter la zone de courtoisie (F.Courtyard)

1. Sélectionnez la couche **F.Courtyard**
2. Dessinez un rectangle avec une marge de 0.25 mm autour du boîtier :
   - Coin supérieur gauche : `(-1.75, -1.75)`
   - Coin inférieur droit : `(1.75, 1.75)`

#### 8.2.8 Propriétés de l'empreinte

1. Cliquez sur ![icône propriétés](P) dans la barre supérieure
2. Remplissez :
   - **Description** : `AHT10 Temperature and Humidity Sensor, DFN-6 3x3mm`
   - **Mots-clés** : `AHT10 sensor temperature humidity DFN`
3. Enregistrez l'empreinte (**Ctrl+S**)

### 8.3 Créer l'empreinte de l'OLED 0.96"

#### 8.3.1 Informations du composant

L'écran OLED possède généralement un connecteur **4 broches traversantes (THT)** avec un espacement de **2.54 mm (0.1")**.

**Dimensions approximatives** :
- **Largeur totale** : 27 mm
- **Hauteur** : 28 mm
- **Zone d'affichage** : 26 mm × 13 mm

#### 8.3.2 Création de l'empreinte

1. Dans l'**Éditeur d'empreintes**, sélectionnez `station_meteo.pretty`
2. Cliquez sur **Fichier → Nouvelle empreinte**
3. Remplissez :
   - **Nom** : `OLED_0.96_I2C_THT`
   - **Valeur** : `OLED 0.96"`
   - **Type** : `Through hole`

#### 8.3.3 Configurer la grille

1. Sélectionnez une grille de **2.54 mm (100 mil)**

#### 8.3.4 Ajouter les pads traversants

1. Cliquez sur **Ajouter un pad**
2. Placez le pad 1 à la position `(0, 0)`
3. Éditez ses propriétés :
   - **Numéro** : `1`
   - **Type** : `Through hole`
   - **Forme** : `Circulaire`
   - **Diamètre** : `1.7 mm`
   - **Diamètre du trou** : `1.0 mm`

4. Ajoutez les 3 autres pads espacés de 2.54 mm :
   - **Pad 2** : Position `(0, 2.54)`
   - **Pad 3** : Position `(0, 5.08)`
   - **Pad 4** : Position `(0, 7.62)`

#### 8.3.5 Dessiner les couches graphiques

**Couche F.Fab :**
- Dessinez un rectangle représentant le PCB de l'écran : 27 mm × 28 mm
- Position du coin inférieur gauche : `(-13.5, -10)` (centré sur les pads)

**Couche F.Silkscreen :**
- Dessinez le contour du module
- Ajoutez un rectangle pour la zone d'affichage (optionnel)

**Couche F.Courtyard :**
- Rectangle de 29 mm × 30 mm (marge de 1 mm)

#### 8.3.6 Enregistrer l'empreinte

1. Configurez les propriétés de l'empreinte (description, mots-clés)
2. Enregistrez (**Ctrl+S**)

---

## 8.4 Associer les empreintes aux symboles

### 8.4.1 Dans l'Éditeur de symboles

1. Ouvrez l'**Éditeur de symboles**
2. Ouvrez le symbole **AHT10**
3. Allez dans **Fichier → Propriétés du symbole**
4. Dans le champ **Empreinte**, cliquez sur l'icône de bibliothèque ![icône livre](L)
5. Naviguez vers `station_meteo:AHT10_DFN-6_3x3mm_P0.65mm`
6. Cliquez sur **OK**
7. Enregistrez le symbole

Répétez pour **OLED_0.96_I2C** :
- Empreinte : `station_meteo:OLED_0.96_I2C_THT`

### 8.4.2 Assigner les empreintes dans le schéma

1. Retournez dans l'**Éditeur de schéma**
2. Cliquez sur ![icône empreinte](F) dans la barre supérieure (outil d'assignation d'empreintes)
3. Pour chaque composant dans la colonne centrale :
   - **Arduino Nano** : `Module:Arduino_Nano`
   - **R1, R2** : `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal`
   - **Barrel Jack** : `Connector_BarrelJack:BarrelJack_Horizontal`
   - **AHT10** : `station_meteo:AHT10_DFN-6_3x3mm_P0.65mm`
   - **OLED** : `station_meteo:OLED_0.96_I2C_THT`

4. Cliquez sur **OK**

---

## 9. Conception du PCB

### 9.1 Ouvrir l'éditeur de PCB

1. Retournez dans le **Gestionnaire de projet**
2. Cliquez sur **Éditeur de PCB**

### 9.2 Configuration de la page

1. Cliquez sur **Fichier → Propriétés de la page**
2. Remplissez les champs (titre, date, révision)

### 9.3 Configuration du PCB

1. Allez dans **Fichier → Configuration du PCB**
2. Onglet **Empilement physique** :
   - Vérifiez le nombre de couches de cuivre : **2** (Top et Bottom)
3. Onglet **Règles de conception → Contraintes** :
   - **Largeur de piste minimale** : `0.2 mm`
   - **Espacement minimal** : `0.2 mm`

### 9.4 Importer le schéma dans le PCB

1. Cliquez sur **Outils → Mettre à jour le PCB depuis le schéma** ou appuyez sur `F8`
2. Vérifiez les changements listés
3. Cliquez sur **Mettre à jour le PCB**
4. Cliquez sur **Fermer**
5. Placez les composants sur le PCB en cliquant

### 9.5 Dessiner le contour du PCB

1. Sélectionnez la couche **Edge.Cuts** dans le panneau Couches
2. Changez la grille à **1 mm** pour faciliter le dessin
3. Utilisez l'outil **Rectangle** ![icône](R)
4. Dessinez un rectangle autour des composants (ex : 50 mm × 40 mm)

### 9.6 Placer les composants

**Stratégie de placement :**
- **Arduino Nano** : au centre ou légèrement vers le bas
- **OLED** : en haut pour faciliter la visualisation
- **AHT10** : sur le côté, avec accès à l'air
- **Connecteur d'alimentation** : sur le bord
- **Résistances** : près des lignes I²C

**Manipulation des composants :**
- Sélectionner : clic gauche
- Déplacer : `M`
- Pivoter : `R`
- Retourner (face arrière) : `F`

1. Placez chaque composant en observant les lignes du **chevelu (ratsnest)** pour minimiser les croisements
2. Essayez d'obtenir une disposition logique et compacte

### 9.7 Routage des pistes

#### 9.7.1 Couches de cuivre

- **F.Cu** (rouge) : Face avant (composants)
- **B.Cu** (bleu) : Face arrière

#### 9.7.2 Configurer les largeurs de pistes

1. En haut de l'écran, dans la liste déroulante **Largeur de piste**, sélectionnez ou ajoutez :
   - **0.3 mm** : pour les signaux I²C
   - **0.6 mm** : pour l'alimentation VCC et GND

#### 9.7.3 Router les pistes

1. Cliquez sur **Router des pistes** ![icône](X) ou appuyez sur `X`
2. Cliquez sur un pad pour commencer une piste
3. Suivez le chevelu pour connecter les pads
4. Changez de couche pendant le routage avec `V` (via)
5. Terminez la piste en cliquant sur le pad de destination

**Conseils :**
- Routez d'abord les connexions critiques (I²C, alimentation)
- Utilisez des vias pour changer de couche si nécessaire
- Évitez les angles à 90° (préférez les 45°)

### 9.8 Plans de masse (zones de cuivre)

#### 9.8.1 Créer une zone GND sur la face arrière

1. Sélectionnez la couche **B.Cu**
2. Cliquez sur **Ajouter une zone remplie** ![icône](Z)
3. Cliquez sur un coin du PCB
4. Dans la boîte de dialogue :
   - **Net** : `GND`
   - **Couche** : `B.Cu`
5. Cliquez sur **OK**
6. Dessinez le contour de la zone en suivant les bords du PCB
7. Double-cliquez pour fermer la zone

#### 9.8.2 Remplir les zones

1. Cliquez sur **Édition → Remplir toutes les zones** ou appuyez sur `B`
2. La zone GND est maintenant remplie de cuivre

**Note :** Les pads GND se connectent automatiquement à la zone avec des reliefs thermiques.

### 9.9 Vérification des règles de conception (DRC)

1. Cliquez sur ![icône DRC](D) dans la barre supérieure
2. Cochez **Reremplir toutes les zones avant d'exécuter DRC**
3. Cliquez sur **Lancer DRC**
4. Corrigez toutes les erreurs signalées
5. Relancez le DRC jusqu'à obtenir 0 erreur

**Erreurs courantes :**
- Pistes trop proches
- Pads non connectés
- Pistes traversant d'autres pistes

### 9.10 Visualisation 3D

1. Cliquez sur **Affichage → Visualiseur 3D**
2. Inspectez le PCB en 3D
3. Vérifiez le placement des composants

**Note :** Certains composants personnalisés peuvent ne pas avoir de modèle 3D.

---

## 10. Génération des fichiers de fabrication

### 10.1 Fichiers Gerber

1. Cliquez sur **Fichier → Tracer**
2. Sélectionnez les couches à tracer :
   - `F.Cu` (cuivre avant)
   - `B.Cu` (cuivre arrière)
   - `F.Silkscreen` (sérigraphie avant)
   - `B.Silkscreen` (sérigraphie arrière, si utilisée)
   - `F.Mask` (masque de soudure avant)
   - `B.Mask` (masque de soudure arrière)
   - `Edge.Cuts` (contour du PCB)
3. **Répertoire de sortie** : créez un dossier `gerbers/` dans le projet
4. **Format** : `Gerber`
5. Cliquez sur **Tracer**

### 10.2 Fichiers de perçage

1. Dans la même fenêtre, cliquez sur **Générer fichier de perçage**
2. Vérifiez les paramètres :
   - **Format** : `Excellon`
   - **Unités** : `Millimètres`
3. Cliquez sur **Générer fichier de perçage**
4. Fermez la fenêtre

### 10.3 Vérifier les fichiers avec le visualiseur Gerber

1. Ouvrez le **Visualiseur Gerber** depuis le Gestionnaire de projet
2. Cliquez sur **Fichier → Charger les fichiers Gerber**
3. Sélectionnez tous les fichiers `.gbr` générés
4. Inspectez chaque couche pour détecter d'éventuels problèmes
5. Vérifiez que les trous de perçage sont correctement positionnés

### 10.4 Fichier BOM (nomenclature)

1. Retournez dans l'**Éditeur de schéma**
2. Cliquez sur **Outils → Générer nomenclature (BOM)**
3. Configurez le format de sortie (CSV ou HTML)
4. Cliquez sur **Exporter**
5. Enregistrez le fichier `BOM.csv`

---

## Conclusion

Félicitations ! Vous avez terminé votre premier projet KiCad complet :

✅ Installation et configuration de KiCad  
✅ Création d'un schéma électronique  
✅ Création de symboles personnalisés (AHT10, OLED)  
✅ Création d'empreintes personnalisées  
✅ Vérification électrique (ERC)  
✅ Conception du PCB  
✅ Routage des pistes et plans de masse  
✅ Vérification des règles de conception (DRC)  
✅ Génération des fichiers de fabrication (Gerber, perçage, BOM)

---

## Annexes

### A. Raccourcis clavier utiles

| Action | Raccourci |
|--------|-----------|
| Ajouter un symbole | `A` |
| Ajouter une alimentation | `P` |
| Ajouter un fil | `W` |
| Ajouter un label | `L` |
| Déplacer | `M` |
| Pivoter | `R` |
| Éditer propriétés | `E` |
| Supprimer | `Del` |
| Dupliquer | `Ctrl+D` |
| Répéter dernière action | `Insert` |
| Zoom avant | `F1` |
| Zoom arrière | `F2` |
| Mettre à jour PCB depuis schéma | `F8` |

### B. Ressources supplémentaires

- **Documentation officielle** : [https://docs.kicad.org](https://docs.kicad.org)
- **Forum KiCad** : [https://forum.kicad.info](https://forum.kicad.info)
- **Bibliothèques KiCad** : [https://kicad.github.io](https://kicad.github.io)
- **Tutoriels vidéo** : Rechercher "KiCad tutorial" sur YouTube

### C. Checklist de fin de projet

- [ ] Schéma complet et vérifié (ERC = 0 erreurs)
- [ ] Toutes les empreintes assignées
- [ ] PCB routé à 100%
- [ ] DRC passé (0 erreurs)
- [ ] Visualisation 3D inspectée
- [ ] Fichiers Gerber générés
- [ ] Fichier de perçage généré
- [ ] BOM exportée
- [ ] Fichiers vérifiés dans le visualiseur Gerber

---

## Critères d'évaluation

| Critère | Points |
|---------|--------|
| Installation correcte de KiCad | /2 |
| Schéma complet et fonctionnel | /4 |
| Symboles AHT10 et OLED créés correctement | /4 |
| Empreintes AHT10 et OLED créées correctement | /4 |
| ERC passé sans erreurs | /2 |
| PCB routé proprement | /6 |
| DRC passé sans erreurs | /2 |
| Fichiers de fabrication générés | /2 |
| Qualité globale du travail | /4 |
| **TOTAL** | **/30** |

---

**Auteur** : Olivier - BTS CIEL  
**Date** : 2025  
**Version** : 1.0
