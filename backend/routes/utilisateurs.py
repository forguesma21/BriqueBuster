from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import Utilisateurs
from database.queries.utilisateurs_queries import verifier_utilisateur_existant, ajouter_utilisateur
from database.queries.utilisateurs_queries import obtenir_profil_utilisateur

utilisateurs_bp = Blueprint('utilisateurs', __name__)


@utilisateurs_bp.route('/connexion', methods=['POST'])
def connexion():
    data = request.get_json()

    utilisateur = Utilisateurs.query.filter_by(courriel=data['courriel']).first()

    if utilisateur and check_password_hash(utilisateur.mot_de_passe, data['motDePasse']):
        return jsonify({"utilisateurID": utilisateur.id}), 200
    else:
        return jsonify({"message": "Mauvais mot de passe ou courriel."}), 400


@utilisateurs_bp.route('/inscription', methods=['POST'])
def inscription():
    data = request.get_json()

    if verifier_utilisateur_existant(data['courriel']):
        return jsonify({"message": "Un utilisateur avec ce courriel existe déjà."}), 400

    try:
        utilisateur = Utilisateurs(
            prenom=data['prenom'],
            nom=data['nom'],
            mot_de_passe=generate_password_hash(data['motDePasse']),
            courriel=data['courriel']
        )

        resultat = ajouter_utilisateur(utilisateur)

        if resultat["success"]:
            return jsonify(resultat), 200
        else:
            return jsonify(resultat), 500
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@utilisateurs_bp.route("/<user_id>", methods=["GET"])
def profil_utilisateur(user_id):
    result = obtenir_profil_utilisateur(user_id)
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify({"message": result["message"]}), 404