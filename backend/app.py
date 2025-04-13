import click
import os
import sys

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
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
migrate = Migrate(app, db)

app.config.from_object('config.Config')

db.init_app(app)

app.register_blueprint(utilisateurs_bp, url_prefix='/utilisateurs', name='utilisateurs_bp')
app.register_blueprint(produits_bp, url_prefix='/produits', name='produits_bp')
app.register_blueprint(paniers_bp, url_prefix='/paniers', name='paniers_bp')
app.register_blueprint(panier_items_bp, url_prefix='/paniers_items', name='paniers_items_bp')


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

if __name__ == '__main__':
    app.run(debug=True)
