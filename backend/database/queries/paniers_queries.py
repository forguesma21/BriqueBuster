from database.db import get_connection

def ajouter_produit_au_panier(user_id: str, produit_id: str, quantite: int = 1):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("AjoutPanier", (user_id, produit_id, quantite))
            conn.commit()
        return {
            "success": True,
            "message": "Produit ajouté au panier avec succès."
        }

    except Exception as e:
        conn.rollback()
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
    finally:
        conn.close()


def obtenir_panier_utilisateur(user_id: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("ObtenirPanier", (user_id,))
            rows = cursor.fetchall()
            produits = [dict(row) for row in rows]

            # 🧼 Nettoyage des résultats restants (évite des erreurs avec certains SGBD)
            try:
                while cursor.nextset():
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
    finally:
        conn.close()


def retirer_produit_du_panier(user_id: str, produit_id: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("RetirerDuPanier", (user_id, produit_id))
            conn.commit()
        return {
            "success": True,
            "message": "Produit retiré du panier avec succès."
        }
    except Exception as e:
        conn.rollback()
        print("🛑 Erreur SQL RetirerDuPanier :", str(e))
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()
