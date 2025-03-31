from flask import Blueprint, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

paniers_bp = Blueprint('paniers', __name__)


@paniers_bp.route('/utilisateur/<user_id>', methods=['GET'])
def obtenir_panier(user_id):
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor(dictionary=True)

        cursor.callproc('ObtenirPanier', [user_id])

        produits = []
        for result in cursor.stored_results():
            produits = result.fetchall()

        total = sum(item['prix'] * item['quantite'] for item in produits)

        cursor.close()
        connection.close()

        return jsonify({"produits": produits, "total": total}), 200

    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
