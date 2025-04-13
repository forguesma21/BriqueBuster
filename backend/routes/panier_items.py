from flask import Blueprint, request, jsonify
from database.queries.paniers_queries import ajouter_produit_au_panier, obtenir_panier_utilisateur
from database.queries.paniers_queries import retirer_produit_du_panier

panier_items_bp = Blueprint('panier_items', __name__)

@panier_items_bp.route("/ajouter", methods=['POST', 'OPTIONS'])
def ajouter_au_panier():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    print("👉 Données reçues :", data)  # debug 1

    result = ajouter_produit_au_panier(
        data["user_id"],
        data["produit_id"],
        data.get("quantite", 1)
    )

    print("👉 Résultat SQL :", result)  # debug 2

    if result["success"]:
        return jsonify({"message": "Ajouté au panier"}), 200
    else:
        return jsonify({"message": result["message"]}), 400


@panier_items_bp.route("/<user_id>", methods=["GET"])
def afficher_panier(user_id):
    print("🔍 Requête GET /paniers reçue pour user_id :", user_id)

    result = obtenir_panier_utilisateur(user_id)

    print("🧪 Résultat retourné :", result)

    if result["success"]:
        response = jsonify(result["produits"])
        status_code = 200
    else:
        response = jsonify({"message": result["message"]})
        status_code = 400

    return response, status_code


@panier_items_bp.route("/retirer", methods=["DELETE"])
def retirer_du_panier():
    data = request.get_json()
    user_id = data.get("user_id")
    produit_id = data.get("produit_id")

    if not user_id or not produit_id:
        return jsonify({"message": "Champs requis manquants."}), 400

    result = retirer_produit_du_panier(user_id, produit_id)

    if result["success"]:
        return jsonify({"message": result["message"]}), 200
    return jsonify({"message": result["message"]}), 400
