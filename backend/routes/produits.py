from flask import Blueprint, jsonify
from database.models import Produits
from utils.formatters import formatter_info_produit

produits_bp = Blueprint('produits', __name__)

@produits_bp.route('/', methods=['GET'])
def obtenir_tous_les_produits():
    produits = Produits.query.all()
    return jsonify({"produits": [formatter_info_produit(p) for p in produits], "nombreProduit": len(produits)}), 200

@produits_bp.route('/<int:produitID>', methods=['GET'])
def obtenir_produit(produitID):
    produit = Produits.query.get_or_404(produitID)
    return jsonify(formatter_info_produit(produit)), 200

