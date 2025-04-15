from database.db import get_connection

def obtenir_categories_fidelite():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nom, seuil_minimum FROM categorie_fidelite ORDER BY seuil_minimum;")
            result = cursor.fetchall()

            return [
                {
                    "id": row["id"],
                    "nom": row["nom"],
                    "seuil": row["seuil_minimum"]
                }
                for row in result
            ]
    except Exception as e:
        print("🛑 Erreur chargement catégories fidélité :", e)
        return []
    finally:
        conn.close()
