---
title: FAQ
summary : Questions fréquentes et dépannage
---
---

## Informations générales 💡
/// details | Que contient cette FAQ ?
Cette FAQ a été conçue dans le but de repondre aux questions les plus **fréquemment posées**.
Les réponses sont toujours écrites de façon à être comprises par tous. Les réponses peuvent également être complétées avec des liens vers d'autres pages du site ou un site externe.
///

/// details | Comment bien utiliser cette FAQ ?
Pour tirer le meilleur parti de cette FAQ, parcourez les catégories et sélectionnez les questions qui correspondent à votre besoin.  
Chaque réponse est rédigée de manière simple et claire afin de vous guider rapidement.
Si vous recherchez une information précise, utilisez la fonction de recherche intégrée de la page avec ```CTRL + F + "Votre recherche"``` .
///





## Généralité sur Skyrift 🌍
/// details | Qu'est-ce que Skyrift ?
Skyrift est un jeu de stratégie au tour par tour en 1 VS 1 dans lequel des dragons s’affrontent jusqu’à la destruction de la base ennemie.

Le joueur affronte une intelligence artificielle et doit gérer ses unités, ses ressources et son positionnement pour remporter la victoire.
///

/// details | A qui est destiné ce jeu ?
Skyrift s’adresse à toute personne souhaitant découvrir ou pratiquer un jeu de stratégie simple et accessible.

Aucune connaissance particulière n’est requise, ce qui le rend adapté aussi bien aux joueurs occasionnels qu’aux amateurs de stratégie.
///

/// details | A combien de joueur peut-on jouer ?
Skyrift se joue en **solo**, en 1 VS 1 contre une intelligence artificielle.

Il n’existe pas de mode multijoueur entre joueurs humains.
///

/// details | Quel est le but du jeu ?
Le but du jeu est de détruire la base ennemie avant que la vôtre ne soit détruite.

Pour y parvenir, le joueur doit invoquer des dragons, gérer ses ressources (Skygold) et adopter une stratégie efficace tout au long de la partie.
///

/// details | Sur quelles plateformes fonctionne le jeu ?
Skyrift est un jeu développé en Python et fonctionne sur les principaux systèmes d’exploitation disposant de Python, notamment :

- Windows
- Linux
- macOS

Les détails d’installation sont disponibles dans la section dédiée.
///

/// details | Doit-on disposer d'un ordinateur puissant pour pouvoir jouer à Skyrift ?
Non, Skyrift est un jeu léger qui ne nécessite pas de matériel performant.

Un ordinateur standard suffit pour faire fonctionner le jeu de manière fluide.
///

/// details | Puis-je sauvegarder ma partie ?
Skyrift repose sur un système de parties rapides et donc ne propose pas de fonctionnalité de sauvegarde.

Chaque partie est jouée du début à la fin en une seule session.
///





## Installation et débuts 📥
/// details | Comment installer Skyrift ?
Pour installer SkyRift, veuillez vous rendre dans la section [installation](./installation.md) et suivre les instructions.
Cette page explique les prérequis, l’installation des dépendances et la mise en place du jeu.
///

/// details | Où puis-je télécharger la dernière version de Skyrift ?
La dernière version de Skyrift est disponible depuis le dépôt officiel du projet.

Un lien de téléchargement est fourni dans la section Installation.
///

/// details | Quel espace est nécessaire pour installer Skyrift ?
Skyrift est un jeu léger et nécessite peu d’espace disque.
///

/// details | Le jeu est-il gratuit ?
Oui, Skyrift est un jeu gratuit.
Il est développé dans un cadre pédagogique et peut être utilisé librement sans frais.
///

/// details | Dois-je installer des logiciels supplémentaire pour faire fonctionner Skyrift ?
Oui, Skyrift nécessite :

- Une version récente de **Python**
- L’installation des dépendances listées dans la documentation

Aucun autre logiciel spécifique n’est requis.
///

/// details | Comment exécuter le jeu ?
Une fois l’installation terminée, le jeu peut être lancé depuis un terminal en exécutant le fichier principal du projet.

Les commandes exactes à utiliser sont précisées dans la section [Installation](./installation.md).
///





## Unités et structures 🐲
/// details | Quels types d'unités sont disponibles dans Skyrift ?
Skyrift propose plusieurs types d’unités basées sur des dragons, chacun ayant un rôle précis en combat :

- **Les dragonnets** : petits dragons rapides, efficaces au combat rapproché.
- **Les dragons moyens** : unités robustes, plus résistantes mais moins mobiles.
- **Les dragons à deux têtes (dragons géants)** : unités très puissantes, lentes mais extrêmement résistantes.

Chaque unité possède des caractéristiques propres (coût, vitesse, dégâts, portée, points de vie).
Pour plus de détails, consultez la page [Unités](./entities.md).
///

/// details | Quelle est la différence entre une unité et une structure ?
Les **unités** sont des éléments mobiles que vous contrôlez activement pendant la partie (dragons).  
Les **structures**, quant à elles, sont statiques et servent principalement à la défense de votre base.
///

/// details | Comment sélectionner une unité ?
Pour sélectionner une unité :

- Cliquez directement sur le dragon souhaité dans l’interface du jeu.
- Une fois sélectionnée, l’unité peut recevoir des ordres (déplacement, attaque).

Une indication visuelle permet de savoir quelle unité est actuellement sélectionnée.
///

/// details | Pourquoi certaines unités sont-elles lentes ou coûteuses ?
L’équilibrage du jeu repose sur un compromis entre puissance, coût et mobilité :

- Les unités puissantes sont plus lentes et plus coûteuses en skygold.
- Les unités rapides sont moins résistantes et infligent moins de dégâts.

Cela encourage le joueur à adapter sa stratégie plutôt qu’à utiliser un seul type d’unité.
///





## Combat et stratégie ⚔️
/// details | Comment fonctionne une partie ?
Skyrift est un jeu de combat stratégique **au tour par tour** en 1 VS 1 contre une intelligence artificielle.

Chaque joueur possède une base qu’il doit défendre tout en attaquant celle de l’adversaire.
La partie se déroule sur une grille où les dragons sont invoqués, déplacés et utilisés pour combattre jusqu’à la destruction de la base ennemie.
///

/// details | Que peut-on faire pendant un tour ?
À chaque tour, le joueur peut :

- Invoquer un dragon (si le point d’apparition est libre)
- Déplacer ses dragons sur la grille
- Attaquer les dragons ennemis adjacents
- Gérer ses ressources (Skygold) pour préparer les tours suivants

Chaque décision est importante, car les actions effectuées influencent directement le tour suivant.
///

/// details | Comment bien gérer sa stratégie contre l’intelligence artificielle ?
Pour être efficace contre l’IA, il est conseillé de :

- Bien gérer son Skygold en évitant les dépenses inutiles
- Varier les types de dragons invoqués
- Anticiper les mouvements ennemis en protégeant sa base
- Profiter des moments où l’IA est en déplacement pour attaquer
///

///details | Pourquoi le positionnement est-il important ?
Le positionnement des dragons sur la grille est un élément clé du combat.
Un bon placement permet de :

- Bloquer l’accès à votre base
- Protéger les unités fragiles
- Attaquer efficacement les dragons ennemis
- Empêcher l’ennemi d’invoquer de nouvelles unités sur son spawn
///




## Paramètres et performance ⚙️
/// details | Quels paramètres sont disponibles dans le jeu ?
Skyrift dispose d’un menu de paramètres accessible en jeu.
Ce menu permet :

- De consulter à nouveau les règles du jeu
- D’activer ou désactiver les effets sonores
- D’activer ou désactiver la musique
- De quitter la partie en cours

Ces options permettent d’adapter l’expérience de jeu selon vos préférences.
///

/// details | Comment désactiver le son ou la musique ?
Dans le menu des paramètres :

- Une option permet de couper les **effets sonores**
- Une autre option permet de couper la **musique**

Les deux réglages sont indépendants et peuvent être modifiés à tout moment pendant la partie.
///

/// details | Que se passe-t-il si je quitte une partie en cours ?
Si vous utilisez le bouton **Quitter** depuis le menu des paramètres :

- La partie en cours est immédiatement arrêtée
- La progression de la partie n’est pas sauvegardée

Cette option permet de quitter rapidement le jeu si nécessaire.
///