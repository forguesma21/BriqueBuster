from flask import Blueprint, request, jsonify
from database.queries.reservations_queries import creer_reservation
from database.queries.reservations_queries import obtenir_historique_reservations

reservations_bp = Blueprint("reservations", __name__)

@reservations_bp.route("/creer", methods=["POST"])
def creer_reservation_route():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"message": "Champ user_id requis"}), 400

    result = creer_reservation(user_id)

    if result["success"]:
        return jsonify({"message": result["message"]}), 200
    else:
        return jsonify({"message": result["message"]}), 400

@reservations_bp.route("/utilisateur/<user_id>", methods=["GET"])
def historique_reservations(user_id):
    result = obtenir_historique_reservations(user_id)
    if result["success"]:
        return jsonify(result["reservations"]), 200
    return jsonify({"message": result["message"]}), 400
