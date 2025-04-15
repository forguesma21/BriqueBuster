from flask import Blueprint, jsonify, request
from database.queries.produits_queries import rechercher_produits_par_nom, obtenir_tous_les_produits, obtenir_produit_par_id

produits_bp = Blueprint('produits', __name__)

@produits_bp.route('/<int:produitID>', methods=['GET'])
def obtenir_produit(produitID):
    produit = obtenir_produit_par_id(produitID)
    if produit:
        return jsonify(produit), 200
    else:
        return jsonify({"message": "Produit non trouvé"}), 404

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
    if result["success"]:
        return jsonify({
            "produits": result["produits"],
            "nombreProduit": result["nombreProduit"]
        }), 200
    else:
        return jsonify({
            "message": result["message"]
        }), 500

