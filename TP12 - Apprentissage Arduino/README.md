# TP d'initiation Arduino Nano

**Type d'activité :** Apprentissage  
**Type d'évaluation :** Non évalué  
**Durée :** 10h

## Matériel nécessaire

- 1 Kit Arduino Nano
- 1 Kit Arduino Uno (pour comparaison)
- 2 LED (dont 1 rouge)
- 2 Résistances (dont 1,5kΩ)
- 1 Bouton poussoir
- 1 Télécommande infrarouge avec récepteur
- 1 Condensateur 22µF
- 1 Oscilloscope Analog Discovery 2 (AD2)
- Câbles de connexion et breadboard

---

## Partie 1 : Installation et découverte de l'Arduino Nano

### 1.1 Installation de l'IDE Arduino

1. Télécharger et installer l'IDE Arduino depuis : https://www.arduino.cc/en/Guide
2. Connecter l'Arduino Nano via USB
3. Sélectionner le bon port COM dans **Outils > Port**
4. Sélectionner la carte **Arduino Nano** dans **Outils > Type de carte**
5. Sélectionner le processeur **ATmega328P** dans **Outils > Processeur**

### 1.2 Présentation de la plateforme Arduino

Arduino est une plateforme pilotée par un logiciel **open-source**, véritable environnement de développement intégré, pour écrire, compiler et transférer le programme vers une carte à microcontrôleur.

Le langage utilisé est proche du **code C**.

**Objectifs :**
- Être capable d'identifier la nature d'un signal (logique, analogique, PWM)
- Être capable d'identifier une entrée et une sortie sur un microcontrôleur
- Être capable d'appréhender les bases d'un langage de programmation

### 1.3 Découverte de l'Arduino Nano

#### Exercice N°1 : Analyse du schéma électrique de l'Arduino Nano

**Q1 :** Repérer sur la carte Arduino Nano et sur le schéma électrique le **connecteur USB**

**Q2 :** Repérer sur la carte Arduino Nano et sur le schéma électrique le **microcontrôleur (ATMEGA 328P)**

**Q3 :** Repérer sur la carte Arduino Nano et sur le schéma électrique le **bornier d'alimentation**

**Q4 :** Repérer sur la carte Arduino Nano et sur le schéma électrique le **bornier des entrées analogiques**

**Q5 :** Repérer sur la carte Arduino Nano et sur le schéma électrique le **bornier des E/S numériques**

**Q6 :** Repérer sur la carte Arduino Nano et sur le schéma électrique les **sorties PWM**

### 1.4 Types de signaux

#### Signal logique
- Tension : 0V ou 5V
- États : LOW (0) ou HIGH (1)
- Usage : Communication binaire, contrôle ON/OFF

#### Signal analogique
- Tension : 0V à 5V (continue)
- Résolution : 10 bits (0-1023)
- Usage : Mesure de capteurs analogiques

#### Signal PWM (Pulse Width Modulation / MLI)
- Tension : 0V / 5V
- Fréquence : ~490 Hz
- Rapport cyclique : 0% à 100%
- Formule : α = T₁/T
- Usage : Variation de luminosité LED, vitesse moteur

### 1.5 Caractéristiques des entrées-sorties

#### Entrées/Sorties numériques
- **Utilisation :** Recevoir/envoyer des informations logiques (0 ou 1)
- **Exemples :** Boutons, capteurs logiques, relais, voyants
- **Caractéristiques électriques :** 
  - Courant max par sortie : 40 mA
  - Courant max total : 200 mA
  - Tension : 5V

#### Sorties PWM
- **Utilisation :** Générer une impulsion à rapport cyclique variable
- **Exemples :** LED à luminosité variable, variation de vitesse moteur
- **Caractéristiques électriques :**
  - Signal : 0-5V
  - Rapport cyclique : 0% à 100%
  - Fréquence : ~490 Hz

#### Entrées analogiques
- **Utilisation :** Mesure de tension
- **Exemples :** Capteur de température, potentiomètre
- **Caractéristiques électriques :**
  - Tension d'entrée : 0 à +5V
  - Résolution : 10 bits (0-1023)
  - Nombre d'entrées : 6 (A0 à A5)

### 1.6 Présentation de l'interface logicielle Arduino IDE

#### Barre de boutons
- ✓ **Vérifier** : Compile le programme
- → **Téléverser** : Transfère vers la carte Arduino
- ☐ **Nouveau** : Création d'un nouveau programme
- ⎆ **Ouvrir** : Ouvrir un programme existant
- ⎘ **Enregistrer** : Enregistrer un programme
- 🗗 **Moniteur série** : Affichage des données

#### Moniteur série
Le moniteur série permet d'afficher des messages, textes reçus sur la carte Arduino et d'envoyer des caractères vers la carte Arduino. Cette fonctionnalité permet une mise au point facilitée des programmes, permettant d'afficher sur l'ordinateur l'état de variables, de résultats de calculs ou de conversions analogique-numérique.

---

## Partie 2 : Découverte du langage basique de l'Arduino

### 2.1 Les instructions `void setup()` et `void loop()`

#### Exercice N°2 : Analyse d'un programme basique

**Q1 :** À l'aide de la référence Arduino (https://www.arduino.cc/reference/en/), indiquer la fonction de chacune des lignes suivantes :
```cpp
void setup()                  // .....................................................
{                             // .....................................................
  pinMode(8, OUTPUT);         // .....................................................
}

void loop()                   // .....................................................
{
  digitalWrite(8, HIGH);      // .....................................................
  delay(1000);                // .....................................................
  digitalWrite(8, LOW);       // .....................................................
  delay(1000);                // .....................................................
}
```

**Q2 :** Quelle est alors la fonction de ce programme ?

**Q3 :** Compléter le schéma de raccordement ci-dessous pour tester le programme précédent avec l'Arduino Nano.

**Q4 :** Calculer la valeur de la résistance pour garantir I = 20mA (Tension LED VD1 = 2V).

**Schéma de principe :**
```
ATMEGA 328          R1        D1
Sortie logique ----[___]----[>|]----
n°8                              |
                                GND
```

**Calcul de la résistance :**
- Tension de sortie : 5V
- Tension LED : 2V
- Courant souhaité : 20mA
```
R = (Vsortie - VLED) / I
R = (5V - 2V) / 0,02A
R = 3V / 0,02A
R = 150Ω
```

**Q5 :** Réaliser le schéma de raccordement sur breadboard avec l'Arduino Nano

**Q6 :** Recopier le programme dans l'IDE Arduino

**Q7 :** Lancer le programme et vérifier le bon fonctionnement (faire valider par le professeur)

### 2.2 Les instructions `pinMode()`, `digitalWrite()`, `digitalRead()`

#### Exercice N°3 : Lecture d'une entrée numérique

**Q1 :** À partir de la référence Arduino, indiquer la fonction de chacune des lignes suivantes :
```cpp
void setup()
{
  pinMode(3, OUTPUT);         // .....................................................
  pinMode(2, INPUT);          // .....................................................
}

void loop()
{
  boolean valeurPin;          // .....................................................
  valeurPin = digitalRead(2); // .....................................................
  digitalWrite(3, valeurPin); // .....................................................
}
```

**Q2 :** Quelle est alors la fonction de ce programme ?

**Q3 :** Compléter le schéma de raccordement (1) permettant de visualiser un état logique haut sur la LED

**Q4 :** Compléter le schéma de raccordement (2) permettant de visualiser un état logique bas sur la LED

**Q5 :** Réaliser le schéma de raccordement avec l'Arduino Nano

**Q6 :** Recopier le programme

**Q7 :** Lancer le programme et vérifier le bon fonctionnement (faire valider par le professeur)

### 2.3 L'instruction `if`

#### Exercice N°4 : Structure conditionnelle

**Q1 :** À partir de la référence Arduino, indiquer la fonction de l'instruction `if`

**Q2 :** Compléter le programme permettant d'allumer la LED sur la sortie n°2 en fonction de l'état du bouton sur l'entrée n°3 (utiliser la structure if)
```cpp
void setup()
{
  pinMode(2, OUTPUT);
  pinMode(3, INPUT);
}

void loop()
{
  boolean valeurPin;
  valeurPin = digitalRead(3);
  
  // Compléter avec la structure if
  // .................................................
  // {
  //   .................................................
  // }
  // .................................................
  // {
  //   .................................................
  // }
}
```

**Schéma de raccordement :**
```
              +5V
               |
              R2
               |
          +---+---+
          |  SW1  |
          +---+---+
              |
              +---- Pin 3
              |
             R1
              |
             GND

Pin 2 ----[R]----[LED]---- GND
```

**Q3 :** Réaliser le schéma de raccordement

**Q4 :** Recopier le programme

**Q5 :** Lancer le programme et vérifier le bon fonctionnement (faire valider par le professeur)

### 2.4 L'instruction `while`

#### Exercice N°5 : Boucle while

**Q1 :** À partir de la référence Arduino, indiquer la fonction de l'instruction `while`

**Q2 :** Sans modifier votre câblage, proposer un programme pour allumer la LED tant que le bouton n'est pas actionné (utiliser la structure while)

**Q3 :** Lancer le programme et vérifier le bon fonctionnement (faire valider par le professeur)

### 2.5 Les différents types de variables

**Q1 :** Indiquer le type d'une variable binaire ou logique et préciser les valeurs possibles

**Q2 :** Indiquer le type d'une variable entière et préciser les valeurs possibles

**Q3 :** Que représente la variable de type `char` ?

---

## Partie 3 : PWM avec Arduino - Variation de luminosité

### 3.1 Objectifs
- Comprendre le principe de la PWM (Pulse Width Modulation)
- Générer un signal PWM avec l'Arduino Nano
- Faire varier la luminosité d'une LED
- Valider le signal à l'oscilloscope

### 3.2 Lecture préalable
Lire attentivement :
- La documentation sur la Conversion Numérique/Analogique – PWM
- La page de référence Arduino sur la fonction `analogWrite()`

### 3.3 Exercice N°6 : Variation automatique de luminosité

**Matériel :**
- Arduino Nano
- LED rouge
- Résistance adaptée
- Oscilloscope Analog Discovery 2 (AD2)

**Q1 :** Réaliser le câblage de la LED et de la résistance sur une **sortie PWM** de l'Arduino Nano

**Rappel :** Sur l'Arduino Nano, les sorties PWM sont indiquées par le symbole **~** (tilde)  
Broches PWM disponibles : D3, D5, D6, D9, D10, D11

**Q2 :** Préciser le repère indiquant les sorties PWM sur la carte

**Q3 :** Réaliser un programme faisant varier la valeur de PWM de 0 à 100% par pas de 1% sur une durée de 10 secondes. Le programme recommence au début.

**Aide :**
- La fonction `analogWrite(pin, value)` permet de générer un signal PWM
- `value` varie de 0 (0%) à 255 (100%)
- Pour un pas de 1% : incrément de 255/100 ≈ 2,55
- Délai entre chaque pas : 10000ms / 100 = 100ms

**Structure du programme :**
```cpp
void setup() {
  // Initialiser la broche PWM en sortie
  pinMode(?, OUTPUT);
}

void loop() {
  // Boucle de 0 à 255
  for (int i = 0; i <= 255; i++) {
    analogWrite(?, i);
    delay(?);
  }
}
```

**Q4 :** Valider à l'aide de l'oscilloscope AD2 que le signal est présent sur la commande de la LED

**Relevés à effectuer :**
- Signal PWM à 25% (valeur ≈ 64)
- Signal PWM à 50% (valeur = 128)
- Signal PWM à 75% (valeur ≈ 192)
- Signal PWM à 100% (valeur = 255)

**Q5 :** Faire valider par le professeur

### 3.4 Exercice N°7 : Contrôle par télécommande infrarouge

**Matériel supplémentaire :**
- Télécommande infrarouge
- Récepteur infrarouge

**Q1 :** Câbler le récepteur infrarouge sur l'Arduino Nano (voir documentation TP37)

**Q2 :** Installer la bibliothèque nécessaire pour la télécommande IR

**Q3 :** Réaliser un programme faisant varier la valeur de PWM :
- De 0 à 100% par pas de 1% en augmentant lors d'un appui sur **˄**
- De 100% à 0% par pas de 1% en diminuant lors d'un appui sur **˅**

**Structure du programme :**
```cpp
#include <IRremote.h>

int RECV_PIN = ?;  // Pin du récepteur IR
int LED_PIN = ?;   // Pin PWM de la LED
int pwmValue = 0;  // Valeur PWM actuelle

IRrecv irrecv(RECV_PIN);
decode_results results;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  irrecv.enableIRIn();
  Serial.begin(9600);
}

void loop() {
  if (irrecv.decode(&results)) {
    // Détecter le code de la touche ˄
    if (results.value == CODE_HAUT) {
      // Augmenter PWM
    }
    // Détecter le code de la touche ˅
    else if (results.value == CODE_BAS) {
      // Diminuer PWM
    }
    
    irrecv.resume();
  }
  
  analogWrite(LED_PIN, pwmValue);
}
```

**Q4 :** Valider à l'aide de l'oscilloscope AD2 que le signal varie correctement

**Q5 :** Faire valider par le professeur

---

## Partie 4 : PWM avec régulation - Filtre passe-bas

### 4.1 Objectifs
- Comprendre la conversion PWM → Tension continue
- Implémenter un filtre passe-bas RC
- Réaliser une régulation simple de tension

### 4.2 Matériel
- Arduino Nano
- Analog Discovery 2 (AD2)
- Résistance 1,5 kΩ
- Condensateur 22 µF
- Breadboard et câbles

### 4.3 Exercice N°8 : Test du signal PWM de base

**Programme mli1.ino :**
```cpp
int pwmPin = 9;      // Sortie PWM
int pwmValue = 191;  // 75% de 255

void setup() {
  pinMode(pwmPin, OUTPUT);
}

void loop() {
  analogWrite(pwmPin, pwmValue);
}
```

**Q1 :** Tester le programme `mli1.ino`

**Q2 :** Régler le signal MLI à 75% (valeur = 191)

**Q3 :** Relever le signal MLI à l'aide de l'AD2

**Observations à noter :**
- Fréquence du signal : ........ Hz
- Rapport cyclique mesuré : ........ %
- Tension max : ........ V
- Tension min : ........ V

### 4.4 Exercice N°9 : Filtre passe-bas RC

**Schéma du filtre :**
```
PWM ----[1,5kΩ]----+---- A0
                   |
                 [22µF]
                   |
                  GND
```

**Q1 :** Câbler le filtre passe-bas entre la sortie MLI (PWM) et l'entrée analogique A0

**Programme mli2.ino :**
```cpp
int pwmPin = 9;       // Sortie PWM
int analogPin = A0;   // Entrée analogique
int pwmValue = 191;   // 75% de 255

void setup() {
  pinMode(pwmPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  analogWrite(pwmPin, pwmValue);
  
  int sensorValue = analogRead(analogPin);
  float voltage = sensorValue * (5.0 / 1023.0);
  
  Serial.print("PWM: ");
  Serial.print(pwmValue);
  Serial.print(" | Analog: ");
  Serial.print(sensorValue);
  Serial.print(" | Voltage: ");
  Serial.println(voltage);
  
  delay(500);
}
```

**Q2 :** Tester le programme `mli2.ino`

**Q3 :** Régler le signal MLI à 75%

**Q4 :** Relever les signaux MLI et l'entrée analogique à l'aide de l'AD2

**Observations :**
- Tension moyenne théorique : 75% × 5V = ........ V
- Tension moyenne mesurée : ........ V
- Ondulation résiduelle : ........ mV

### 4.5 Exercice N°10 : Régulation de tension par PWM

**Objectif :** Réaliser une régulation simple de la tension moyenne de la MLI par comparaison

**Algorithme de régulation :**
```
Si Valeur Moyenne MLI < Vref alors
    Valeur MLI = Valeur MLI + 2
Sinon
    Valeur MLI = Valeur MLI - 2
```

**Q1 :** Réaliser le programme de régulation

**Programme à compléter :**
```cpp
int pwmPin = 9;
int analogPin = A0;
int pwmValue = 128;    // Valeur initiale (50%)
float Vref = 1.75;     // Tension de référence en volts

void setup() {
  pinMode(pwmPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // Générer le signal PWM
  analogWrite(pwmPin, pwmValue);
  
  // Lire la tension filtrée
  int sensorValue = analogRead(analogPin);
  float voltage = sensorValue * (5.0 / 1023.0);
  
  // Algorithme de régulation
  // À COMPLÉTER
  
  // Limiter pwmValue entre 0 et 255
  if (pwmValue > 255) pwmValue = 255;
  if (pwmValue < 0) pwmValue = 0;
  
  // Affichage pour debug
  Serial.print("Vref: ");
  Serial.print(Vref);
  Serial.print("V | Vmesure: ");
  Serial.print(voltage);
  Serial.print("V | PWM: ");
  Serial.println(pwmValue);
  
  delay(10);  // Petit délai pour la stabilité
}
```

**Q2 :** Valider le fonctionnement de l'algorithme en relevant les signaux MLI et l'entrée analogique à l'aide de l'AD2 pour **Vref = 1,75V**

**Observations :**
- Tension de consigne : 1,75 V
- Tension stabilisée : ........ V
- Valeur PWM stabilisée : ........ (théorique : 1,75/5 × 255 = 89)
- Temps de stabilisation : ........ ms

**Q3 :** Tester avec d'autres valeurs de Vref :
- Vref = 1,0 V → PWM ≈ ........
- Vref = 2,5 V → PWM ≈ ........
- Vref = 3,75 V → PWM ≈ ........

**Q4 :** Faire valider par le professeur

---

## Partie 5 : Questionnaire de synthèse

### 5.1 Questions Vrai/Faux

Répondre par **Vrai** ou **Faux** :

1. La fonction `void setup()` est obligatoire en début de programme ? ☐ Vrai ☐ Faux

2. La fonction `void setup()` permet d'initialiser le programme ? ☐ Vrai ☐ Faux

3. La fonction `void setup()` s'exécute plusieurs fois ? ☐ Vrai ☐ Faux

4. La fonction `void setup()` s'exécute une fois en début de programme ? ☐ Vrai ☐ Faux

5. La fonction `void loop()` est obligatoire ? ☐ Vrai ☐ Faux

6. La fonction `void loop()` s'exécute une seule fois ? ☐ Vrai ☐ Faux

7. La fonction `void loop()` s'exécute en permanence ? ☐ Vrai ☐ Faux

8. La fonction `pinMode()` permet d'affecter une broche en entrée ou en sortie ? ☐ Vrai ☐ Faux

9. La fonction `pinMode()` s'exécute toujours dans la fonction `void setup()` ? ☐ Vrai ☐ Faux

10. La fonction `pinMode()` s'exécute toujours dans la fonction `void loop()` ? ☐ Vrai ☐ Faux

11. La fonction `digitalRead()` permet ............ l'état logique sur une entrée.  
    ☐ d'écrire ☐ de lire

12. La fonction `digitalWrite()` permet ............ l'état logique sur une sortie.  
    ☐ d'écrire ☐ de lire

13. Les variables [0 et 1] sont des variables de type : ..............................

14. Les variables [0, 1, 20, 30, 32, 55…] sont des variables de type : ..............................

15. Les variables [A, B, C, D, …] sont des variables de type : ..............................

16. Quelle est l'unité de la fonction `delay()` ? ..............................

17. Donner la signification des termes HIGH et LOW : ..............................

18. Donner la signification des termes INPUT et OUTPUT : ..............................

19. L'Arduino Nano utilise le même microcontrôleur que l'Arduino Uno ? ☐ Vrai ☐ Faux

20. Le microcontrôleur de l'Arduino Nano est : ..............................

### 5.2 Questions sur le matériel Arduino Nano

21. Combien de broches PWM possède l'Arduino Nano ? ..............................

22. Comment reconnait-on les broches PWM sur la carte ? ..............................

23. Quelle est la tension de fonctionnement logique de l'Arduino Nano ? ..............................

24. Combien d'entrées analogiques possède l'Arduino Nano ? ..............................

25. Quelle est la résolution du convertisseur analogique-numérique ? ..............................  
    (nombre de valeurs possibles)

26. Sur l'Arduino Nano, peut-on utiliser les broches analogiques comme E/S numériques ?  
    ☐ Oui ☐ Non

27. Quel est le courant maximum qu'une sortie numérique peut fournir ? ..............................

28. Quelle est la fréquence approximative du signal PWM ? ..............................

### 5.3 Questions sur la programmation

29. Quelle instruction permet de lire une entrée analogique ? ..............................

30. La fonction `analogRead()` renvoie une valeur entre ........... et ...........

31. Quelle instruction permet de générer un signal PWM ? ..............................

32. La fonction `analogWrite()` accepte une valeur entre ........... et ...........

33. Pour obtenir un rapport cyclique de 50%, quelle valeur doit-on mettre dans `analogWrite()` ?  
    ..............................

34. Quelle instruction permet d'afficher des messages sur le moniteur série ? ..............................

35. Quelle est la vitesse de communication série par défaut (baud rate) ? ..............................

### 5.4 Questions sur les signaux

36. Un signal PWM à 75% a un état haut pendant ........... % du temps.

37. Un signal PWM peut être converti en tension continue à l'aide d'un filtre : ..............................

38. Pour un filtre RC passe-bas, quels composants sont nécessaires ?  
    - R = ..............................
    - C = ..............................

39. Avec un signal PWM à 5V et un rapport cyclique de 60%, quelle sera la tension moyenne après filtrage ?  
    ..............................

40. Dans une régulation simple, si la tension mesurée est inférieure à la consigne, on doit :  
    ☐ Augmenter le PWM ☐ Diminuer le PWM

---

## Ressources et références

### Liens utiles
- Référence du langage Arduino : https://www.arduino.cc/reference/en/
- Documentation Arduino Nano : https://docs.arduino.cc/hardware/nano
- Tutoriels Arduino : https://www.arduino.cc/en/Tutorial/HomePage
- Forum Arduino français : https://forum.arduino.cc/c/francais/28

### Documentation à consulter
- Branchements conditionnels en C : `synthese-arduino-branchements.pdf`
- Documentation des fonctions Arduino (format PDF fourni)
- TP37 : Télécommande infrarouge

### Bibliothèques utiles
- **IRremote** : Pour la gestion de la télécommande infrarouge
- **Serial** : Pour la communication avec le moniteur série (intégrée)

---

## Validation finale

Pour valider ce TP, l'étudiant doit :

- ✓ Avoir réalisé tous les exercices pratiques
- ✓ Faire valider par le professeur les montages et programmes fonctionnels
- ✓ Compléter le questionnaire de synthèse
- ✓ Comprendre les principes de base de la programmation Arduino
- ✓ Savoir utiliser les E/S numériques, analogiques et PWM
- ✓ Être capable de réaliser un montage simple avec LED, bouton et capteurs

**Signature du professeur :**

---

*Ce TP a été conçu pour une initiation progressive à l'Arduino Nano, en 10 heures de formation pratique.*