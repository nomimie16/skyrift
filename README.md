# Skyrift

Skyrift est un jeu tour par tour développé avec Pygame en lanagage Python. Ce jeu de startégie mélange mécaniques de combat et intelligence artificielle.

[![Version](https://img.shields.io/badge/version-0.13.0-blue.svg)](https://github.com/nomimie16/skyrift)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://nomimie16.github.io/skyrift)


## Description
Ce jeu développé en Python se déroule dans les cieux, où une zone de combat est générée aléatoirement avec diffréntes iles aux pouvoirs magiques. Le but du jeu est de démolir la base de votre ennemi, à l'aide de votre armée de dragons. Pour réussir à atteindre la victoire, et remporter le Skyrift, il vous faudra utiliser des tours de défense, passer aux travers d'un volcan et ramasser un maximum de Skygold pour acheter vos dragons.

## Installation

- Téléchargement de l'exécutable
  - Rendez vous sur le dépôt GitHub officiel : [Skyrift Github]((https://github.com/nomimie16/skyrift))
  - Dans la section "Releases", à droite, cliquez sur la dernière version téléchargeable.
  - Téléchargez l'exécutable correspondant à votre système.

## Lancement du jeu
- Lancement depuis **l'éxecutable** (bientot disponible) :
  * Accédez au fichier skyrift.exe et lancez le fichier. Le jeu va se lancer automatiquement.

- Lancement depuis un **terminal** de commande :
  * Dans un terminal ouvert sur le repertoire du jeu, entrez cette commande :
  ```bash
  python main.py
  ```

## Dépendances

* [Pygame](https://www.pygame.org/news) :  affichage, sprites, événements et sons.

* [Pygame GUI](https://pygame-gui.readthedocs.io/en/latest/) :  Framework d’interface graphique basé sur Pygame. 

* [Numpy](https://numpy.org/) : mathématiques avancés, matrices et algorithmes IA.

* [Moviepy](https://zulko.github.io/moviepy/) :

* [Pytest](https://docs.pytest.org/en/stable/) : Framework de tests automatisés.

## Gameplay
Une fois le jeu lancé, vous aurez accès à l'écran du menu principal.
Pour commencer une nouvelle partie, cliquez sur " START " et vous aurez accès au début du jeu.

Ensuite le jeu se déroule tour par tour et quand arrive votre tour, plusieurs possibilités s'offrent à vous :

- **Acheter** une unité (dragon, tour ou autre..) : en cliquant sur votre base, une boutique apparait à l'écran, vous permettant d'acheter ce dont vous avez besoin pour gagner

- **Déplacer** un dragon : les déplacements possibles s'affichent en cliquant sur un dragon existant  

- **Attaquer** un dragon adverse : les attaques deviennent possibles et visibles lorsque votre dragon se tient à une certaine distance de celui d'un ennemi

Il vous faudra donc choisir une action à réaliser pour poursuivre le jeu.

Au cours de la partie, il vous est également posssible d'accéder aux paramètres du jeu, en cliquant sur l'icone en haut à droite de l'écran. Ce menu concernant les paramètres permet :

- De consulter à nouveau les règles du jeu
- D’activer ou désactiver les effets sonores
- D’activer ou désactiver la musique
- De quitter la partie en cours
- 

Il ne vous reste plus qu'à défendre votre base et attaquer votre ennemi pour tenter de remporter le Skyrift !

## Structure du projet 

```
 README.md
├── assets
│   ├── font
│   ├── img
│   └── sprites
├── component
│   ├── __pycache__
│   ├── entities
│   ├── enum
│   ├── grid.py
│   ├── path_finding.py
│   └── position.py
├── const.py
├── docs
│   ├── docs
│   ├── mkdocs.yml
│   └── site
├── economy.py
├── events
│   └── dragonEvents.py
├── maptest.py
├── mkdoc
├── page
│   ├── component
│   ├── game.py
│   ├── launch.py
│   ├── main.py
│   ├── menu.py
│   ├── pause.py
│   ├── rules.py
│   ├── settings.py
│   ├── sidepanels.py
│   ├── sound.py
│   ├── startGame.py
│   └── ui.py
├── player.py
├── pytest.ini
├── requirements.txt
├── screen_const.py
├── test
│   ├── components
│   ├── test_economy.py
│   └── test_grid.py
```

## Documentation

Pour visualiser la documentation détaillée, rendez vous sur [https://nomimie16.github.io/skyrift/](https://nomimie16.github.io/skyrift/).

* Documentation utilisateur : installation, gameplay, contrôles.
* Documentation technique : Structure, développement, architecture.

## Auteurs

* [GERME Charlotte](https://github.com/chharlote) 
* [ARABAH Yanis](https://github.com/Yanisssssse) 
* [LIGNIER Noémie](https://github.com/nomimie16) 
* [CHATELAIN Lilou](https://github.com/liiloouu16) 
* [FAILLIE Chloé](https://github.com/ChloeXena) 