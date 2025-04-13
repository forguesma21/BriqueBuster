import click
import os
import sys
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask.cli import with_appcontext
from flask_cors import CORS
from dotenv import load_dotenv
from database.db import db
from flask_migrate import Migrate
from database.models import Utilisateurs
from routes.utilisateurs import utilisateurs_bp
from routes.produits import produits_bp
from routes.paniers import paniers_bp
from routes.panier_items import panier_items_bp
from routes.reservations import reservations_bp
from sqlalchemy import create_engine, text
import pymysql

load_dotenv()

def create_db():
    db_uri = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/"
    engine = create_engine(db_uri)
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS brique_buster"))
            print("Base de données 'brique_buster' créée avec succès (ou existe déjà).")
    except Exception as e:
        print(f"Erreur lors de la création de la base de données : {str(e)}")


def load_sql_objects():
    try:
        # Définir le répertoire où se trouvent les fichiers SQL
        sql_dir = os.path.join(os.path.dirname(__file__), 'sql')

        # Liste des fichiers SQL à charger
        sql_files = ['triggers.sql', 'functions.sql', 'procedures.sql']

        # Paramètres de connexion
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_NAME')

        import subprocess

        for file_name in sql_files:
            file_path = os.path.abspath(os.path.join(sql_dir, file_name))

            if not os.path.exists(file_path):
                print(f"Fichier {file_name} non trouvé dans {sql_dir}")
                continue

            # Construire la commande MySQL
            cmd = [
                "mysql",
                f"-h{host}",
                f"-u{user}",
                f"-p{password}",
                database,
                "-e", f"source {file_path}"
            ]

            try:
                # Exécuter la commande
                process = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True
                )

                if process.returncode == 0:
                    print(f"{file_name} chargé avec succès!")
                else:
                    print(f"Erreur lors du chargement de {file_name}:")
                    print(process.stderr)

            except Exception as e:
                print(f"Erreur pour {file_name}: {str(e)}")

        print("Chargement des objets SQL terminé.")

    except Exception as e:
        print(f"Erreur globale: {str(e)}")

app = Flask(__name__)
CORS(app, origin='http://localhost:5174')
migrate = Migrate(app, db)

app.config.from_object('config.Config')

db.init_app(app)

app.register_blueprint(utilisateurs_bp, url_prefix='/utilisateurs', name='utilisateurs_bp')
app.register_blueprint(produits_bp, url_prefix='/produits', name='produits_bp')
app.register_blueprint(paniers_bp, url_prefix='/paniers', name='paniers_bp')
app.register_blueprint(panier_items_bp, url_prefix='/panier_items', name='panier_items_bp')
app.register_blueprint(reservations_bp, url_prefix="/reservations")

@click.command(name='init_db')
@with_appcontext
def init_db():
    """Crée la base de données et initialise les tables"""
    create_db()
    with app.app_context():
        db.create_all()
        load_sql_objects()
        try:
            # Charger le module seed.py
            seed_path = os.path.join(os.path.dirname(__file__), "scripts", "seed.py")
            spec = importlib.util.spec_from_file_location("seed", seed_path)
            seed_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(seed_module)
            print("Données initiales chargées avec succès.")
        except Exception as e:
            print(f"Erreur lors du chargement des données initiales: {str(e)}")
    print("Base de données créée et tables initialisées avec succès.")

@click.command(name='start_db')
@with_appcontext
def start_db():
    with app.app_context():
        db.create_all()
        print("Tables créées avec succès.")

@click.command(name='reset_db')
@with_appcontext
def reset_db():
    conn = db.engine.raw_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        db.drop_all()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        db.create_all()
        conn.commit()
        print("Base de données réinitialisée avec succès.")
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la réinitialisation de la base de données : {str(e)}")
    finally:
        cursor.close()
        conn.close()


@app.route('/')
def index():
    return "Bienvenue sur le serveur de Chez Brique Buster."


app.cli.add_command(reset_db)
app.cli.add_command(start_db)
app.cli.add_command(init_db)

if __name__ == '__main__':
    app.run(debug=True)
