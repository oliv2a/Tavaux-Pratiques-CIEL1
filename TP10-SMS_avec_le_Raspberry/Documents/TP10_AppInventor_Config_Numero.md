# TP10 - App Inventor : Configuration du numéro de téléphone

## Comprendre la logique

Quand l'utilisateur clique sur **"📱 Configurer numéro"** :
1. Une boîte de dialogue s'ouvre pour saisir le numéro
2. L'utilisateur tape le numéro et valide
3. Le numéro est sauvegardé dans la mémoire du téléphone (TinyDB)
4. Le numéro est configuré pour l'envoi de SMS

---

## Bloc 1 : Réaction au clic du bouton

Dans l'éditeur de blocs, cherchez dans le panneau gauche le composant **Btn_Config** :

```
when Btn_Config.Click
do
  call Notificateur.ShowTextDialog
    message : "Entrez le numéro de téléphone (format international) :"
    title : "Configuration"
    cancelable : true
```

### Comment construire ce bloc

1. Dans le panneau gauche, cliquez sur **Btn_Config**
2. Glissez le bloc violet **when Btn_Config.Click do**
3. Dans le panneau gauche, cliquez sur **Notificateur**
4. Glissez le bloc **call Notificateur.ShowTextDialog** à l'intérieur
5. Pour les paramètres :
   - Cliquez sur **Text** (panneau gauche, section Built-in)
   - Glissez deux blocs texte roses `" "` pour remplir `message` et `title`
   - Tapez le texte dans chaque bloc
   - Pour `cancelable` : cliquez sur **Logic** → glissez le bloc `true`

### Ce que fait ce bloc

> Au clic du bouton, une boîte de dialogue s'ouvre avec un champ de saisie texte. L'utilisateur peut taper son numéro ou annuler.

---

## Bloc 2 : Traitement après la saisie

Ce bloc se déclenche **automatiquement** après que l'utilisateur a validé ou annulé la boîte de dialogue :

```
when Notificateur.AfterTextInput
do
  ...
```

### Comment construire ce bloc

1. Dans le panneau gauche, cliquez sur **Notificateur**
2. Glissez le bloc marron **when Notificateur.AfterTextInput do**

> ⚠️ Ce bloc contient automatiquement une variable **responseText** qui contient ce que l'utilisateur a tapé.

---

## Bloc 3 : Vérification si le champ est vide

```
  if is empty responseText
  then
    call Notificateur.ShowAlert
      notice : "Aucun numéro saisi"
```

### Comment construire ce bloc

1. Cliquez sur **Control** (Built-in) → glissez le bloc **if then**
2. Cliquez sur **Text** → glissez **is empty** dans la condition `if`
3. Dans **is empty**, insérez la variable **responseText** :
   - Dans le bloc **when Notificateur.AfterTextInput**, survolez `responseText` → cliquez **get responseText**
4. Dans le `then`, ajoutez **call Notificateur.ShowAlert**
5. Remplissez `notice` avec un bloc texte : `"Aucun numéro saisi"`

### Ce que fait ce bloc

> Si l'utilisateur a validé sans rien taper (ou a annulé), on affiche un message d'alerte.

---

## Bloc 4 : Sauvegarde et configuration du numéro

```
  else
    set SMS_Envoi.PhoneNumber to responseText
    call TinyDB_Config.StoreValue
      tag : "numero_telephone"
      valueToStore : responseText
```

Le bloc `else` s'exécute si l'utilisateur a bien saisi un numéro.

### Ligne 1 : `set SMS_Envoi.PhoneNumber to responseText`

1. Cliquez sur **SMS_Envoi** → glissez **set SMS_Envoi.PhoneNumber to**
2. Insérez **get responseText** dedans

> Cela configure immédiatement le numéro pour l'envoi de SMS.

### Ligne 2 : `call TinyDB_Config.StoreValue`

1. Cliquez sur **TinyDB_Config** → glissez **call TinyDB_Config.StoreValue**
2. Pour `tag` : bloc texte `"numero_telephone"`
3. Pour `valueToStore` : **get responseText**

> Cela **sauvegarde le numéro** dans la mémoire permanente du téléphone. Même si on ferme l'application, le numéro sera mémorisé au prochain lancement.

---

## Bloc 5 : Confirmation visuelle

```
    call Notificateur.ShowAlert
      notice : join("Numéro configuré : " responseText)

    set Lbl_Statut.Text to "Numéro configuré ✓"
    set Lbl_Statut.TextColor to color Green
```

### Ligne 1 : Afficher une alerte de confirmation

1. Ajoutez **call Notificateur.ShowAlert**
2. Pour `notice` : on veut afficher `"Numéro configuré : +33612345678"`
3. Cliquez sur **Text** → glissez le bloc **join**
4. Dans **join** : bloc texte `"Numéro configuré : "` + **get responseText**

### Ligne 2 : Mettre à jour le label de statut

1. Cliquez sur **Lbl_Statut** → **set Lbl_Statut.Text to**
2. Bloc texte : `"Numéro configuré ✓"`

### Ligne 3 : Changer la couleur en vert

1. Cliquez sur **Lbl_Statut** → **set Lbl_Statut.TextColor to**
2. Cliquez sur **Colors** → glissez le bloc couleur **Green**

---

## Résultat visuel attendu

Quand l'utilisateur clique sur **📱 Configurer numéro** :

```
┌─────────────────────────────┐
│         Configuration        │
│                              │
│  Entrez le numéro de         │
│  téléphone (format           │
│  international) :            │
│                              │
│  ┌─────────────────────┐    │
│  │ +33612345678        │    │
│  └─────────────────────┘    │
│                              │
│    [Annuler]   [OK]          │
└─────────────────────────────┘
```

Après validation :
- Une alerte s'affiche : **"Numéro configuré : +33612345678"**
- Le label en bas de l'écran affiche **"Numéro configuré ✓"** en vert
- Le numéro est mémorisé pour les prochains lancements

---

## Pourquoi utiliser TinyDB ?

Sans TinyDB, si l'utilisateur ferme l'application, le numéro est perdu. Avec TinyDB :

| Sans TinyDB | Avec TinyDB |
|-------------|-------------|
| Numéro oublié à chaque fermeture | Numéro mémorisé définitivement |
| L'utilisateur doit reconfigurer à chaque fois | Configuration faite une seule fois |

C'est comme un petit fichier de configuration sauvegardé sur le téléphone.

---

## Récapitulatif des blocs

| Bloc | Déclencheur | Action |
|------|-------------|--------|
| `when Btn_Config.Click` | Clic sur le bouton | Ouvre la boîte de dialogue |
| `when Notificateur.AfterTextInput` | Validation de la saisie | Traite la réponse |
| `if is empty responseText` | Saisie vide | Affiche une alerte |
| `set SMS_Envoi.PhoneNumber` | Saisie valide | Configure le numéro SMS |
| `TinyDB_Config.StoreValue` | Saisie valide | Sauvegarde le numéro |
| `Notificateur.ShowAlert` | Saisie valide | Confirme visuellement |

---

**Version :** 1.0  
**Date :** Janvier 2025  
**Auteur :** Votre établissement
