from database.db import db
from sqlalchemy import text


def ajouter_produit_au_panier(user_id: str, produit_id: str, quantite: int = 1):
    try:

        db.session.execute(
            text("CALL AjoutPanier(:userID, :produitID, :quantite)"),
            {"userID": user_id, "produitID": produit_id, "quantite": quantite}
        )

        db.session.commit()
        return {
            "success": True,
            "message": "Produit ajouté au panier avec succès."
        }

    except Exception as e:
        db.session.rollback()
        error_message = str(e)

        print("🛑 Erreur SQL AjoutPanier :", error_message)

        if "Le produit spécifié n'existe pas" in error_message:
            message = "Ce produit n'existe pas."
        elif "Quantité demandée supérieure au stock disponible" in error_message:
            message = "La quantité demandée dépasse le stock disponible."
        elif "Unknown procedure" in error_message or "doesn't exist" in error_message:
            message = "La procédure AjoutPanier n'existe pas."
        else:
            message = "Une erreur est survenue lors de l’ajout au panier."

        return {
            "success": False,
            "message": message
        }

def obtenir_panier_utilisateur(user_id: str):
    try:
        result = db.session.execute(
            text("CALL ObtenirPanier(:userID)"),
            {"userID": user_id}
        )

        rows = result.fetchall()
        produits = [dict(row._mapping) for row in rows]

        try:
            while result.nextset():
                pass
        except Exception as e:
            print("⚠️ nextset() ignoré :", str(e))

        return {
            "success": True,
            "produits": produits
        }

    except Exception as e:
        error_message = str(e)
        print("🛑 Erreur SQL ObtenirPanier :", error_message)

        return {
            "success": False,
            "message": "Erreur lors de la récupération du panier."
        }


def retirer_produit_du_panier(user_id: str, produit_id: str):
    try:
        db.session.execute(
            text("CALL RetirerDuPanier(:userID, :produitID)"),
            {"userID": user_id, "produitID": produit_id}
        )
        db.session.commit()

        return {
            "success": True,
            "message": "Produit retiré du panier avec succès."
        }

    except Exception as e:
        db.session.rollback()
        print("🛑 Erreur SQL RetirerDuPanier :", str(e))
        return {
            "success": False,
            "message": str(e)
        }
