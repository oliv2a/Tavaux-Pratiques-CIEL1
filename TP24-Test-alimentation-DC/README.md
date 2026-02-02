# TP 24 : Test de Convertisseur DC/DC pour les montages électroniques

## Informations générales

- **Type d'activité** : Cours/TP
- **Type d'évaluation** : Compte-rendu d'activité & questionnement oral
- **Durée** : 10h

## Matériel

1. Carte 1 "Module de charge de batterie au lithium Mini 1A avec interface USB" avec connecteur pour résistance externe
2. Carte 2 "Module de charge de batterie au lithium Mini 1A avec interface USB"
3. Carte 3 "Module de convertisseur de tension Geekcreit® Mini DC réglable"
4. Batterie LI-PO

## Tâches à effectuer

### 1. Étude théorique

Dans le dossier Cours, lire dans l'ordre :

a) "Cours sur les alimentations continues.pdf"

b) "alim-decoupage.pdf" (page 1 à 3)

c) "Les alimentations à découpage et convertisseurs DC-DC - Traité d'électricité et d'électronique pour le radioamateur - F6CRP.pdf"

### 2. Mesures avec résistance externe de 1,2 kΩ

Brancher la carte 1 selon le schéma 1 pour une résistance externe de 1,2K; mesurer la tension Vs et le courant Is.

### 3. Caractérisation du courant de charge

Pour toutes les valeurs de la résistance externe contenues dans la "pj2-35184-2242.pdf", relever les valeurs du courant Is; comparer à la documentation.

### 4. Charge à courant constant

Expliquer ce que signifie une charge à courant constant.

### 5. Caractéristiques de la batterie

Lire la documentation "pj2-msds-2209-2630.pdf"; pour cette batterie, donner :
- La tension nominale
- La capacité
- Le temps de charge maximal avec la carte 2

### 6. Mesures de sécurité

Indiquer les mesures principales de sécurité en fonctionnement normal.

### 7. État de charge de la batterie

Consulter les ressources suivantes :
- https://www.majordome-video.com/guides/le-guide-ultime-de-la-batterie-lipo/
- https://oscarliang.com/wp-content/uploads/2017/02/Lipo-battery-guide-Voltage-vs-capacity-used-percentage.jpg

Mesurer la tension de la batterie; en déduire la charge de celle-ci; déterminer la tension minimale admissible pour la batterie.

### 8. Décharge de la batterie

Si la tension de la batterie est > à 3,6 V, faire le branchement du schéma 2 pour décharger la batterie jusqu'à la valeur de tension de 3,6V.

- Estimer le temps de décharge (on considérera le courant comme constant pendant la décharge)
- Mesurer le temps de décharge
- Pendant la décharge, relever dans un tableau toutes les 10 mn :
  - Le temps
  - La tension
  - Le courant de décharge
  
**Note** : T=0 correspond au moment où l'on commence la décharge.

### 9. Courbes de décharge

Tracer les courbes de l'évolution de la tension et du courant de la batterie en fonction du temps (on utilisera un tableur) pendant la décharge.

### 10. Charge de la batterie

Câbler la carte 2 à la batterie déchargée (voir schéma 3).

- Estimer et mesurer le temps de charge
- Pendant la charge, relever dans un tableau toutes les 10 mn :
  - Le temps
  - La tension
  - Le courant de charge
  
**Note** : T=0 correspond au moment où l'on commence la charge.

### 11. Courbes de charge

Tracer les courbes de l'évolution de la tension et du courant de la batterie en fonction du temps (on utilisera un tableur) pendant la charge.

## Schémas de câblage

### Schéma 1 : Test avec résistance externe

```
Alimentation USB ──────► CARTE 1 ──► Bat+ ──► 100Ω ──► 100Ω ──► (A)
                            │                   │
                            └───────────────────┘
                          Résistance              Vs
                           externe                │
                                                  Is
                                              Bat-
```

**Description** :
- Alimentation USB connectée à CARTE 1
- Sortie Bat+ connectée à deux résistances de 100 Ohms en série
- Mesure de la tension Vs et du courant Is
- Résistance externe programmable connectée à CARTE 1

### Schéma 2 : Décharge de la batterie

```
        ┌──────────┐
        │          │
        │ Batterie │ ──► + ──► 10 Ohms ──► (A)
        │          │           │
        └──────────┘           │ Vbat
              │                │
              └────────────────┘
                    -         Ibat
```

**Description** :
- Batterie connectée à une résistance de charge de 10 Ohms
- Mesure de la tension Vbat et du courant Ibat

### Schéma 3 : Charge de la batterie

```
Alimentation  ┌─────────┐  Bat+   ┌───┐     ┌──────────┐
USB 3A    ───►│ CARTE 2 │───────►│ A │  ───►│          │
              └─────────┘    │    └───┘  +  │ Batterie │
                             │  Vbat ┌───┐  │          │
                        Bat- └──────►│ V │  └──────────┘
                                Ibat └───┘       -
```

**Description** :
- Alimentation USB 3A connectée à CARTE 2
- Sortie Bat+ et Bat- connectées à la batterie
- Mesures simultanées de Vbat (voltmètre) et Ibat (ampèremètre)

## Aide

Voir liens et PDF dans le dossier Documents
