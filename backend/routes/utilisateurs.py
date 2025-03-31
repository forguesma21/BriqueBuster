from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from database.models import Utilisateurs
from database import db

# Importation des utilitaires
from utils.formatters import formatter_info_utilisateur
from database.queries.utilisateurs_queries import verifier_utilisateur_existant, ajouter_utilisateur

utilisateurs_bp = Blueprint('utilisateurs', __name__)


@utilisateurs_bp.route('/connexion', methods=['POST'])
def connexion():
    data = request.get_json()  # Récupère le body de la requête JSON

    # Recherche l'utilisateur dans la base de données en fonction du courriel
    utilisateur = Utilisateurs.query.filter_by(courriel=data['courriel']).first()

    if utilisateur and check_password_hash(utilisateur.mot_de_passe, data['motDePasse']):
        # Si le mot de passe est correct, retourner l'id de l'utilisateur
        return jsonify({"utilisateurID": utilisateur.id}), 200
    else:
        # Sinon, retourner une erreur
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