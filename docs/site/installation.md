---
title: Installation et configuration
summary: Téléchargement et installation du jeu
---
---
Afin de lancer une toute première fois Skyrift, vous devez installer la dernière version du jeu disponible à ce jour.

## Prérequis système
* OS : Windows 10/11
* Mémoire : 2 GB RAM
* Stockage : 50 Mo d'espace libre requis

## Installation du jeu

!!! info "Information :"
    Il existe deux façons d'installer et de lancer Skyrift en fonction de vos préférences

* ### Téléchargement de l'exécutable

    1. Rendez-vous sur le dépôt GitHub officiel : [Skyrift Github](https://github.com/nomimie16/skyrift)

    2. Dans la section "Releases", à droite, cliquez sur la dernière version téléchargeable.

    3. Téléchargez l'exécutable correspondant à votre système.

* ### Lancement depuis le code source

    1. Depuis l'onglet **"Releases"**, téléchargez le code source si vous ne souhaitez pas utiliser l’exécutable.

    2. Décompressez le fichier téléchargé.

    3. Assurez-vous d’avoir [Python](https://www.python.org/downloads/) et [PIP](https://www.python.org/downloads/) installé sur votre machine.

    4. Ouvrez un terminal dans le dossier du projet et lancez :


``` 
pip install -r requirements.txt
python skyrift/main.py
pip
```

## Mise à jour

Lorsqu'une mise à jour apparaît sur le dépot officiel :

* Cliquez [ici](https://github.com/nomimie16/skyrift/releases) pour ouvrir la page GitHub contenant les dernières releases
* Téléchargez l'archive correspondant à votre système d'exploitation
* Extrayez l'archive
* Remplacez les anciens fichiers par les nouveaux
