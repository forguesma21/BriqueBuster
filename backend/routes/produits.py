from flask import Blueprint, jsonify, request
from database.models import Produits
from utils.formatters import formatter_info_produit
from database.queries.produits_queries import rechercher_produits_par_nom, obtenir_tous_les_produits

produits_bp = Blueprint('produits', __name__)

@produits_bp.route('/<int:produitID>', methods=['GET'])
def obtenir_produit(produitID):
    produit = Produits.query.get_or_404(produitID)
    return jsonify(formatter_info_produit(produit)), 200

@produits_bp.route('/recherche', methods=['GET'])
def recherche_par_nom():
    terme = request.args.get('q', '')

    if not terme:
        return jsonify({
            "success": False,
            "message": "Aucun terme de recherche fourni."
        }), 400

    resultats = rechercher_produits_par_nom(terme)
    return jsonify(resultats)

@produits_bp.route('/', methods=['GET'])
def route_obtenir_tous_les_produits():
    result = obtenir_tous_les_produits()
    return jsonify(result), 200 if result["success"] else 500