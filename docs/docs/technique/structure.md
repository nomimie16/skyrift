---
title: Structure du projet 
summary : Présentation de la structure du code et de la répartition des classes.
---

---

## Structure et organisation du projet

**Skyrift** est structuré pour garantir une bonne **lisibilité** du code et une maintenance plus simple.

L’organisation des fichiers est basée sur une **séparation** entre les différentes **parties** du jeu.

---
## Principes de conception

Le projet respecte les principes suivants :

* Lisibilité et **clarté** du code
* **Réutilisabilité** des composants
* Facilité de **maintenance**

---

## Arborescence des fichiers

L’arborescence suivante représente l’organisation générale du projet.  
Elle pourra évoluer en fonction des besoins et de l’avancement du développement.

```
└── skyrift/
  ├── main.py  (lance le jeu)
  ├──  assets/
  |   ├── sounds/
  |   ├── sprites/
  ├──  component/
  |   ├── entities/ (contient les unités)
  |   ├── position.py
  ├── page/
  |   ├── ui.py (affichage de l’écran de jeu)
  |   ├── ...
  ├── test/ (tests du projet)
  ├── grid.py (Classe Grille)
  ├── economy.py (gestion des revenu des joueur)
  ├── events.py (gestion des événements : souris, clavier etc)

```

## Structure des objets 

```
- Class Entity
  - Class Dragon
    - Dragonnet
    - DragonDoubleTete
    - DragonGeant
  - Class EffectZone

- Class StaticEntity 
  - Base
  - Tower
  - Volcano
  - Tornado
  - island of life
  
- Class Grille (contient les cases et leur état)
- Class Economy
- Class Event
- Class Position
```

---

## Utilité des dossiers

### `assets/`

Contient l’ensemble des **ressources** utilisées par le jeu.

* Images (sprites, décors)
* Sons (effets sonores, musiques)
* Polices de caractères

Les fichiers présents dans ce dossier ne doivent pas être renommés sans modification correspondante dans le code.


### `src/`

Contient tout le code **source** du projet.


### `entities/`

Contient les **définitions** des **entités** du jeu :

- Les dragons
- Les tours de défenses
- Les structures (bases, volcan, il de vie, tornade)
- Les bourses


Les entités peuvent être :

- dynamiques (se déplacent, agissent)
- statiques (bâtiments, zones fixes)
- temporaires (effets, zones d’impact)


### `page/`

Gestion de **l’interface utilisateur** :

* Menus
* Écrans de lancement du jeu
* Interactions utilisateur

---

## Fichiers principaux

### `main.py`

Fichier principal d’exécution du jeu.

Responsabilités :

* Chargement des ressources
* Initialisation des systèmes
* Lancement de la boucle de jeu


### `src/constants.py`

Les **constantes globales** du jeu sont regroupées dans ce fichier 

Ce fichier contient notamment :

* Points de vie
* Dégâts
* Coûts
* Vitesses
* Paramètres de la map


### `requirements.txt`

Liste des **dépendances** Python nécessaires au bon fonctionnement du projet.

---