---
title: Maintenance et support
summary : Présentation de la structure du code et de la répartition des classes.
---

---

## Structure et organisation du code

Le projet Skyrift utilise Git pour le versionnement du code.	

### Utilisation de Git

* **Bonnes pratiques :**

    * Créer une branche pour chaque fonctionnalité ou correction
    * Utiliser des messages de commit clairs
    * Tester le jeu avant chaque push
    * Exemple de message de commit :
    ```fix: correction bug déplacement dragon```

* **Ce projet respecte la [convention de commit](https://www.conventionalcommits.org/en/v1.0.0/) :**

    * ```fix:``` corrige un bug dans le code
    * ```feat:``` introduit une nouvelle fonctionnalité dans le code
    * ```docs:``` ajoute un changement au sein de la documentation
    * ```refactor:``` spécifie un changement dans le code qui ne corrige pas de bug et n'ajoute pas de nouvelle fonctionnalité
    * ```tests:``` ajoute des tests manquants ou des corrections de tests


### Arborescence des fichiers
...
à faire à la fin du projet


### Utilité des dossiers

* ```assets/``` : contient toutes les ressources graphiques et sonores
* ```tests/``` : contient les tests unitaires
* ```main.py``` : fichier principal d’exécution
* ...
* à faire à la fin du projet

### Emplacement des constantes globales

Les **constantes globales** (coûts, PV, dégâts, etc.) sont regroupées dans un fichier dédié afin de faciliter l’équilibrage du jeu.

à faire à la fin du projet

---

## Installer l'environnement de dev

### Version de Python requise

Skyrift nécessite :

```Python 3.x``` (version recommandée : 3.10 ou supérieure)

### Dépendances

Pour vérifier et installer les dépendances requise au jeu, rendez vous dans la partie [dépendances](./dependencies.md) de la documentation.

### Système d'exécution 

Le jeu est lancé via le fichier principal : ```python main.py```

---

## Tests et vérification

### Comment exécuter les tests unitaires
Les tests unitaires sont situés dans le dossier ```tests/```.

Exécution :
```
python -m unittest
```

### Rédiger de nouveaux tests

* Lors de **l’ajout** d’une fonctionnalité :
    * Créer un nouveau fichier de test dans ```tests/```
    * Tester les comportements attendus
    * Vérifier les cas d’erreur


* **Erreurs possibles** que peuvent rencontrer les admins
    * Dépendances manquantes
    * Mauvaise version de Python
    * Fichiers assets introuvables
    * Conflits Git lors des mises à jour

---

## Publier des mises à jour

### Générer un exécutable

Un exécutable peut être généré à l’aide d’un outil tel que [PyInstaller](https://pyinstaller.org/en/stable/).

Exemple :
```
pyinstaller main.py --onefile
```

### Publier une nouvelle version

* **Étapes recommandées :**

    * Mettre à jour le code
    * Tester le jeu
    * Mettre à jour le changelog
    * Créer un tag Git
    * Publier la version

### Modification des assets

Les assets peuvent être **modifiés** dans le dossier ```assets/```.

* **Recommandations :**

    * Conserver les noms de fichiers
    * Respecter les formats utilisés
    * Tester le jeu après modification

---

## Risques et problèmes connus


### Risques

* Désynchronisation entre code et assets
* Bugs introduits lors d’une mise à jour
* Incompatibilité avec certaines versions de Python

### En cas de problème

* Consulter les logs
* Vérifier les dépendances
* Tester sur un environnement propre

---

## Logs de maintenance

### Où trouver les logs

à faire à la fin du projet

### Log de maintenance

Exemple de log :

```
Date : 12/01/2026
Auteur : Nom Prénom
Version : 1.0.2
Actions :
- Correction bug IA
- Mise à jour dépendances
- Tests de validation
```