import os
import sys

# Assurez-vous que le chemin est correct
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from database.db import db
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_tables():
    app = Flask(__name__)

    # Configurez la connexion à la base de données# Configurez la connexion à la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Importer les modèles ici pour qu'ils soient reconnus par SQLAlchemy
        from database.models import Utilisateurs, Produits, Paniers, PaniersProduits, Reservations, Fidelite, \
            CategorieFidelite, Reservations_items

        # Créer toutes les tables
        db.create_all()
        print("Tables créées avec succès.")


if __name__ == "__main__":
    create_tables()