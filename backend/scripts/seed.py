import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # seed des cat de fidelite
        categories = [
            (0, "Cassette Basique",  0),
            (1, "VHS Classique",  100),
            (2, "Édition Collector",  500),
            (3, "LaserDisc Élite", 1000),
            (4, "Master du Magnétoscope", 2500)
        ]

        requete_categorie = """
                INSERT INTO categorie_fidelite (id, nom, seuil_minimum)
                VALUES (%s, %s, %s)
                """

        cursor.executemany(requete_categorie, categories)
        connection.commit()
        print(f"{cursor.rowcount} catégories de fidélité ont été insérées avec succès !")

        # seed pour les produits
        films = [
            ('123e4567-e89b-12d3-a456-426614174000', "Science-fiction", "La Guerre des Étoiles",
             "Un jeune fermier se joint à une rébellion contre un Empire maléfique.", 22.99, 121, 1977, 15),
            ('a3b55932-446d-44ac-a2be-2f1ffc7b8b28', "Aventure", "Les Aventuriers de l'arche perdue",
             "Indiana Jones cherche l'Arche d'alliance avant les nazis.", 20.99, 115, 1981, 5),
            ('a2c5853e-c7fd-4c20-8991-4fbe0a29aece', "Animation", "Le Roi Lion", "Un jeune lion doit retrouver son royaume après la mort de son père.", 16.99,
             89, 1994, 20),
            ('aa9e40c3-2d8f-42cf-85e9-1b9861449571', "Drame", "Le Fabuleux Destin d'Amélie Poulain",
             "Amélie, une jeune serveuse parisienne, décide de changer la vie des autres.", 18.99, 122, 2001, 8),
            ('b16ace2b-00d4-4f27-a25f-e0bc090ea85a', "Aventure", "Jurassic Park", "Des dinosaures ramenés à la vie terrorisent un parc à thème.", 12.99, 127,
             1993, 7),
            ('e53912b5-5c8b-4c6e-9140-45d8ede27ad3', "Drame", "Titanic",
             "Une romance naît entre deux passagers de classes différentes à bord d'un navire en perdition.", 14.99,
             195, 1997, 10),
            ('1d724a84-cdea-4195-b64a-5765ec6bb0de', "Science-fiction", "Inception",
             "Un voleur infiltre les rêves pour dérober des secrets et réimplanter des idées.", 18.99, 148, 2010, 12),
            ('df6381bb-3926-47e9-8d1f-2393182865dc', "Aventure", "Retour vers le Futur", "Un adolescent voyage dans le temps avec une voiture modifiée.", 17.99,
             116, 1985, 6),
            ('ad0c8fc5-8d15-4b9d-a2f3-9d6fc11ff0de', "Crime", "Pulp Fiction", "Une série d'histoires criminelles entremêlées dans Los Angeles.", 14.99, 154,
             1994, 8),
            ('c65aaa64-1049-47eb-9c31-b27a6e209f24',
            "Drame", "Rocky", "Un boxeur amateur de Philadelphie tente sa chance contre un champion.", 13.99, 120, 1976,
            10)
        ]

        requete_insertion = """
        INSERT INTO produits (id, categorie, nom, description, prix, longueur, annee, en_stock)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(requete_insertion, films)
        connection.commit()

        print(f"{cursor.rowcount} films ont été insérés avec succès !")

except Error as e:
    print(f"Erreur lors de la connexion à MySQL : {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
