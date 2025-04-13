from flask import Blueprint, request, jsonify
from database.queries.reservations_queries import creer_reservation

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
