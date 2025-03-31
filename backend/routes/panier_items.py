from flask import Blueprint, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

panier_items_bp = Blueprint('panier_items', __name__)


@panier_items_bp.route('/ajouter', methods=['POST'])
def ajouter():
    data = request.json
    user_id = data['user_id']
    produit_id = data['produit_id']
    quantite = data['quantite']

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        cursor = connection.cursor()

        cursor.callproc('AddToPanier', [user_id, produit_id, quantite])

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Produit ajouté au panier avec succès."}), 200

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
