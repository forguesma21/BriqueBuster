from database.db import get_connection

def creer_reservation(user_id: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("CreerReservation", (user_id,))
            conn.commit()
        return {"success": True, "message": "Réservation créée"}
    except Exception as e:
        conn.rollback()
        return {"success": False, "message": str(e)}
    finally:
        conn.close()


def obtenir_historique_reservations(user_id: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("ObtenirHistoriqueReservations", (user_id,))
            rows = cursor.fetchall()

            reservations = {}
            for row in rows:
                res_id = row["reservation_id"]
                if res_id not in reservations:
                    reservations[res_id] = {
                        "id": res_id,
                        "date_reservation": row["date_reservation"],
                        "date_fin": row["date_fin"],
                        "montant_total": float(row["montant_total"]),
                        "produits": []
                    }
                reservations[res_id]["produits"].append({
                    "produit_id": row["produit_id"],
                    "nom": row["produit_nom"],
                    "categorie": row["categorie"],
                    "annee": row["annee"],
                    "prix": float(row["prix"]),
                    "quantite": row["quantite"]
                })

            return {"success": True, "reservations": list(reservations.values())}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()