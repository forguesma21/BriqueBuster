## <center> Projet </center>

Description

### Prérequis 

# Lancement du projet
## 1. Création d'environnement virtuel python
> À faire seulement si vous n'en avez pas déjà un
1. ```python -m venv venv``` (si vous n'avez pas d'environnement virtuel déjà créé)
2. ```venv\Scripts\activate```
> [!CAUTION]
> En cas d'erreur, assurez vous que votre environnement virtuel est sur python 3.10

## 2. Installation des dépendances
1. ```python -m pip install -r requirements.txt```

## Initialisation de la base de données
1. Ouvrir le fichier .env et y entrer les informations de la BD de votre choix ou créer une base de donnée mysql nommée "brique_buster"
2.  ```python initialize_db.py```
2. ```python seed.py```

## Démarrer l'application 
1. ```python app.py```