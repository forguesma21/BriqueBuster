from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import Utilisateurs
from database.queries.utilisateurs_queries import verifier_utilisateur_existant, ajouter_utilisateur
from database.queries.utilisateurs_queries import obtenir_profil_utilisateur, verifier_connexion
import uuid


utilisateurs_bp = Blueprint('utilisateurs', __name__)


@utilisateurs_bp.route('/connexion', methods=['POST'])
def connexion():
    data = request.get_json()
    utilisateur = verifier_connexion(data['courriel'])

    if utilisateur :
        print("🔐 Hash stocké :", utilisateur["mot_de_passe"])
        print("🔑 Mot de passe entré :", data["motDePasse"])

    if utilisateur and check_password_hash(utilisateur["mot_de_passe"], data['motDePasse']):
        return jsonify({"utilisateurID": utilisateur["id"]}), 200
    else:
        return jsonify({"message": "Mauvais mot de passe ou courriel."}), 400


@utilisateurs_bp.route('/inscription', methods=['POST'])
def inscription():
    data = request.get_json()
    print("data - INSCRIPTION ", data)

    if verifier_utilisateur_existant(data['courriel']):
        return jsonify({"message": "Un utilisateur avec ce courriel existe déjà."}), 400

    try:
        utilisateur_id = str(uuid.uuid4())
        print("🆔 UUID généré :", utilisateur_id)

        utilisateur = {
            "userID": utilisateur_id,
            "prenom": data["prenom"],
            "nom": data["nom"],
            "courriel": data["courriel"],
            "motDePasse": generate_password_hash(data["motDePasse"]),
        }

        resultat = ajouter_utilisateur(utilisateur)

        if resultat["success"]:
            return jsonify(resultat), 200
        else:
            return jsonify(resultat), 500
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@utilisateurs_bp.route("/<user_id>", methods=["GET"])
def profil_utilisateur(user_id):
    print("🔎 User ID reçu :", user_id)

    result = obtenir_profil_utilisateur(user_id)
    print("Résultat obtenu :", result)

    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify({"message": result["message"]}), 404