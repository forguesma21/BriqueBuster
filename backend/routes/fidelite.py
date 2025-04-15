from flask import Blueprint, jsonify
from database.queries.fidelite_queries import obtenir_categories_fidelite

fidelite_bp = Blueprint("fidelite", __name__)

@fidelite_bp.route("/categories", methods=["GET"])
def get_categories_fidelite():
    categories = obtenir_categories_fidelite()
    return jsonify(categories), 200
