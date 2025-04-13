## <center> Projet </center>
# Lancement du projet
## 1. Création d'environnement virtuel python
> À faire seulement si vous n'en avez pas déjà un
1. ```python -m venv venv``` (si vous n'avez pas d'environnement virtuel déjà créé)
2. ```venv\Scripts\activate```
> [!CAUTION]
> En cas d'erreur, assurez vous que votre environnement virtuel est sur python 3.10

## 2. Installation des dépendances
1. ```python -m pip install -r requirements.txt```

## 3. Initialisation de la base de données
1. Ouvrir le fichier .env et y entrer les informations de la BD de votre 
2. ```python setup.py```
3.  ```flask init_db```

## 4. Démarrer l'application 
1. ```flask run```