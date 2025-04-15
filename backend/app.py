import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.utilisateurs import utilisateurs_bp
from routes.produits import produits_bp
from routes.paniers import paniers_bp
from routes.panier_items import panier_items_bp
from routes.reservations import reservations_bp
from routes.fidelite import fidelite_bp
import pymysql

load_dotenv()

app = Flask(__name__)
CORS(app, origins='http://localhost:5174')

# 📦 Chargement config
app.config.from_object('config.Config')

# ✅ Chargement des routes
app.register_blueprint(utilisateurs_bp, url_prefix='/utilisateurs')
app.register_blueprint(produits_bp, url_prefix='/produits')
app.register_blueprint(paniers_bp, url_prefix='/paniers')
app.register_blueprint(panier_items_bp, url_prefix='/panier_items')
app.register_blueprint(reservations_bp, url_prefix="/reservations")
app.register_blueprint(fidelite_bp, url_prefix="/fidelite")

# 🔨 Fonction d'init SQL
import pymysql
import os

def init_db():
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "brique_buster")

    # 🔹 Étape 1 : Connexion sans base pour créer la base si besoin
    print("📦 Connexion au serveur MySQL...")
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        autocommit=True
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            print(f"✅ Base de données `{db_name}` vérifiée/créée.")
    finally:
        connection.close()

    # 🔹 Étape 2 : Connexion à la base pour créer les tables
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        autocommit=True
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            if len(tables) > 0:
                print("✅ Tables déjà présentes. Pas besoin de recharger.")
                return

            with open("schema.sql", "r", encoding="utf-8") as f:
                sql = f.read()
                cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                for statement in sql.split(";"):
                    if statement.strip():
                        cursor.execute(statement)
                cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            print("✅ Tables créées avec succès.")
    except Exception as e:
        print("🛑 Erreur lors de l'initialisation de la base :", e)
    finally:
        connection.close()

# Route de test
@app.route('/')
def index():
    return "Bienvenue sur le serveur de Chez Brique Buster."

# Lance l'init et le serveur
if __name__ == '__main__':
    init_db()
    app.run(debug=True)