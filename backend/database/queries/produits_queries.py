from database.db import get_connection

def rechercher_produits_par_nom(terme: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("RechercherProduitsParNom", (terme,))
            result = cursor.fetchall()
            produits = [dict(row) for row in result]

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
    finally:
        conn.close()

def obtenir_tous_les_produits():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("GetAllProduits")
            result = cursor.fetchall()

            produits = [dict(row) for row in result]

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
    finally:
        conn.close()

def obtenir_produit_par_id(produit_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("GetProduitByID", (produit_id,))
            result = cursor.fetchone()

            if not result:
                return None

            return {
                "id": result["id"],
                "nom": result["nom"],
                "prix": result["prix"],
                "description": result["description"],
                "categorie": result["categorie"],
                "annee": result["annee"],
                "longueur": result["longueur"],
                "enStock": result["en_stock"]
            }
    except Exception as e:
        print("🛑 Erreur GetProduitByID:", str(e))
        return None
    finally:
        conn.close()