# Démarrer avec KiCad
The KiCad Team

---

## Table des matières

- Introduction à KiCad 9.0
- Téléchargez et installez KiCad
- Assistance
- Concepts de base et Workflow
- Workflow de conception PCB
- Tutoriel Partie 1 : Projet
- Tutoriel Partie 2 : Schéma
  - Configuration de la table de bibliothèques de symboles
  - Bases de l'éditeur de schéma
  - Configuration de la feuille de schéma
  - Ajout de symboles au schéma
  - Sélection et déplacement d'objets
  - Câblage du schéma
  - Annotation, propriétés des symboles et empreintes
  - Vérification des règles électriques
  - Nomenclature
- Tutoriel Partie 3 : Circuit imprimé
  - Bases de l'éditeur de PCB
  - Configuration du circuit et empilement
  - Import des modifications depuis le schéma
  - Dessin d'un contour de circuit
  - Placement des empreintes
  - Routage des pistes
  - Placement des zones de cuivre
  - Vérification des règles de conception
  - Visualiseur 3D
  - Sorties de fabrication
- Tutoriel Partie 4 : Symboles et empreintes personnalisés
  - Bases des bibliothèques et tables de bibliothèques
  - Création de nouvelles bibliothèques globales ou de projet
  - Création de nouveaux symboles
  - Création de nouvelles empreintes
  - Liaison des symboles, empreintes et modèles 3D
- Où aller ensuite
  - Plus de ressources d'apprentissage
  - Aidez à améliorer KiCad

---

## Copyright

Ce document est Copyright © 2010-2024 par ses contributeurs listés ci-dessous. Vous pouvez le distribuer et/ou le modifier selon les termes de la GNU General Public License (http://www.gnu.org/licenses/gpl.html), version 3 ou ultérieure, ou la licence Creative Commons Attribution (http://creativecommons.org/licenses/by/3.0/), version 3.0 ou ultérieure.

Toutes les marques apparaissant dans ce document appartiennent à leurs propriétaires respectifs.

### Contributeurs
Graham Keeth, Jon Evans, Glenn Peterson.

### Traduction
Pierre Beneteau <pierre.beneteau@univ-lyon1.fr>, 2015.
Martin d'Allens <martin.dallens@gmail.com>, 2015.
Marc Berlioux <marc.berlioux@gmail.com>, 2015-2016.
Francisco Dos Santos <f.dos.santos@free.fr>, 2020.

### Anciens contributeurs
David Jahshan, Phil Hutchinson, Fabrizio Tappero, Christina Jarron, Melroy van den Berg, Marc Berlioux.

### Retours

Le projet KiCad accueille les retours, rapports de bogues et suggestions liés au logiciel ou à sa documentation. Pour plus d'informations sur la manière de soumettre des retours ou de signaler un problème, veuillez consulter les instructions à https://www.kicad.org/help/report-an-issue/

### Version du logiciel et de la documentation

Ce manuel utilisateur est basé sur KiCad 9.0.7. Les fonctionnalités et l'apparence peuvent être différentes dans d'autres versions de KiCad.

Révision de la documentation : 79bdb77e.

---

## Introduction à KiCad 9.0

KiCad est une suite logicielle open-source pour créer des schémas de circuits électroniques, des circuits imprimés (PCB), et des descriptions de pièces associées. KiCad prend en charge un workflow de conception intégré dans lequel un schéma et le PCB correspondant sont conçus ensemble, ainsi que des workflows autonomes pour des utilisations spéciales.

KiCad inclut également plusieurs utilitaires pour aider à la conception de circuits et de PCB, notamment un calculateur PCB pour déterminer les propriétés électriques des structures de circuit, un visualiseur Gerber pour inspecter les fichiers de fabrication, un visualiseur 3D pour visualiser le PCB fini, et un simulateur SPICE intégré pour inspecter le comportement du circuit.

KiCad fonctionne sur tous les systèmes d'exploitation majeurs et une large gamme de matériel informatique. Il prend en charge les PCB avec jusqu'à 32 couches de cuivre et convient à la création de conceptions de toutes complexités. KiCad est développé par une équipe bénévole d'ingénieurs logiciels et électroniques du monde entier avec pour mission de créer un logiciel de conception électronique libre et open-source adapté aux concepteurs professionnels.

La dernière documentation pour KiCad est disponible sur https://docs.kicad.org. Ce document s'applique à KiCad version 9.0.

## Téléchargez et installez KiCad

KiCad fonctionne sur de nombreux systèmes d'exploitation, notamment Microsoft Windows, Apple macOS, et de nombreuses distributions Linux majeures.

Vous pouvez trouver les liens de téléchargement les plus à jour et les instructions d'installation sur https://www.kicad.org/download/. Ces instructions ne sont pas incluses dans ce manuel car elles peuvent changer au fil du temps avec la sortie de mises à jour des systèmes d'exploitation.

Si vous rencontrez des problèmes pour exécuter KiCad sur votre système, consultez la liste des problèmes connus liés au système et des solutions de contournement sur https://www.kicad.org/help/known-system-related-issues/.

**IMPORTANT**

Les versions stables de KiCad sont publiées périodiquement selon la politique de publication de versions stables de KiCad. De nouvelles fonctionnalités sont continuellement ajoutées à la branche de développement. Si vous souhaitez profiter de ces nouvelles fonctionnalités et aider en les testant, veuillez télécharger le dernier package de compilation nocturne pour votre plateforme. Les compilations nocturnes peuvent introduire des bogues tels que la corruption de fichiers, la génération de mauvais Gerbers, etc., mais l'objectif de l'équipe de développement KiCad est de maintenir la branche de développement aussi utilisable que possible pendant le développement de nouvelles fonctionnalités.

## Assistance

Si vous avez des idées, des remarques, des questions ou si vous avez besoin d'aide :

- Le forum utilisateur officiel de KiCad est un excellent endroit pour se connecter avec d'autres utilisateurs de KiCad et obtenir de l'aide.
- Rejoignez nos communautés sur Discord ou IRC pour des discussions en temps réel avec des utilisateurs et des développeurs.
- Consultez le site web KiCad pour des ressources d'apprentissage créées par la communauté KiCad.

---

## Concepts de base et Workflow

Le workflow typique dans KiCad consiste en deux tâches principales : dessiner un schéma et concevoir un circuit imprimé.

Le schéma est une représentation symbolique du circuit : quels composants sont utilisés et quelles connexions sont établies entre eux. Les symboles schématiques sont des représentations picturales de composants électroniques dans un schéma, tels qu'un zigzag ou un rectangle pour une résistance ou un triangle pour un amplificateur opérationnel. Le schéma contient des symboles pour chaque composant dans la conception, avec des fils connectant les broches dans les symboles. Le schéma est généralement dessiné en premier, avant de concevoir le circuit imprimé.

Le circuit imprimé est la réalisation physique du schéma, avec des empreintes de composants positionnées sur le circuit et des pistes de cuivre réalisant les connexions décrites dans le schéma. Les empreintes sont un ensemble de pastilles de cuivre qui correspondent aux broches d'un composant physique. Lorsque le circuit est fabriqué et assemblé, le composant sera soudé sur son empreinte correspondante sur le circuit imprimé.

KiCad dispose de fenêtres séparées pour dessiner le schéma ("Éditeur de schéma"), concevoir le circuit ("Éditeur de PCB"), et éditer les symboles et empreintes ("Éditeur de symboles" et "Éditeur d'empreintes"). KiCad est livré avec une grande bibliothèque de symboles et d'empreintes de haute qualité, contribués par les utilisateurs, mais il est également simple de créer de nouveaux symboles et empreintes ou de modifier des symboles et empreintes existants.

Enfin, il est important de comprendre que KiCad a un workflow basé sur les projets. Un projet KiCad est un dossier avec un fichier projet, un schéma, une conception de circuit, et optionnellement d'autres fichiers associés tels que des bibliothèques de symboles et d'empreintes, des données de simulation, des informations d'achat, etc. De nombreux paramètres liés au projet, y compris les classes de nets et les règles de conception, sont stockés au niveau du projet. L'ouverture d'un circuit en dehors de son projet associé peut entraîner des informations de conception manquantes, assurez-vous donc de conserver tous les fichiers associés à un projet ensemble.

---

## Workflow de conception PCB

Typiquement, le schéma est dessiné en premier. Cela signifie ajouter des symboles au schéma et dessiner les connexions entre eux. Des symboles personnalisés peuvent devoir être créés si des symboles appropriés ne sont pas déjà disponibles. À ce stade, les empreintes sont également sélectionnées pour chaque composant, avec des empreintes personnalisées créées si nécessaire. Lorsque le schéma est complet et que la conception a passé une vérification des règles électriques (ERC), les informations de conception dans le schéma sont transférées à l'éditeur de circuits et la conception commence.

Le schéma décrit quels composants sont dans la conception et comment ils sont connectés ; l'éditeur de circuits utilise ces informations pour faciliter la conception et prévenir les discordances entre le schéma et le PCB. Le processus de conception nécessite un placement soigneux de chaque empreinte sur le circuit imprimé. Après le placement des composants, des pistes de cuivre sont tracées entre les composants en fonction des connexions dans le schéma ainsi que d'autres considérations électriques, telles que la résistance des pistes, les exigences d'impédance contrôlée, la diaphonie, etc.

Souvent, le schéma devra être mis à jour après le début de la conception ; les modifications du schéma peuvent être facilement intégrées dans la conception du circuit. L'inverse peut souvent se produire : toute modification de conception effectuée dans la conception du circuit peut être renvoyée au schéma pour maintenir la cohérence entre les deux.

Lorsque la conception du circuit est terminée et que le circuit a passé la vérification des règles de conception (DRC), les sorties de fabrication sont générées afin que le circuit puisse être fabriqué par un fabricant de PCB.

---

## Tutoriel Partie 1 : Projet

La première chose à faire lors du démarrage d'une nouvelle conception est de créer un nouveau projet. L'ouverture de KiCad affichera le gestionnaire de projet. Cliquez sur Fichier → Nouveau projet, naviguez vers l'emplacement souhaité, et donnez un nom à votre projet, tel que getting-started. Assurez-vous que la case Créer un nouveau dossier pour le projet est cochée, puis cliquez sur Enregistrer. Cela créera vos fichiers projet dans un nouveau sous-dossier portant le même nom que votre projet.

À gauche, le volet Fichiers du projet liste les fichiers du nouveau projet. Il y a un fichier projet avec l'extension .kicad_pro, un fichier schéma avec l'extension .kicad_sch, et un fichier circuit avec l'extension .kicad_pcb. Tous ces fichiers partagent un nom avec votre projet.

Il peut également y avoir un répertoire -backups : KiCad créera automatiquement des sauvegardes de votre projet lorsque vous enregistrez, et optionnellement à intervalles de temps fixes. Les paramètres de sauvegarde sont configurables en allant dans Préférences → Préférences → Commun → Sauvegarde du projet.

**NOTE**

L'ouverture de la boîte de dialogue Préférences peut déclencher une boîte de dialogue de configuration de table de bibliothèques. Cette boîte de dialogue est expliquée ci-dessous.

**NOTE** Sur macOS, la boîte de dialogue Préférences se trouve dans le menu KiCad, pas le menu Préférences.

À droite de la fenêtre Projet, il y a des boutons pour lancer les différents outils que KiCad fournit. Le lancement de ces outils ouvrira automatiquement le fichier de conception associé (schéma ou PCB) du projet actuel.

Commencez par ouvrir l'Éditeur de schéma.

---

## Tutoriel Partie 2 : Schéma

### Configuration de la table de bibliothèques de symboles

La première fois que l'éditeur de schéma est ouvert, une boîte de dialogue apparaîtra demandant comment configurer la table de bibliothèques de symboles globale. La table de bibliothèques de symboles indique à KiCad quelles bibliothèques de symboles utiliser et où elles se trouvent.

Si vous avez installé les bibliothèques par défaut avec KiCad, ce qui est recommandé, sélectionnez l'option par défaut : Copier la table de bibliothèques de symboles globale par défaut (recommandé).

Si KiCad ne peut pas trouver les bibliothèques dans leur emplacement d'installation attendu, cette option sera désactivée. Dans ce cas, l'utilisateur doit choisir la deuxième option, Copier une table de bibliothèques de symboles globale personnalisée. Cliquez sur le bouton dossier en bas, et naviguez vers l'emplacement indiqué ci-dessous. Sélectionnez le fichier sym-lib-table.

L'emplacement des fichiers de table de bibliothèques par défaut dépend du système d'exploitation et peut varier en fonction de l'emplacement d'installation. Voici les valeurs par défaut pour chaque système d'exploitation :

- Windows : C:\Program Files\KiCad\9.0\share\kicad\template\
- Linux : /usr/share/kicad/template/
- macOS : /Applications/KiCad/KiCad.app/Contents/SharedSupport/template/

### Bases de l'éditeur de schéma

Pour faire un panoramique autour du schéma, cliquez et faites glisser avec le bouton central de la souris ou le bouton droit de la souris. Zoomez avec la molette de la souris ou F1 et F2. Les utilisateurs d'ordinateurs portables peuvent trouver utile de modifier les contrôles de la souris pour être mieux adaptés à un pavé tactile ; les contrôles de la souris sont configurables dans Préférences → Préférences... → Souris et pavé tactile.

**NOTE** Sur macOS, la boîte de dialogue Préférences se trouve dans le menu KiCad, pas le menu Préférences.

Par défaut, KiCad active un paramètre de souris appelé Centrer et déplacer le curseur lors du zoom. Lorsque cette fonctionnalité est activée, le curseur de la souris est automatiquement déplacé au centre de l'écran lorsque l'utilisateur zoome. Cela maintient la région zoomée centrée en tout temps. Cette fonctionnalité est inhabituelle, mais de nombreux utilisateurs la trouvent utile une fois qu'ils s'y sont habitués. Essayez de zoomer avec le curseur de la souris dans différentes zones du canevas. Si le comportement de zoom par défaut est inconfortable, désactivez la fonctionnalité dans les préférences Souris et pavé tactile.

La barre d'outils sur le côté gauche de l'écran de l'éditeur de schéma contient des paramètres d'affichage de base. La barre d'outils sur le côté droit de l'écran contient des outils pour éditer le schéma.

La plupart des outils dans KiCad ont soit des raccourcis clavier par défaut assignés, soit peuvent avoir des raccourcis clavier personnalisés assignés. Pour voir tous les raccourcis clavier, allez dans Aide → Lister les raccourcis clavier.... Les raccourcis clavier peuvent être modifiés dans le panneau Raccourcis clavier de la boîte de dialogue Préférences.

### Configuration de la feuille de schéma

Avant de dessiner quoi que ce soit dans le schéma, configurez la feuille de schéma elle-même. Cliquez sur Fichier → Mise en page. Donnez un titre et une date au schéma, et changez la taille du papier si désiré.

### Ajout de symboles au schéma

Commencez à créer le circuit en ajoutant quelques symboles au schéma. Ouvrez la boîte de dialogue Choisir un symbole en cliquant sur le bouton Ajouter des symboles sur le côté droit de la fenêtre ou en appuyant sur A.

Cette action déclenchera la boîte de dialogue Configuration de la table de bibliothèques d'empreintes si elle n'a pas déjà été déclenchée. Cette boîte de dialogue est équivalente à la boîte de dialogue Configuration de la table de bibliothèques de symboles expliquée précédemment, mais pour les empreintes au lieu des symboles.

Encore une fois, sélectionnez l'option par défaut : Copier la table de bibliothèques d'empreintes globale par défaut (recommandé). Si cette option est désactivée, sélectionnez la deuxième option, Copier une table de bibliothèques d'empreintes globale personnalisée. Cliquez sur le bouton dossier en bas, et naviguez vers l'emplacement indiqué dans les instructions de configuration de la table de bibliothèques de symboles. Sélectionnez le fichier fp-lib-table et cliquez sur OK.

La boîte de dialogue Choisir un symbole liste les bibliothèques de symboles disponibles et les symboles de composants qu'elles contiennent. Les appareils de base comme les composants passifs, les diodes et autres symboles génériques se trouvent dans la bibliothèque Device. Des appareils spécifiques, tels qu'une LED particulière, peuvent être trouvés dans d'autres bibliothèques.

Faites défiler jusqu'à la bibliothèque Device, développez-la, et sélectionnez le symbole LED. Cliquez sur OK, et cliquez à nouveau pour placer le symbole dans le schéma.

Ensuite, ajoutez une résistance de limitation de courant. Retournez au sélecteur de symboles, mais cette fois essayez de rechercher une résistance en entrant R dans la boîte de filtre en haut. Encore une fois, elle se trouve dans la bibliothèque Device. Le composant R est un symbole de résistance rectangulaire de style IEC. Un symbole R_US est également disponible pour les utilisateurs qui préfèrent le symbole en zigzag de style ANSI. Sélectionnez un symbole de résistance et ajoutez-le au schéma.

Enfin, ajoutez une batterie pour alimenter la LED. La bibliothèque Device a un symbole Battery_Cell approprié.

### Sélection et déplacement d'objets

Ensuite, positionnez les symboles correctement les uns par rapport aux autres, comme montré dans la capture d'écran. Vous le ferez en sélectionnant chaque symbole, puis en le déplaçant et en le faisant pivoter.

Dans KiCad, les objets sont sélectionnés en cliquant dessus pendant que l'outil de sélection est actif. L'outil de sélection est l'outil par défaut lorsqu'aucun autre outil n'est actif, vous pouvez donc entrer dans l'outil de sélection en quittant tout outil actif (Esc) ou en cliquant sur le bouton dans la barre d'outils de droite.

Des objets supplémentaires peuvent être ajoutés à la sélection avec Shift+clic, ou retirés avec Ctrl+Shift+clic (macOS : Cmd+Shift+clic). Vous pouvez basculer l'état de sélection d'un élément avec Ctrl+clic (macOS : Cmd+clic).

La sélection par glissement est également possible ; glisser de gauche à droite sélectionne les objets qui sont entièrement enclos par le rectangle de sélection, tandis que glisser de droite à gauche sélectionne également les objets qui sont partiellement enclos par le rectangle de sélection. Shift, Ctrl+Shift (Cmd+Shift), et Ctrl (Cmd) peuvent également être utilisés avec la sélection par glissement pour ajouter, soustraire ou basculer de la sélection, respectivement.

Notez qu'il est possible de sélectionner un symbole entier (en cliquant sur la forme du symbole elle-même) ou de sélectionner un champ de texte dans le symbole sans sélectionner le reste du symbole (en cliquant sur le texte). Lorsque seul un champ de texte est sélectionné, toute action effectuée agira uniquement sur le texte sélectionné et non sur le reste du symbole.

Les objets sélectionnés sont déplacés en appuyant sur M et pivotés en appuyant sur R. Le raccourci G (glisser) peut également être utilisé pour déplacer des objets. Pour déplacer des symboles non connectés, G et M se comportent de manière identique, mais pour les symboles avec des fils attachés, G déplace le symbole et maintient les fils attachés, tandis que M déplace le symbole et laisse les fils derrière. Les objets sélectionnés peuvent être supprimés avec la touche Del.

### Câblage du schéma

Les broches du symbole ont toutes de petits cercles sur elles, indiquant qu'elles ne sont pas connectées. Corrigez cela en dessinant des fils entre les broches du symbole comme montré dans la capture d'écran. Cliquez sur le bouton Ajouter un fil dans la barre d'outils de droite ou utilisez le raccourci W. Cliquez et relâchez pour commencer à dessiner un fil, et terminez le dessin du fil en cliquant sur une broche de symbole ou en double-cliquant n'importe où. Appuyer sur Échap annulera le dessin du fil.

Une autre méthode pratique pour dessiner des fils est de survoler une broche non connectée. Le curseur de la souris changera pour indiquer qu'un fil peut être dessiné à partir de cet emplacement. Cliquer sur la broche commencera alors automatiquement à dessiner un fil.

Ensuite, ajoutez des symboles d'alimentation et de masse au schéma. Bien que cela ne soit pas strictement nécessaire dans un schéma aussi simple, cela facilite la compréhension des grands schémas.

Un certain nombre de symboles d'alimentation et de masse sont disponibles dans la bibliothèque de symboles Power. Cependant, il existe un raccourci pour ajouter ces symboles : cliquez sur le bouton Ajouter un symbole d'alimentation ou utilisez le raccourci P. Cela affiche la boîte de dialogue Choisir un symbole, mais n'affiche que les bibliothèques de symboles qui contiennent des symboles d'alimentation.

Ajoutez un symbole VCC et un symbole GND puis connectez-les au circuit avec des fils.

Enfin, ajoutez une étiquette au fil entre la LED et la résistance. Encore une fois, cela peut ne pas être nécessaire dans un circuit simple, mais c'est une bonne pratique d'étiqueter les nets importants. Cliquez sur le bouton Dessiner des étiquettes de net dans la barre d'outils de droite (L), tapez un nom d'étiquette (led), et placez l'étiquette dans le schéma de sorte que le point d'attache carré chevauche le fil. Faites pivoter et alignez l'étiquette si nécessaire.

Notez que les étiquettes et les symboles d'alimentation avec le même nom sont connectés ensemble. Un autre symbole GND ou un fil étiqueté led sur cette page de schéma serait court-circuité avec celui existant, même sans fils les connectant visuellement.

### Annotation, propriétés des symboles et empreintes

#### Annotation

Chaque symbole a besoin d'un désignateur de référence unique qui lui soit assigné. Ce processus est également connu sous le nom d'annotation.

Par défaut, les symboles sont automatiquement annotés lorsqu'ils sont ajoutés au schéma. L'annotation automatique peut être activée ou désactivée en utilisant le bouton dans la barre d'outils de gauche.

Bien que cela ne soit pas nécessaire pour ce guide, les symboles peuvent être annotés manuellement ou ré-annotés en utilisant le bouton Remplir les désignateurs de référence des symboles de schéma dans la barre d'outils du haut.

#### Propriétés des symboles

Ensuite, remplissez les valeurs pour chaque composant. Sélectionnez la LED, faites un clic droit, et sélectionnez Propriétés... (E). Ce projet utilisera une LED rouge, donc changez le champ Valeur pour être red. Dans un vrai projet, il serait peut-être mieux d'écrire ici le numéro de pièce du fabricant de la LED. Notez qu'il est possible d'éditer les désignateurs de référence individuellement dans les propriétés de chaque symbole.

Ce projet utilisera une pile bouton au lithium de 3V, donc changez le champ Valeur de BT1 en 3V. Changez la valeur de la résistance en 1k.

#### Attribution d'empreinte

Enfin, attribuez une empreinte à chaque composant. Cela définit comment chaque composant se fixera au PCB. Certains symboles sont livrés avec des empreintes pré-assignées, mais pour de nombreux composants il existe plusieurs empreintes possibles, donc l'utilisateur doit sélectionner celle appropriée.

Il existe plusieurs façons d'attribuer des empreintes, mais une méthode pratique consiste à utiliser l'outil d'attribution d'empreintes en cliquant sur le bouton dans la barre d'outils du haut.

Le volet gauche de cette fenêtre liste les bibliothèques d'empreintes disponibles. Le volet central montre les symboles dans le schéma. Tous ces symboles recevront des empreintes qui leur seront attribuées. Le volet droit montre les empreintes qui peuvent être choisies pour le symbole sélectionné dans le volet central. Pour attribuer une empreinte à un symbole, sélectionnez le symbole dans le volet central et double-cliquez sur l'empreinte désirée dans le volet droit. Vous pouvez prévisualiser une empreinte en faisant un clic droit sur le nom de l'empreinte et en sélectionnant Voir l'empreinte sélectionnée.

De nombreuses empreintes sont incluses avec KiCad, donc l'outil d'attribution d'empreintes offre plusieurs façons de filtrer les empreintes qui ne sont pas pertinentes pour le symbole en question.

- Le bouton le plus à gauche active les filtres qui peuvent être définis dans chaque symbole. Par exemple, un symbole d'amplificateur opérationnel pourrait définir des filtres qui ne montrent que les empreintes SOIC et DIP. Parfois ces filtres prédéfinis sont manquants ou trop restrictifs, il peut donc être utile de désactiver ce filtre dans certaines situations.

- Le bouton du milieu filtre par nombre de broches, de sorte que seules les empreintes à 8 pastilles sont montrées pour les symboles à 8 broches. Ce filtre est presque toujours utile.

- Le bouton de droite filtre par bibliothèque sélectionnée. Les bibliothèques sont sélectionnées dans le volet gauche ; les empreintes qui ne sont pas dans la bibliothèque sélectionnée seront filtrées. Ce filtre est utile tant que l'on sait quelle bibliothèque contient la bonne empreinte. Il est souvent préférable d'utiliser ce filtre ou les filtres de symboles, mais pas les deux.

- La zone de texte filtre les empreintes qui ne correspondent pas au texte dans la boîte. Ce filtre est désactivé lorsque la boîte est vide.

En utilisant les filtres, trouvez chacune des empreintes montrées dans la colonne centrale de la capture d'écran ci-dessus. Les empreintes pour chaque symbole sont également listées dans le tableau ci-dessous. Attribuez chaque empreinte à un symbole en sélectionnant le symbole dans la colonne centrale puis en double-cliquant sur l'empreinte appropriée dans la colonne de droite. Une fois que toutes les empreintes ont été attribuées, cliquez sur OK.

| Référence du symbole | Empreinte à attribuer |
|----------------------|-----------------------|
| BT1 | Battery:BatteryHolder_Keystone_1058_1x2032 |
| D1 | LED_THT:LED_D5.0mm |
| R1 | Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal |

Il existe d'autres façons d'attribuer des empreintes ; une façon est à travers la fenêtre de propriétés du symbole. Pour plus d'informations sur l'attribution d'empreintes, consultez le manuel.

### Vérification des règles électriques

La dernière chose à faire dans le schéma est de vérifier les erreurs électriques. La vérification des règles électriques (ERC) de KiCad ne peut pas s'assurer que la conception dans le schéma fonctionnera, mais elle peut vérifier certains problèmes de connexion courants tels que des broches non connectées, deux sorties d'alimentation court-circuitées ensemble, ou une entrée d'alimentation qui n'est alimentée par rien. Elle vérifie également d'autres erreurs comme des symboles qui ne sont pas annotés et des fautes de frappe dans les étiquettes de net. Pour voir la liste complète des règles électriques et pour ajuster leur sévérité, allez dans Fichier → Configuration du schéma... → Règles électriques → Sévérité des violations. C'est une bonne idée d'exécuter l'ERC avant de commencer la conception.

Exécutez une vérification des règles électriques en cliquant sur le bouton ERC dans la barre d'outils du haut puis en cliquant sur Exécuter l'ERC.

Même dans ce schéma simple, KiCad a trouvé deux erreurs potentielles. Les erreurs sont listées dans la fenêtre ERC, et des flèches pointent vers les emplacements de violation dans le schéma. Sélectionner une violation dans la fenêtre ERC met en surbrillance la flèche correspondante.

Vous pouvez exclure des violations individuelles ou ignorer des classes entières de violations en faisant un clic droit sur chaque message d'erreur. Cependant, il vaut généralement la peine de traiter les violations, même si elles ne sont pas des erreurs de conception réelles, afin d'obtenir un rapport ERC propre et d'éviter de manquer de vrais problèmes.

Dans ce cas, KiCad signale "Broche d'alimentation d'entrée non pilotée par des broches de sortie d'alimentation" pour les nets VCC et GND. C'est une erreur ERC KiCad courante. Les symboles d'alimentation sont configurés pour nécessiter une broche de sortie d'alimentation, telle que la sortie d'un régulateur de tension, sur le même net ; sinon KiCad pense que le net n'est pas piloté. Pour un humain, il est évident que VCC et GND sont pilotés par la batterie, mais il est nécessaire de le montrer explicitement dans le schéma.

Il existe un symbole spécial PWR_FLAG dans la bibliothèque de symboles Power qui est utilisé pour résoudre ce problème en indiquant à KiCad que les nets sont effectivement pilotés. Ajoutez ce symbole aux nets VCC et GND et réexécutez l'ERC. Lorsque l'ERC passe sans aucune violation, le schéma est complet.

### Nomenclature

Une dernière étape optionnelle consiste à générer une nomenclature listant tous les composants utilisés dans le projet. Cliquez sur Outils → Générer la nomenclature....

KiCad dispose d'une interface graphique pour l'export de nomenclature. Vous pouvez configurer quelles métadonnées de symboles seront exportées, et comment les symboles sont regroupés, dans l'onglet Édition, et configurer le format de sortie dans l'onglet Export.

Pour l'instant, les paramètres par défaut devraient convenir, mais vous pouvez voir un aperçu brut de ce qui sera exporté dans le volet de prévisualisation. Spécifiez un fichier de sortie dans l'onglet Export, puis appuyez sur le bouton Exporter.

La nomenclature devrait ressembler à l'image ci-dessous lorsqu'elle est ouverte dans un tableur.

---

## Tutoriel Partie 3 : Circuit imprimé

Une fois le schéma terminé, retournez à la fenêtre Projet et ouvrez l'Éditeur de PCB, soit en cliquant sur le bouton Éditeur de PCB soit en ouvrant le fichier circuit.

### Bases de l'éditeur de PCB

La navigation dans l'Éditeur de PCB est la même que dans l'éditeur de schéma : faites un panoramique en glissant avec le bouton central de la souris ou le bouton droit de la souris, et zoomez avec la molette de défilement ou F1 / F2.

La principale partie de l'Éditeur de PCB est un canevas où le circuit sera conçu. La barre d'outils sur le côté gauche dispose de diverses options d'affichage pour le circuit, notamment les unités et les bascules pour le mode contour/rempli pour les pistes, vias, pastilles et zones. La barre d'outils juste à droite du canevas contient des outils pour concevoir le PCB.

**NOTE**

Certains boutons de la barre d'outils de droite ont un petit triangle dans le coin inférieur droit. Le triangle indique que le bouton dispose d'une palette extensible contenant plusieurs outils connexes, par exemple différents types de cotes. Pour sélectionner un outil alternatif, cliquez et maintenez sur le bouton jusqu'à ce que la palette apparaisse, puis cliquez sur l'outil alternatif. Une autre façon d'utiliser les palettes est de cliquer sur le bouton et de glisser vers la gauche jusqu'à ce que la palette apparaisse, puis de relâcher le bouton de la souris lorsque l'outil désiré est en surbrillance.

À l'extrême droite se trouve le panneau Apparence et le filtre de sélection. Le panneau Apparence est utilisé pour changer la visibilité, les couleurs et l'opacité des couches PCB, des objets et des nets. La couche active est changée en cliquant sur le nom d'une couche.

Sous le panneau Apparence se trouve le filtre de sélection, qui active et désactive la sélection de divers types d'objets PCB. Ceci est utile pour sélectionner des éléments spécifiques dans une conception encombrée.

### Configuration du circuit et empilement

Avant de concevoir le circuit, définissez la taille de la page et ajoutez des informations au cartouche. Cliquez sur Fichier → Mise en page..., puis choisissez une taille de papier appropriée et entrez une date, une révision et un titre.

Ensuite, allez dans Fichier → Configuration du circuit... pour définir comment le PCB sera fabriqué. Les paramètres les plus importants sont l'empilement, c'est-à-dire quelles couches de cuivre et diélectriques le PCB aura (et leurs épaisseurs), et les règles de conception, par exemple les tailles et espacements pour les pistes et vias.

Pour définir l'empilement, ouvrez la page Configuration du circuit → Empilement du circuit → Empilement physique de la fenêtre Configuration du circuit. Pour ce guide, laissez le nombre de couches de cuivre à 2, mais des projets plus compliqués pourraient nécessiter plus de couches.

Ensuite, allez à la page Règles de conception → Contraintes. Les paramètres sur cette page spécifient les règles de conception prioritaires pour tout dans la conception du circuit. Pour ce guide, les valeurs par défaut conviennent. Cependant, pour un vrai projet, celles-ci devraient être définies selon les capacités du fabricant de PCB afin que la conception du PCB soit fabricable.

Enfin, ouvrez la page Règles de conception → Classes de nets. Une classe de nets est un ensemble de règles de conception associées à un groupe spécifique de nets. Cette page liste les règles de conception pour chaque classe de nets dans la conception et permet d'attribuer des nets à chaque classe de nets (les nets peuvent également être attribués à des classes de nets dans l'éditeur de schéma).

Dans cette conception, aucune classe de nets n'est spécifiée, donc tous les nets appartiendront à la classe de nets Default. Les règles de conception par défaut pour cette classe de nets sont acceptables pour ce projet, mais d'autres conceptions peuvent avoir plusieurs classes de nets, chacune avec des règles de conception différentes. Par exemple, un circuit pourrait avoir une classe de nets High Current avec des pistes larges, ou une classe de nets 50 ohm avec des règles de largeur et d'espacement spécifiques pour des pistes d'impédance contrôlée de 50 ohms.

### Import des modifications depuis le schéma

Le schéma est complet, mais il n'y a pas encore de composants dans la conception. Pour importer les données de conception du schéma dans la conception, cliquez sur Outils → Mettre à jour le PCB depuis le schéma..., ou appuyez sur F8. Il y a aussi un bouton dans la barre d'outils du haut.

Lisez les messages dans la fenêtre Modifications à appliquer, qui dira que les trois composants du schéma seront ajoutés au circuit. Cliquez sur Mettre à jour le PCB, Fermer, et cliquez sur le canevas pour placer les trois empreintes. L'emplacement de chaque empreinte par rapport aux autres sera changé plus tard.

Dans KiCad, la mise à jour du PCB avec les modifications dans le schéma est un processus manuel : le concepteur décide quand il est approprié de mettre à jour le PCB avec les modifications dans le schéma. Chaque fois que le schéma est édité, le concepteur doit utiliser l'outil Mettre à jour le PCB depuis le schéma pour maintenir le schéma et la conception en synchronisation.

### Dessin d'un contour de circuit

Maintenant les trois composants ont été placés, mais le circuit lui-même n'a pas été défini. Le circuit est défini en dessinant un contour de circuit sur la couche Edge.Cuts.

Il est souvent utile de dessiner le contour du circuit avec une grille grossière, ce qui facilite l'obtention de nombres ronds pour la taille du circuit. Changez pour une grille grossière en sélectionnant 1mm dans le menu déroulant Grille au-dessus du canevas.

Pour dessiner sur la couche Edge.Cuts, cliquez sur Edge.Cuts dans l'onglet Couches du panneau Apparence à droite. Choisissez l'outil rectangle dans la barre d'outils de droite, cliquez sur le canevas pour placer le premier coin, puis cliquez à nouveau pour placer le coin opposé de sorte que le rectangle entoure approximativement les trois empreintes. Les autres outils graphiques (ligne, arc, cercle, polygone, bézier, ou une combinaison d'entre eux) pourraient également être utilisés pour définir le contour du circuit ; la seule exigence est que le contour soit une forme fermée unique qui ne se croise pas elle-même.

### Placement des empreintes

L'étape suivante du processus de conception est d'arranger les empreintes sur le circuit. En général, il y a plusieurs considérations pour positionner les empreintes :

- Certaines empreintes peuvent avoir des exigences exactes pour leurs emplacements, tels que les connecteurs, indicateurs, ou boutons et interrupteurs.
- Certains composants peuvent devoir être placés selon des considérations électriques. Les condensateurs de découplage doivent être proches des broches d'alimentation du CI associé et les composants analogiques sensibles doivent être loin des interférences numériques.
- Presque tous les composants ont un "Courtyard" (ou deux si Front et Back sont tous deux définis). Généralement les courtyards ne doivent pas se croiser.
- Sinon, les composants doivent être positionnés pour faciliter le routage. Les composants connectés doivent généralement être proches les uns des autres, et arrangés pour minimiser la complexité de routage. Le chevelu (les lignes fines indiquant les connexions entre les pastilles) est utile pour déterminer comment mieux positionner les empreintes par rapport aux autres empreintes.

Pour ce guide, le seul objectif de placement est de rendre le processus de routage aussi simple que possible.

Commencez par déplacer le support de batterie BT1 sur le côté arrière du circuit. Cliquez dessus pour le sélectionner, puis appuyez sur M pour le déplacer. Appuyez sur F pour le retourner sur le côté opposé ; il apparaît maintenant en miroir et ses pastilles ont changé de rouge à bleu.

Toutes les couches PCB sont vues du côté avant du circuit. Les empreintes au fond du circuit sont donc à l'envers et apparaissent en miroir.

Chaque couche PCB a une couleur unique, qui est montrée par les échantillons dans l'onglet Couches du panneau Apparence. Dans le schéma de couleurs par défaut, les éléments sur la couche F.Cu (Cuivre avant) sont rouges, tandis que les éléments sur B.Cu (Cuivre arrière) sont bleus.

Maintenant placez les deux autres composants. Un par un, sélectionnez chaque composant, puis déplacez-le et faites-le pivoter avec M et R. Regardez les lignes de chevelu entre chaque pastille pour choisir l'arrangement le plus simple des composants ; un bon arrangement laissera les lignes non enchevêtrées. Un arrangement possible est montré dans la capture d'écran ci-dessous.

### Routage des pistes

Avec les composants en place, il est temps de connecter les pastilles avec des pistes de cuivre.

La première piste sera dessinée sur le devant du circuit, donc changez la couche active vers F.Cu dans l'onglet Couches du panneau Apparence.

Cliquez sur Router les pistes dans la barre d'outils de droite ou appuyez sur X. Cliquez sur la pastille led de D1 et relâchez le bouton de la souris. La ligne de chevelu indique qu'il y a une connexion non routée vers la pastille led de R1, donc cliquez sur cette pastille pour dessiner une piste connectant les deux pastilles. Cliquer sur la deuxième pastille termine la piste. La ligne de chevelu entre les broches led n'est plus dessinée car la connexion a été établie en cuivre.

Maintenant dessinez une piste entre les pastilles GND de BT1 et D1, en commençant par la pastille BT1 à l'arrière du circuit. Notez que la couche active a automatiquement changé vers B.Cu après avoir cliqué sur la pastille BT1. Cliquez sur la pastille D1 pour terminer la piste.

Alors que BT1 a des pastilles montées en surface qui ne sont qu'au fond du circuit, D1 a des pastilles traversantes qui peuvent se connecter à des pistes à la fois sur le devant et à l'arrière. Les pastilles traversantes sont une façon de faire une connexion entre plusieurs couches. Dans ce cas, D1 est un composant sur le côté avant du circuit, mais ses pastilles traversantes sont utilisées pour se connecter à une piste sur le côté arrière du circuit.

Une autre façon de faire une connexion à travers les couches est avec un via. Commencez à router à la pastille VCC de BT1 à l'arrière du circuit. Appuyez sur V et cliquez à mi-chemin entre BT1 et R1 pour insérer un via, ce qui change également la couche active vers F.Cu. Terminez la piste sur le dessus du circuit en cliquant sur la pastille VCC de R1.

À ce stade, toutes les connexions sont routées. Cela peut être confirmé en regardant l'écran d'état dans le coin inférieur gauche de la fenêtre, où le nombre de nets non routés est donné comme 0.

### Placement des zones de cuivre

Les zones de cuivre sont des régions de cuivre avec un net associé. Les zones se connectent automatiquement aux objets de cuivre appartenant au même net et évitent les objets appartenant à d'autres nets. Les zones sont souvent utilisées pour les connexions de masse et d'alimentation car elles fournissent une connexion d'impédance plus faible que les pistes.

Ajoutez une zone GND sur le bas du circuit en basculant vers la couche de cuivre inférieure et en cliquant sur le bouton Ajouter une zone remplie dans la barre d'outils de droite. Cliquez sur le PCB pour placer le premier coin de la zone.

Dans la boîte de dialogue Propriétés de la zone de cuivre qui apparaît, sélectionnez le net GND et assurez-vous que la couche B.Cu est sélectionnée. Cliquez sur OK, puis cliquez pour placer les trois autres coins de la zone. Double-cliquez lors du placement du dernier coin pour terminer la zone.

Le contour de la zone est affiché sur le canevas, mais la zone n'est pas encore remplie — il n'y a pas de cuivre dans la zone, et donc la zone ne fait aucune connexion électrique. Remplissez la zone avec Édition → Remplir toutes les zones (B).

Le cuivre a été ajouté à la zone, mais il ne se connecte pas aux pastilles ou pistes VCC ou led, et est découpé par le bord du circuit. Il chevauche la piste GND dessinée précédemment, et il se connecte aux pastilles GND à travers des pistes fines. Ce sont des reliefs thermiques, qui rendent les pastilles plus faciles à souder. Les reliefs thermiques et d'autres paramètres de zone peuvent être modifiés dans la boîte de dialogue de propriétés de la zone.

Dans KiCad, les zones ne sont pas remplies automatiquement lorsqu'elles sont d'abord dessinées ou modifiées, ou lorsque des empreintes à l'intérieur d'elles sont déplacées. Les zones sont reremplies en les remplissant manuellement et lors de l'exécution du DRC. Assurez-vous que les remplissages de zone sont à jour avant de générer les sorties de fabrication.

Parfois, les zones remplies peuvent rendre difficile la visualisation d'autres objets dans une conception de circuit encombrée. Les zones peuvent être masquées sauf leurs contours en utilisant le bouton Montrer uniquement les contours de zone dans la barre d'outils de gauche. Les zones conservent leur état rempli lorsque seuls leurs contours sont montrés — masquer un remplissage de zone n'est pas la même chose que le déremplir.

Les zones peuvent également être rendues transparentes en utilisant le panneau Apparence, et les couches inactives peuvent également être masquées ou atténuées en utilisant les Options d'affichage des couches dans le panneau Apparence.

### Vérification des règles de conception

La vérification des règles de conception est l'équivalent de la vérification des règles électriques pour le schéma dans la disposition. Le DRC recherche des erreurs de conception comme des discordances entre le schéma et la disposition, des régions de cuivre qui ont un espacement insuffisant ou qui sont court-circuitées ensemble, et des pistes qui ne se connectent à rien. Vous pouvez également écrire des règles DRC personnalisées. Pour voir la liste complète des règles de conception qui sont vérifiées et pour ajuster leur sévérité, allez dans Fichier → Configuration du circuit... → Règles de conception → Sévérité des violations. Il est fortement conseillé d'exécuter le DRC et de corriger toutes les erreurs avant de générer les sorties de fabrication.

Exécutez une vérification DRC avec Inspecter → Vérificateur de règles de conception, ou utilisez le bouton dans la barre d'outils du haut. Cliquez sur Exécuter le DRC. Lorsque les vérifications sont terminées, aucune erreur ou avertissement ne devrait être signalé. Fermez la fenêtre DRC.

Maintenant causez intentionnellement une erreur DRC en déplaçant l'empreinte de la résistance pour chevaucher la zone remplie. Utilisez D (Glisser) pour déplacer légèrement l'empreinte de la résistance tout en gardant les pistes attachées à ses pastilles. Cela crée une violation d'espacement car les pastilles VCC et led de la résistance sont court-circuitées vers le remplissage de zone GND. Ordinairement cela serait corrigé en reremplissant la zone, mais ne reremplissez pas encore la zone.

Exécutez à nouveau le DRC, mais assurez-vous de décocher la case Reremplir toutes les zones avant d'effectuer le DRC. Le DRC signale 6 violations : pour chaque pastille de R1, il y a une violation d'espacement entre la pastille et la zone, une autre violation d'espacement entre le trou traversant de la pastille et la zone, et une troisième violation où l'ouverture de masque de soudure de la pastille expose le cuivre de deux nets différents (le remplissage GND et la piste connectée à la pastille). Des flèches pointent vers chaque violation dans le canevas. Cliquer sur chaque message de violation zoome sur la violation respective.

Fermez la boîte de dialogue DRC, appuyez sur B pour reremplir la zone, et réexécutez le DRC. Alternativement, cochez la case Reremplir toutes les zones avant d'effectuer le DRC et réexécutez le DRC. Toutes les violations sont corrigées.

### Visualiseur 3D

KiCad offre un visualiseur 3D qui est utile pour inspecter le PCB. Ouvrez le visualiseur 3D avec Vue → Visualiseur 3D.

Faites un panoramique en glissant avec le bouton central de la souris, et orbitez en glissant avec le bouton gauche de la souris. Orbitez autour du PCB pour voir la LED et la résistance sur le dessus, et le support de batterie sur le dessous.

Un mode de ray-tracing est disponible, qui est plus lent mais offre un rendu plus précis. Basculez vers le mode de ray-tracing avec Préférences → Ray-tracing.

Beaucoup des empreintes de la bibliothèque de KiCad sont livrées avec des modèles 3D, y compris toutes les empreintes utilisées dans ce guide. Certaines empreintes ne sont pas livrées avec des modèles 3D, mais les utilisateurs peuvent ajouter les leurs.

### Sorties de fabrication

Avec la conception du circuit terminée, l'étape finale est de générer les sorties de fabrication afin que le circuit puisse être fabriqué.

Ouvrez la boîte de dialogue Tracer avec Fichier → Tracer.... Cette boîte de dialogue peut tracer la conception dans plusieurs formats, mais Gerber est généralement le bon format pour commander auprès d'un fabricant de PCB.

Spécifiez un répertoire de sortie afin que les fichiers tracés soient collectés dans un dossier. Sinon, les paramètres par défaut conviennent, mais assurez-vous que toutes les couches nécessaires sont cochées : incluez les couches de cuivre (*.Cu), le contour du circuit (Edge.Cuts), le masque de soudure (*.Mask), et la sérigraphie (*.Silkscreen). Les couches de pâte (*.Paste) sont utiles pour fabriquer des pochoirs de pâte à souder. Les couches Adhésif (*.Adhesive) ne sont nécessaires que si des composants seront collés au circuit pendant l'assemblage. D'autres couches peuvent être utiles à tracer, mais ne sont généralement pas nécessaires pour la fabrication de PCB.

Cliquez sur Tracer pour générer les fichiers Gerber. Cliquez également sur Générer les fichiers de perçage... puis sur Générer le fichier de perçage pour créer des fichiers spécifiant l'emplacement de tous les trous qui seront percés dans le circuit. Enfin, fermez la boîte de dialogue Tracer.

La conception est terminée.

---

## Tutoriel Partie 4 : Symboles et empreintes personnalisés

Le circuit serait amélioré en ajoutant un interrupteur pour allumer et éteindre la LED. Le processus pour ajouter cet interrupteur nécessitera de créer une nouvelle bibliothèque de symboles et d'empreintes, de dessiner un symbole d'interrupteur, et de créer une empreinte pour l'interrupteur.

L'interrupteur spécifique qui sera utilisé dans ce guide est le NKK M2011S3A1W03, un interrupteur à bascule SPST. De nombreux autres interrupteurs pourraient être utilisés, mais la numérotation des broches et les dimensions de l'empreinte pourraient nécessiter des ajustements.

### Bases des bibliothèques et tables de bibliothèques

Les symboles et empreintes sont organisés en bibliothèques. Une bibliothèque peut contenir des symboles ou des empreintes, mais pas les deux.

KiCad garde trace des bibliothèques de symboles et d'empreintes de l'utilisateur dans la table de bibliothèques de symboles et la table de bibliothèques d'empreintes, respectivement. Chaque table de bibliothèques est une liste de noms de bibliothèques et de l'emplacement où chaque bibliothèque existe sur le disque.

En plus des tables de bibliothèques de symboles et d'empreintes globales, il existe également des tables de bibliothèques de projet pour les symboles et les empreintes. Les symboles et empreintes qui sont ajoutés aux tables globales sont disponibles dans tous les projets, tandis que les symboles et empreintes dans les tables spécifiques au projet ne sont disponibles que pour ce projet spécifique. Les utilisateurs peuvent ajouter leurs propres bibliothèques aux tables de bibliothèques globales ou aux tables spécifiques au projet.

Les tables de bibliothèques de symboles peuvent être visualisées ou éditées avec Préférences → Gérer les bibliothèques de symboles... dans les fenêtres Éditeur de schéma ou Éditeur de symboles. Les tables de bibliothèques d'empreintes peuvent être visualisées ou éditées avec Préférences → Gérer les bibliothèques d'empreintes... dans l'Éditeur de circuits ou l'Éditeur d'empreintes. Les deux tables de bibliothèques peuvent également être accédées depuis le gestionnaire de projet.

Souvent, les chemins vers les bibliothèques sont définis avec des variables de substitution de chemin. Cela permet à un utilisateur de déplacer toutes ses bibliothèques vers un nouvel emplacement sans modifier les tables de bibliothèques. La seule chose qui doit changer est de redéfinir la variable pour pointer vers le nouvel emplacement. Les variables de substitution de chemin de KiCad sont éditées avec Préférences → Configurer les chemins... dans le gestionnaire de projet ou l'une des fenêtres Éditeur.

Une variable de substitution de chemin utile est ${KIPRJMOD}. Cette variable pointe toujours vers le répertoire du projet actuel, elle peut donc être utilisée pour inclure des bibliothèques spécifiques au projet qui sont stockées à l'intérieur du répertoire du projet.

Au premier lancement, KiCad invite l'utilisateur à configurer la table de bibliothèques de symboles et la table de bibliothèques d'empreintes. Pour passer à nouveau par cette configuration, supprimez ou renommez les fichiers de table de bibliothèques de symboles ou d'empreintes. Faites une sauvegarde des tables avant de les supprimer.

L'emplacement des fichiers de table de bibliothèques de symboles et d'empreintes dépend du système d'exploitation.

- Windows : %APPDATA%\kicad\9.0\sym-lib-table et %APPDATA%\kicad\9.0\fp-lib-table
- Linux : ~/.config/kicad/9.0/sym-lib-table et ~/.config/kicad/9.0/fp-lib-table
- macOS : ~/Library/Preferences/kicad/9.0/sym-lib-table et ~/Library/Preferences/kicad/9.0/fp-lib-table

### Création de nouvelles bibliothèques globales ou de projet

La première étape pour dessiner un nouveau symbole ou empreinte est de choisir une bibliothèque dans laquelle le stocker. Pour ce guide, le symbole et l'empreinte de l'interrupteur iront dans de nouvelles bibliothèques spécifiques au projet.

Ouvrez l'Éditeur de symboles depuis le gestionnaire de projet. Cliquez sur Fichier → Nouvelle bibliothèque, et sélectionnez Projet. Choisissez un nom pour la nouvelle bibliothèque (par ex. getting-started.kicad_sym) et enregistrez-la dans le répertoire du projet. La nouvelle bibliothèque vide est maintenant sélectionnée dans le volet Bibliothèques à gauche, et a été automatiquement ajoutée à la table de bibliothèques de projet (vérifiez l'onglet Bibliothèques spécifiques au projet dans Préférences → Gérer les bibliothèques de symboles...).

### Création de nouveaux symboles

Maintenant créez le symbole d'interrupteur dans la nouvelle bibliothèque. Avec la bibliothèque getting-started sélectionnée dans le volet Bibliothèques, cliquez sur Fichier → Nouveau symbole.... Dans le champ Nom du symbole, entrez le numéro de pièce : M2011S3A1W03. Les symboles d'interrupteur devraient avoir des désignateurs de référence qui commencent par SW, donc changez le champ Désignateur de référence par défaut en SW. Tous les autres champs peuvent rester aux valeurs par défaut.

Dans le volet Bibliothèques, le symbole M2011S3A1W03 apparaît maintenant sous la bibliothèque getting-started. Dans le canevas, une croix indique le centre de l'empreinte, et du texte a été ajouté pour le désignateur de référence. Pour l'instant, déplacez le texte loin du centre du symbole pour le dégager.

#### Broches de symbole

Commencez à dessiner le symbole en ajoutant une broche. Ce symbole n'aura pas de broche 1, nous commencerons donc par une broche numérotée 2. Cliquez sur le bouton Ajouter une broche dans la barre d'outils de droite. La boîte de dialogue Propriétés de la broche apparaîtra. Définissez les propriétés de la broche comme suit :

- Nom de broche : A
- Numéro de broche : 2
- Type électrique : Passive
- Orientation : Droite
- Position X : -200 mils
- Position Y : 0

**NOTE**

Il est fortement recommandé d'utiliser toujours des mils (ou des pouces) dans l'Éditeur de schéma et l'Éditeur de symboles, particulièrement pour les broches de symbole. Mélanger les unités impériales et métriques entraînera des broches de symbole qui ne peuvent pas être correctement connectées car elles ne s'alignent pas avec les fils ou d'autres broches. Les bibliothèques KiCad utilisent une grille de 50 mils pour leurs broches ; utiliser un système d'unités différent empêchera vos symboles et schémas de se connecter avec les symboles intégrés de KiCad. Notez que contrairement à l'éditeur de PCB, les unités dans le schéma n'ont aucune signification physique.

Cliquez sur OK, puis cliquez sur le canevas pour placer la broche. Si la broche s'est déplacée après avoir cliqué sur OK, il peut être nécessaire de modifier à nouveau les propriétés de la broche (double-cliquez sur la broche, ou clic droit sur la broche → Propriétés...) pour définir la position correctement.

Ajoutez une deuxième broche, mais cette fois n'utilisez pas l'outil Ajouter une broche. Au lieu de cela, appuyez sur Insert. Une nouvelle broche numérotée 3 est ajoutée au symbole, juste en dessous de la broche 2.

**ASTUCE**

Dans de nombreux endroits dans KiCad, appuyer sur Insert répétera la dernière action. L'emplacement du nouvel élément sera décalé et la numérotation incrémentée automatiquement, selon le cas. Dans l'Éditeur de symboles, cela peut être utilisé pour placer rapidement un grand nombre de broches. Dans l'Éditeur de schéma, cela peut être utilisé pour placer à plusieurs reprises un composant, ou pour étiqueter les broches d'un grand composant avec des étiquettes numérotées. Insert peut être utile dans les éditeurs d'empreintes et de circuits également.

Nous voulons que la broche 3 soit sur le côté droit du symbole d'interrupteur, nous éditerons donc ses propriétés pour changer l'emplacement et l'orientation. Au lieu d'utiliser la boîte de dialogue Propriétés de la broche, cette fois nous pouvons utiliser le panneau Propriétés. C'est un panneau ancré sur le côté gauche du canevas d'édition qui vous permet de visualiser et d'éditer les propriétés de l'objet ou des objets sélectionnés. Pour afficher ou masquer le panneau Propriétés, utilisez le bouton dans la barre d'outils de gauche.

Avec la broche 3 sélectionnée, utilisez le panneau Propriétés pour définir ses propriétés comme suit :

- Nom de broche : B
- Position X : 200 mils
- Position Y : 0
- Orientation : Gauche

**NOTE**

Le panneau Propriétés est disponible dans chaque éditeur KiCad (Schéma, Circuit, Symbole et Empreinte).

#### Fonctionnalités graphiques

Avec les broches placées, utilisez les outils cercle et ligne pour faire en sorte que le symbole ressemble à un interrupteur SPST. Pour cette étape, il sera utile de basculer vers une grille plus fine : cliquez droit sur le canevas et sélectionnez une grille plus petite dans le sous-menu Grille. Après avoir ajouté les formes graphiques, revenez à une grille de 50 mils.

**AVERTISSEMENT**

Les petites grilles sont utiles pour les fonctionnalités graphiques, mais les broches de symbole doivent toujours être placées sur une grille de 50 mils (1,27 mm). Les broches qui ne sont pas alignées sur une grille de 50 mils ne pourront pas se connecter aux fils dans le schéma.

#### Propriétés du symbole

Maintenant éditez les propriétés pour l'ensemble du symbole avec Fichier → Propriétés du symbole, ou en double-cliquant sur le canevas. Changez le champ Valeur en M2011S3A1W03, et ajoutez spst switch toggle au champ Mot-clé pour faciliter la recherche du symbole. Pour ce symbole, les noms de broches n'ajoutent aucune information utile, donc décochez Montrer le nom de broche pour rendre le symbole visuellement plus simple.

Après avoir cliqué sur OK, déplacez le texte du champ valeur plus bas pour qu'il ne chevauche pas les graphiques du symbole.

Le symbole est maintenant complet. Enregistrez-le et passez à la création d'une empreinte.

### Création de nouvelles empreintes

Ouvrez l'Éditeur d'empreintes et créez une nouvelle bibliothèque d'empreintes spécifique au projet nommée getting-started.pretty (Fichier → Nouvelle bibliothèque...). Comme pour les bibliothèques de symboles, la nouvelle bibliothèque d'empreintes est ajoutée à la table de bibliothèques de projet. Avec la nouvelle bibliothèque sélectionnée dans le volet Bibliothèques, créez une nouvelle empreinte (Fichier → Nouvelle empreinte...). Éditez les propriétés de l'empreinte (bouton dans la barre d'outils du haut) et définissez les propriétés suivantes :

- Nom de l'empreinte : Switch_Toggle_SPST_NKK_M2011S3A1x03
- Valeur : Switch_Toggle_SPST_NKK_M2011S3A1x03
- Type de composant : Trou traversant

#### Pastilles d'empreinte

L'interrupteur a deux broches, numérotées dans la datasheet comme 2 et 3, et espacées de 4,7 mm. Pour faciliter le placement, ajustez la grille pour correspondre à l'espacement des pastilles. Ouvrez les paramètres de grille en cliquant droit sur le bouton dans la barre d'outils de gauche et en sélectionnant Éditer les grilles.... Ajoutez une nouvelle grille avec le bouton plus en bas. Définissez la taille X de la nouvelle grille à 4,7 mm. Acceptez la boîte de dialogue, retournez au canevas d'édition, puis basculez vers la nouvelle grille dans le menu déroulant grille dans la barre d'outils du haut, si elle n'est pas déjà sélectionnée.

Par convention, les empreintes traversantes ont la broche 1 située à (0,0) et sont orientées avec la broche 1 en haut à gauche. La version SPST de cet interrupteur n'a pas de broche 1, donc l'empreinte laissera (0,0) vide et placera les pastilles 2 et 3 à (0, 4,7 mm) et (0, 9,4 mm). Notez que dans le système de coordonnées par défaut de KiCad, l'axe Y positif est orienté vers le bas.

**NOTE**

Les coordonnées X et Y du curseur sont affichées dans la barre d'état en bas de la fenêtre. Vous pouvez utiliser cela pour vérifier les coordonnées lorsque vous dessinez ou placez quelque chose.

Utilisez l'outil Ajouter une pastille dans la barre d'outils de droite pour placer une pastille une division de grille en dessous de l'origine, ce qui est (0, 4,7 mm). Appuyez sur Esc pour quitter l'outil pastille, puis double-cliquez sur la pastille pour éditer ses propriétés. Changez le numéro de pastille en 2 et vérifiez que la position est correcte. Les broches de l'interrupteur mesurent 1,17 mm x 0,8 mm, ce qui donne une diagonale (dimension de broche maximale) de 1,42 mm. Par conséquent, définissez le diamètre du trou à 1,42 mm + 0,2 mm = 1,62 mm, et le diamètre de la pastille à 1,62 mm + 2*0,15 mm = 1,92 mm pour fournir un anneau annulaire suffisant.

Maintenant utilisez à nouveau l'outil Ajouter une pastille pour placer l'autre pastille à (0, 9,4 mm). Notez que le numéro de pastille est automatiquement incrémenté et les propriétés incluant la taille de pastille et la taille de trou sont copiées de la pastille précédente.

Avec les deux pastilles placées, les anneaux annulaires semblent légèrement petits. L'interrupteur sera plus facile à souder et mécaniquement plus robuste si les anneaux annulaires sont agrandis. Augmentez l'épaisseur de l'anneau annulaire de 0,15 mm à 0,3 mm en éditant la pastille 2 et en changeant la taille de pastille à 1,62 mm + 2*0,3 mm = 2,22 mm. Ne changez pas la taille du trou. Notez que le champ taille de pastille accepte les expressions mathématiques, donc 1.62+2*0.3 peut être entré directement et sera évalué à 2,22 mm.

**ASTUCE** De nombreuses zones de texte dans KiCad prennent en charge les expressions mathématiques, y compris les conversions d'unités.

Faites la même modification d'anneau annulaire à l'autre pastille également. Comme raccourci, faites un clic droit sur la pastille 2, cliquez sur Pousser les propriétés de pastille vers d'autres pastilles..., puis cliquez sur Changer les pastilles sur l'empreinte actuelle.

#### Graphiques d'empreinte

Une bonne empreinte aura le contour exact de la pièce dessiné sur la couche de fabrication (F.Fab), un contour légèrement plus grand sur la couche sérigraphie (F.Silkscreen), et un courtyard (F.Courtyard) entourant l'empreinte entière pour empêcher les chevauchements avec d'autres empreintes.

Basculez vers la couche de fabrication avant en cliquant sur F.Fab dans le panneau Couches à droite. Le contour de fabrication devrait correspondre précisément aux dimensions physiques de la pièce, qui est de 7,9 mm de large et 13 mm de haut. Utilisez les outils ligne, rectangle ou polygone pour dessiner le contour de la pièce comme montré dans la capture d'écran ci-dessous.

Une façon de placer précisément le contour est de créer une nouvelle grille avec l'espacement X et Y correct, comme nous l'avons fait pour les pastilles. Assurez-vous de décocher la case Lié dans la boîte de dialogue Paramètres de grille pour permettre un espacement de grille X et Y inégal. Vous pouvez ensuite ajuster l'origine de la grille en cliquant droit sur le bouton et en sélectionnant Origine de la grille.... Configurez l'espacement de grille et l'origine comme suit :

- Grille X : 7,9 mm
- Grille Y : 13 mm
- Origine X : 7,9 mm / 2 = 3,95 mm
- Origine Y : 4,7 mm - (13 mm / 2) = -1,8 mm.

Le dessin de fabrication terminé est montré ci-dessous, avec les coordonnées des coins annotées.

Ensuite, basculez vers la couche F.Silkscreen. Nous voulons que le contour de sérigraphie soit juste à l'extérieur du contour de la pièce, donc les lignes de sérigraphie seront dessinées 0,11 mm à l'extérieur des lignes sur la couche de fabrication (0,11 mm est la moitié de la largeur de ligne fab de 0,10 mm, plus la moitié de la largeur de ligne sérigraphie de 0,12 mm). Les coordonnées exactes sont montrées dans la capture d'écran ci-dessous, et des paramètres de grille utiles sont :

- Grille X : 7,9 mm + 2 * 0,11 mm = 8,12 mm
- Grille Y : 13 mm + 2 * 0,11 mm = 13,22 mm
- Origine X : 8,12 mm / 2 = 4,06 mm
- Origine Y : -1,8 mm - 0,11 mm = -1,91 mm

Enfin, sélectionnez la couche F.Courtyard. Nous voulons que le contour de courtyard entoure la pièce avec un espacement de 0,25 mm.

Pour varier, nous pouvons utiliser une stratégie différente pour dessiner la forme sur cette couche. Basculez vers une grille de 1mm au lieu d'une grille personnalisée, et dessinez un rectangle entourant approximativement l'empreinte. Sélectionnez le rectangle et appuyez sur E pour éditer ses propriétés, et entrez directement les coordonnées des coins du rectangle. Les coordonnées des coins sont :

- En haut à gauche : (-4,2, -2,05)
- En bas à droite : (4,2, 11,45)

Après avoir terminé les contours, positionnez le texte comme montré ci-dessous. L'empreinte est complète.

#### Conventions de bibliothèque KiCad

Pour maintenir des bibliothèques de symboles et d'empreintes de haute qualité, KiCad dispose d'un document Conventions de bibliothèque KiCad, qui est un ensemble de directives pour les symboles et empreintes. Il n'est pas nécessaire de suivre ces conventions pour les bibliothèques personnelles, mais elles constituent un bon point de départ. Les empreintes et symboles dans la bibliothèque officielle doivent suivre KLC. KLC est utilisé comme base pour le symbole et l'empreinte dans ce guide.

### Ajout de l'interrupteur au schéma

Maintenant que l'empreinte est complète, le symbole d'interrupteur peut être modifié pour que l'empreinte correspondante soit utilisée par défaut.

Retournez à l'éditeur de symboles et ouvrez le symbole d'interrupteur. Éditez les Propriétés du symbole. Cliquez dans le champ Empreinte, puis cliquez sur l'icône de livre de bibliothèque qui apparaît. Naviguez vers la bibliothèque d'empreintes de projet et double-cliquez sur l'empreinte d'interrupteur. Enregistrez le symbole.

L'empreinte d'interrupteur est maintenant attribuée à ce symbole par défaut ; l'empreinte n'a pas besoin d'être sélectionnée manuellement chaque fois que le symbole est ajouté à un schéma.

Ouvrez le schéma, ajoutez un nouveau symbole, et sélectionnez le nouveau symbole d'interrupteur. Câblez-le pour connecter ou déconnecter la LED et la batterie.

Il n'est pas nécessaire de choisir manuellement une empreinte pour l'interrupteur, car le symbole d'interrupteur spécifie déjà une empreinte. Exécutez l'ERC pour vous assurer que le schéma modifié ne viole aucune règle électrique.

### Ajout de l'interrupteur à la disposition

Assurez-vous que le schéma est enregistré, puis ouvrez l'Éditeur de circuits pour ajouter le symbole à la disposition. Mettez à jour le PCB avec les modifications du schéma en utilisant Outils → Mettre à jour le PCB depuis le schéma... et placez l'empreinte d'interrupteur sur le circuit comme montré. Si nécessaire, redimensionnez le contour du circuit et la zone de cuivre (la zone de cuivre se déremplit si elle est redimensionnée, mais vous pouvez la reremplir si nécessaire avec B).

Le chevelu montre les nouvelles connexions qui doivent être routées. De plus, la connexion entre la batterie et la résistance doit être supprimée.

Tout d'abord, supprimez les pistes inutiles. Sélectionnez l'une des pistes entre la batterie et la résistance — peu importe laquelle. Appuyez sur U plusieurs fois pour étendre la sélection pour inclure tous les segments entre la batterie et la résistance. Appuyez sur Suppr pour retirer la connexion.

Routez les nouvelles pistes entre la batterie et l'interrupteur, et entre l'interrupteur et la résistance. Appuyez sur B pour reremplir les zones.

Enfin, réexécutez le DRC pour vous assurer que le circuit modifié ne viole aucune règle de conception.

---

## Liaison des symboles, empreintes et modèles 3D

### Symboles et empreintes

Comme décrit dans la section attribution d'empreintes, chaque symbole dans le schéma doit avoir une empreinte qui lui est attribuée pendant le processus d'entrée schéma. Le nom de l'empreinte attribuée à chaque symbole est stocké dans le champ Empreinte des propriétés du symbole.

Les symboles peuvent spécifier une empreinte présélectionnée. Les empreintes n'ont pas besoin d'être attribuées manuellement à de tels symboles, car une empreinte a été choisie lors de la création du symbole. Les utilisateurs peuvent remplacer l'empreinte présélectionnée pendant le processus d'attribution d'empreintes normalement. Définir une empreinte par défaut est une bonne idée pour les symboles qui auront généralement ou toujours la même empreinte qui leur sera attribuée, par exemple un composant qui n'est disponible que dans un seul boîtier. L'empreinte d'interrupteur a été définie comme défaut pour son symbole correspondant.

Les symboles peuvent également spécifier des filtres d'empreintes, qui peuvent être utilisés pour masquer les empreintes incompatibles avec le symbole. Par exemple, le symbole 74HC00 a des filtres d'empreintes qui ne montrent que les empreintes DIP et SO14 applicables dans l'outil d'attribution d'empreintes.

Les exigences KLC pour les filtres d'empreintes contiennent quelques conseils utiles pour des filtres d'empreintes efficaces.

### Empreintes et modèles 3D

Les modèles 3D pour les composants sont stockés dans des fichiers séparés. Les noms de fichiers pour le(s) modèle(s) 3D du composant sont enregistrés dans l'empreinte. N'importe quel nombre de modèles 3D peut être ajouté à chaque empreinte. Les noms de fichiers des modèles 3D, ainsi que l'échelle, la rotation, le décalage et l'opacité du modèle, sont définis dans l'onglet Modèles 3D des Propriétés de l'empreinte.

Les formats de modèles 3D STEP (.step) et VRML (.wrl) sont tous deux pris en charge. Les fichiers STEP sont utiles là où la précision dimensionnelle est nécessaire, tandis que les fichiers VRML peuvent être utilisés pour des rendus visuellement plus attrayants. Beaucoup d'empreintes dans la bibliothèque de KiCad ont des modèles 3D associés ; ces modèles sont fournis aux formats VRML et STEP. Seul l'un des deux modèles doit être listé dans l'empreinte (typiquement le nom de fichier VRML est donné). KiCad peut automatiquement substituer la version STEP lors de l'export d'un modèle 3D du circuit à des fins de CAO mécanique.

**NOTE**

Toutes les empreintes dans la bibliothèque de KiCad ne sont pas fournies avec des modèles 3D, mais toutes les empreintes listent un nom de fichier de modèle 3D même si le modèle 3D n'existe pas. C'est pour que les modèles 3D puissent être ajoutés à une date ultérieure sans avoir besoin de modifier l'empreinte.

FreeCAD avec le Workbench StepUp sont utiles pour créer des modèles 3D de composants ; ils sont utilisés pour de nombreux modèles dans la bibliothèque de KiCad. StepUp est utilisé pour générer des fichiers STEP et VRML avec placement, échelle et rotation corrects.

---

## Où aller ensuite

### Plus de ressources d'apprentissage

Pour plus d'informations sur la façon d'utiliser KiCad, consultez le manuel.

D'autres ressources incluent le forum utilisateur officiel de KiCad, Discord ou IRC, et des ressources d'apprentissage supplémentaires de la communauté KiCad.

Pour voir plus de ce qui est possible avec KiCad, parcourez la section Made With KiCad du site web, ou ouvrez les projets de démonstration inclus avec KiCad (Fichier → Ouvrir un projet de démonstration...).

### Aidez à améliorer KiCad

Pour signaler un bogue ou demander une fonctionnalité, veuillez utiliser Aide → Signaler un bogue ou ouvrir un ticket sur Gitlab.

Pour contribuer au développement de KiCad, veuillez consulter la page Contribution des développeurs. Les utilisateurs peuvent également aider en contribuant aux bibliothèques ou à la documentation et traduction. Enfin, envisagez de soutenir financièrement le développement continu de KiCad.
