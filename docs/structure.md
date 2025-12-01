---
title: Structure du projet 
nav_order: 3
---

# Structure du projet
{: .fs-9 .fw-300 }
---

Présentation de la structure du code et de la répartition des classes.

### Structure générale :
```
- main.py  (lance le jeu)
- assets/
  - sounds/
  - sprites/
- component/
  - entities/ (contient les unités)
  - position.py
- page/
  - ui.py (affichage de l’écran de jeu)
  - ...
- test/ (tests du projet)
- grid.py (Classe Grille)
- economy.py (gestion des revenu des joueur)
- events.py (gestion des événements : clique de souris, clique de touche etc…)

```

### Structure des objets :

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