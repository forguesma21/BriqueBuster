from database.db import db
from sqlalchemy import text

def rechercher_produits_par_nom(terme: str):
    try:
        result = db.session.execute(
            text("CALL RechercherProduitsParNom(:terme)"),
            {"terme": terme}
        )

        produits = [dict(row._mapping) for row in result]
        return {
            "success": True,
            "produits": produits
        }

    except Exception as e:
        error_message = str(e)
        print("🔍 Erreur SQL RechercherProduitsParNom :", error_message)

        return {
            "success": False,
            "message": "Une erreur est survenue lors de la recherche."
        }

def obtenir_tous_les_produits():
    try:
        result = db.session.execute(text("CALL GetAllProduits()"))
        produits = [dict(row._mapping) for row in result]
        return {
            "success": True,
            "produits": produits,
            "nombreProduit": len(produits)
        }
    except Exception as e:
        print("🛑 Erreur SQL GetAllProduits:", str(e))
        return {
            "success": False,
            "message": "Erreur lors de la récupération des produits."
        }