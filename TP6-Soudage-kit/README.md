# TP6 - Soudage et Vérification du fonctionnement d'un Kit (composants traversants)

## 📋 Informations générales

**Type d'activité :** Initiation au soudage  
**Durée :** 10 heures  
**Type d'évaluation :** Rapport d'activité écrit et mesures

---

## 🎯 Objectifs

À l'issue de ce TP, vous serez capable de :

- Identifier et vérifier les composants d'un kit électronique
- Réaliser des soudures de qualité sur composants traversants (THT)
- Identifier les défauts de soudure courants
- Utiliser un multimètre pour vérifier le fonctionnement d'un circuit
- Valider le fonctionnement d'un montage électronique

---

## 🛠️ Matériel nécessaire

### Kit et composants
- **1 Kit M** (kit électronique à souder)
- **Notice du kit** (schéma, nomenclature, instructions)

### Équipement de soudage
- **Fer à souder** (température réglable, 300-350°C recommandé)
- **Support de fer à souder**
- **Éponge humide** ou **laine de laiton** (nettoyage panne)
- **Fil de soudure** (étain 60/40 ou sans plomb, Ø 0.8-1mm)
- **Pompe à dessouder** ou **tresse à dessouder** (correction erreurs)
- **Pince coupante** (coupe des pattes de composants)
- **Pince à becs** (manipulation des composants)

### Équipement de mesure
- **Multimètre** (mesure tensions, résistances, continuités)
- **Analog Discovery 2 (AD2)** (oscilloscope, génération de signaux)

### Sécurité
- **Lunettes de protection**
- **Ventilation** (fumées de soudure)
- **Tapis antistatique** (ESD)

---

## 📚 Rappels de sécurité

### Avant de commencer

⚠️ **Règles de sécurité obligatoires :**

1. **Porter des lunettes de protection** (projections de soudure)
2. **Travailler dans un local ventilé** (fumées toxiques)
3. **Ne jamais toucher la panne du fer** (300°C+)
4. **Débrancher le fer quand inutilisé**
5. **Utiliser un support pour le fer à souder**
6. **Se laver les mains après manipulation** (résidus de flux)
7. **Précautions ESD** : bracelet antistatique pour composants sensibles

### Risques
- **Brûlures** : Panne à 300°C+
- **Inhalation de fumées** : Flux contient des substances irritantes
- **Décharges électrostatiques (ESD)** : Peuvent détruire les composants

---

## 📝 Tâches à effectuer

### Tâche 1 : Vérification du contenu du kit

#### Objectif
S'assurer que tous les composants sont présents avant de commencer le montage.

#### Procédure

**Étape 1 : Inventaire**

1. Ouvrir la boîte du Kit M
2. Sortir tous les composants et les disposer sur une surface propre
3. Ouvrir la **nomenclature** (liste des composants)
4. Vérifier composant par composant

**Étape 2 : Identification des composants**

Pour chaque composant, noter :
- **Type** (résistance, condensateur, LED, transistor, CI, etc.)
- **Valeur** (résistance en Ω, capacité en µF/nF, etc.)
- **Référence** (R1, C2, IC1, etc.)
- **Quantité**

**Tableau de vérification :**

| Référence | Type | Valeur | Quantité attendue | Quantité réelle | ✓/✗ |
|-----------|------|--------|-------------------|-----------------|-----|
| R1-R4 | Résistance | 10kΩ | 4 | | |
| C1-C2 | Condensateur céramique | 100nF | 2 | | |
| LED1 | LED | Rouge 5mm | 1 | | |
| IC1 | Circuit intégré | NE555 | 1 | | |
| PCB | Circuit imprimé | - | 1 | | |

**Étape 3 : Signaler les manquants**

Si des composants manquent, **ne pas commencer** le montage. Signaler à l'enseignant.

**À documenter :**
- Photo de tous les composants étalés
- Tableau de vérification complété
- Identification des composants (avec code couleur pour résistances)

---

### Tâche 2 : Réalisation du câblage du kit

#### Avant de souder : Comprendre le schéma

**Étape 1 : Lecture du schéma**

1. Ouvrir la notice du kit
2. Identifier le **schéma électrique**
3. Repérer le **plan d'implantation des composants**
4. Comprendre le fonctionnement du circuit

**Étape 2 : Ordre de montage**

**⚠️ Important :** Souder les composants **du plus petit au plus grand** :

1. **Résistances** (plates)
2. **Diodes** (attention au sens !)
3. **Supports de CI** (si présents)
4. **Condensateurs céramiques**
5. **Condensateurs électrolytiques** (attention polarité !)
6. **LEDs** (attention au sens !)
7. **Transistors** (respecter le brochage)
8. **Connecteurs, borniers**
9. **Circuits intégrés** (en dernier, dans les supports)

---

#### Tutoriel de soudage

**Ressources vidéo recommandées :**

- 🎥 **[Comment bien souder - Tutoriel complet (YouTube)](https://www.youtube.com/watch?v=Qps9woUGkvI)**
- 🎥 **[Soudage composants traversants - Guide débutant](https://www.youtube.com/watch?v=AqvHogekDI4)**
- 🎥 **[Les 10 erreurs de soudure à éviter](https://www.youtube.com/watch?v=Fp37DPZVdRI)**

**Ressources écrites :**

- 📖 **[Guide de soudage IPC](https://www.ipc.org/)**
- 📖 **[Adafruit Guide to Excellent Soldering](https://learn.adafruit.com/adafruit-guide-excellent-soldering)**
- 📖 **[SparkFun How to Solder](https://learn.sparkfun.com/tutorials/how-to-solder-through-hole-soldering)**

---

#### Technique de soudage correcte

**Les 5 étapes d'une bonne soudure :**

```
1. Chauffer PAD + patte simultanément (2-3 secondes)
   ───────────────────────
   Fer à souder ──►  ╱
                   PAD + Patte
                    │
                   PCB

2. Apporter la soudure (pas sur le fer !)
   ───────────────────────
        Fil étain ──►  ╱
   Fer ──►           PAD
                      │

3. La soudure fond et mouille le joint
   ───────────────────────
                    ╱╲
                  ╱    ╲  ← Cône de soudure
                 PAD    Patte

4. Retirer le fil de soudure (maintenir le fer 1s)

5. Retirer le fer rapidement
```

**Critères d'une bonne soudure :**

✅ **Forme de cône** ou volcan  
✅ **Surface brillante** et lisse  
✅ **Mouillage complet** du pad et de la patte  
✅ **Pas d'excès de soudure** (pas de boule)  
✅ **Pas de soudure froide** (aspect terne, granuleux)

---

#### Défauts courants à éviter

| Défaut | Cause | Solution |
|--------|-------|----------|
| **Soudure froide** (aspect terne) | Température trop basse ou temps trop court | Augmenter température, chauffer plus longtemps |
| **Pont de soudure** (court-circuit) | Trop de soudure | Retirer l'excès avec tresse à dessouder |
| **Soudure sèche** (pas de mouillage) | Oxydation, pad sale | Nettoyer, utiliser flux |
| **Composant brûlé** | Fer trop chaud ou trop longtemps | Réduire température, souder plus vite |
| **Pad décollé** | Surchauffe du PCB | Remplacer, souder rapidement |

---

#### Procédure de montage détaillée

**Exemple : Soudage d'une résistance**

1. **Identifier** la résistance (code couleur)
2. **Plier** les pattes à 90° (espacement = pad)
3. **Insérer** dans le PCB (pas de sens pour les résistances)
4. **Plier légèrement** les pattes côté cuivre (maintien temporaire)
5. **Souder** les deux pattes
6. **Couper** les pattes au ras avec la pince coupante
7. **Vérifier** la soudure (brillante, cône)

**Exemple : Soudage d'une diode ou LED**

⚠️ **Attention au sens !**

```
Diode/LED :
   Anode (+) ────┤►├──── Cathode (-)
                LED
         Patte longue = +
         Patte courte = -
         Méplat = -
```

1. Identifier le sens (patte longue = +, méplat = -)
2. Respecter le plan d'implantation
3. Insérer en respectant la polarité
4. Souder et couper

**Exemple : Condensateur électrolytique**

⚠️ **Polarisé ! Attention au sens !**

```
Condensateur électrolytique :
    + ║ -
      ║  ← Bande blanche côté -
      ║  ← Patte courte côté -
```

---

#### Progression du montage

**Créer un tableau de suivi :**

| Composant | Référence | Soudé | Vérifié | Observations |
|-----------|-----------|-------|---------|--------------|
| Résistances | R1-R4 | ☐ | ☐ | |
| Condensateurs | C1-C2 | ☐ | ☐ | |
| LED | LED1 | ☐ | ☐ | Respecter polarité |
| CI | IC1 | ☐ | ☐ | Utiliser support |

**À documenter :**
- Photos de chaque étape de montage
- Difficultés rencontrées
- Solutions apportées

---

### Tâche 3 : Analyse photographique des soudures

#### Objectif

Réaliser une auto-évaluation critique de la qualité des soudures.

#### Procédure

**Étape 1 : Photographie**

1. **Nettoyer la carte** (retirer résidus de flux avec alcool isopropylique)
2. **Photographier le côté soudures** :
   - Vue d'ensemble
   - Vues détaillées (macro) de zones représentatives
3. **Bon éclairage** (lumière naturelle ou LED blanche)
4. **Mise au point nette**

**Étape 2 : Identification des défauts**

Sur les photos, **annoter** :

- ✅ **Soudures correctes** (encadrer en vert)
- ⚠️ **Soudures moyennes** (encadrer en orange)
- ❌ **Défauts critiques** (encadrer en rouge)

**Étape 3 : Classification des défauts**

Pour chaque défaut, identifier :

| Type de défaut | Description | Gravité | Action corrective |
|----------------|-------------|---------|-------------------|
| Soudure froide | Aspect terne, granuleux | ⚠️ Moyenne | Refaire la soudure |
| Pont de soudure | Court-circuit entre pads | ❌ Critique | Retirer excès |
| Manque de soudure | Soudure insuffisante | ⚠️ Moyenne | Ajouter de la soudure |
| Soudure en boule | Excès, pas de cône | ⚠️ Faible | Acceptable si mouillage OK |
| Pad décollé | Pad arraché du PCB | ❌ Critique | Remplacement |

**À documenter :**
- Photos annotées avec flèches et légendes
- Tableau récapitulatif des défauts
- Auto-évaluation (note sur 20)
- Plan d'amélioration

---

### Tâche 4 : Mesures et vérification du fonctionnement

#### Objectif

Valider le fonctionnement correct du circuit monté.

---

#### Partie A : Tests visuels préliminaires

**Avant toute mise sous tension :**

**Checklist de sécurité :**

- [ ] Toutes les soudures sont terminées
- [ ] Pas de ponts de soudure visibles
- [ ] Tous les composants sont correctement orientés
- [ ] Pas de pattes en court-circuit
- [ ] Pas de composants manquants
- [ ] Circuits imprimé propre (pas de résidus)

---

#### Partie B : Tests électriques avec multimètre

**Test 1 : Continuité**

Vérifier qu'il n'y a **pas de court-circuit** :

```bash
Mode : Test de continuité (buzzer)
```

1. Multimètre en mode continuité
2. Vérifier entre **VCC et GND** : ne doit PAS sonner
3. Si ça sonne → **court-circuit** → ne pas alimenter !

**Test 2 : Résistances**

Mesurer chaque résistance soudée :

| Référence | Valeur théorique | Valeur mesurée | Écart | ✓/✗ |
|-----------|------------------|----------------|-------|-----|
| R1 | 10kΩ | | | |
| R2 | 10kΩ | | | |

Tolérance : ±5% (ou ±10% selon marquage)

**Test 3 : Continuité des pistes**

Vérifier que les connexions électriques sont correctes (comparer avec le schéma).

---

#### Partie C : Tests fonctionnels (selon le kit)

**⚠️ Se référer à la notice spécifique du Kit M**

**Exemple de tests courants :**

**Si le kit est un clignotant LED :**

1. Alimenter le circuit (pile 9V ou alimentation)
2. Vérifier que la LED clignote
3. Mesurer la fréquence de clignotement
4. Mesurer la tension aux bornes de la LED

**Si le kit est un oscillateur :**

1. Connecter l'AD2 en sortie du circuit
2. Visualiser le signal à l'oscilloscope
3. Mesurer :
   - Fréquence
   - Amplitude
   - Forme d'onde

**Test avec l'Analog Discovery 2 :**

1. **Oscilloscope** : Visualiser les signaux
   - Canal 1 : Signal d'entrée (si applicable)
   - Canal 2 : Signal de sortie
2. **Analyseur de spectre** : Analyser les fréquences
3. **Mesures automatiques** :
   - Fréquence
   - Amplitude peak-to-peak
   - Rapport cyclique (duty cycle)

**À documenter :**
- Tableau des mesures de résistances
- Résultat du test de continuité VCC/GND
- Captures d'écran de l'oscilloscope
- Photos du circuit en fonctionnement
- Comparaison valeurs théoriques vs mesurées

---

## 📊 Rapport d'activité

### Structure du rapport

**1. Page de garde**
- Titre : Soudage et vérification d'un kit électronique
- Nom, prénom, classe, date

**2. Sommaire**

**3. Introduction**
- Présentation du kit
- Objectifs du TP
- Rappels de sécurité

**4. Vérification du contenu**
- Tableau d'inventaire complété
- Photo des composants
- Identification (code couleur résistances)

**5. Réalisation du montage**
- Plan d'implantation (annoté)
- Ordre de montage suivi
- Photos des étapes clés
- Difficultés rencontrées et solutions

**6. Analyse des soudures**
- Photos côté soudures (vue d'ensemble + détails)
- Identification et annotation des défauts
- Tableau récapitulatif des défauts
- Auto-évaluation critique
- Actions correctives effectuées

**7. Mesures et validation**
- Tests préliminaires (continuité)
- Mesures des résistances (tableau)
- Tests fonctionnels
- Captures oscilloscope
- Analyse des résultats
- Conformité au cahier des charges

**8. Conclusion**
- Objectifs atteints
- Compétences acquises en soudage
- Points à améliorer
- Bilan personnel

**9. Annexes**
- Schéma électrique du kit
- Plan d'implantation
- Nomenclature complète
- Code couleur des résistances

---

## 🔍 Annexe : Code couleur des résistances

### Résistances 4 bandes

```
┌─────────────────────┐
│ ▌▌  ▌     ▌        │
│ 1  2  ×  Tolérance │
└─────────────────────┘

Valeur = (10×Bande1 + Bande2) × 10^Bande3
```

**Tableau des couleurs :**

| Couleur | Chiffre | Multiplicateur | Tolérance |
|---------|---------|----------------|-----------|
| Noir | 0 | ×1 | - |
| Marron | 1 | ×10 | ±1% |
| Rouge | 2 | ×100 | ±2% |
| Orange | 3 | ×1k | - |
| Jaune | 4 | ×10k | - |
| Vert | 5 | ×100k | ±0.5% |
| Bleu | 6 | ×1M | - |
| Violet | 7 | - | - |
| Gris | 8 | - | - |
| Blanc | 9 | - | - |
| Or | - | ×0.1 | ±5% |
| Argent | - | ×0.01 | ±10% |

**Exemples :**
- Marron-Noir-Rouge-Or = 10×100 = **1kΩ ±5%**
- Jaune-Violet-Orange-Or = 47×1000 = **47kΩ ±5%**

---

## 📚 Ressources

### Tutoriels soudage

**Vidéos YouTube (français) :**
- [Comment bien souder - Tuto complet](https://www.youtube.com/results?search_query=comment+bien+souder+composants)
- [Apprendre à souder des composants électroniques](https://www.youtube.com/watch?v=Qps9woUGkvI)
- [Les erreurs à éviter en soudage](https://www.youtube.com/watch?v=Fp37DPZVdRI)

**Guides écrits (anglais) :**
- [Adafruit Guide to Excellent Soldering](https://learn.adafruit.com/adafruit-guide-excellent-soldering)
- [SparkFun How to Solder](https://learn.sparkfun.com/tutorials/how-to-solder-through-hole-soldering)
- [IPC-A-610 Acceptability Standard](https://www.ipc.org/TOC/IPC-A-610.pdf)

### Sécurité

- [Fiche sécurité soudage électronique](https://www.inrs.fr/)
- [Guide ESD (décharges électrostatiques)](https://www.esda.org/)

### Outils de mesure

- [Guide du multimètre débutant](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter)
- [Documentation Analog Discovery 2](https://digilent.com/reference/test-and-measurement/analog-discovery-2/start)

---

## ✅ Checklist finale

### Avant de soumettre le rapport

**Montage :**
- [ ] Tous les composants sont soudés
- [ ] Pas de court-circuits
- [ ] Polarités respectées
- [ ] Soudures de qualité acceptable
- [ ] Pattes coupées proprement
- [ ] PCB nettoyé

**Mesures :**
- [ ] Test de continuité VCC/GND OK
- [ ] Résistances mesurées et conformes
- [ ] Tests fonctionnels effectués
- [ ] Captures oscilloscope réalisées

**Documentation :**
- [ ] Photos de toutes les étapes
- [ ] Photos annotées des soudures
- [ ] Tous les tableaux remplis
- [ ] Analyse critique des défauts
- [ ] Mesures documentées
- [ ] Rapport complet et soigné

---

## 💡 Conseils pour réussir

### Préparation
- Lire **entièrement** la notice avant de commencer
- Organiser les composants (par type)
- Préparer un espace de travail propre et dégagé

### Pendant le soudage
- **Patience** : ne pas précipiter
- Vérifier **deux fois** avant de souder (polarité, position)
- Nettoyer régulièrement la panne du fer
- Faire des **pauses** (éviter la fatigue)

### Qualité
- Privilégier la **qualité** sur la vitesse
- Ne pas hésiter à **refaire** une soudure douteuse
- Demander un **avis externe** en cas de doute

### Sécurité
- **Toujours** débrancher le fer quand inutilisé
- **Aérer** régulièrement
- **Ranger** les outils après usage

---

**Bon courage pour votre première expérience de soudage ! 🔧⚡**