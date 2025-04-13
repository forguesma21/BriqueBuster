from database.db import db
from database.models import CategorieFidelite

def obtenir_categories_fidelite():
    try:
        categories = CategorieFidelite.query.order_by(CategorieFidelite.seuil_minimum).all()
        return [
            {
                "id": cat.id,
                "nom": cat.nom,
                "seuil": cat.seuil_minimum
            }
            for cat in categories
        ]
    except Exception as e:
        print("🛑 Erreur chargement catégories fidélité :", e)
        return []
