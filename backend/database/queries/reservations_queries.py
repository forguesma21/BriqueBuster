from sqlalchemy import text
from database.db import db

def creer_reservation(user_id: str):
    try:
        db.session.execute(
            text("CALL CreerReservation(:userID)"),
            {"userID": user_id}
        )
        db.session.commit()

        return {
            "success": True,
            "message": "Réservation créée avec succès."
        }

    except Exception as e:
        db.session.rollback()
        print("🛑 Erreur SQL CreerReservation :", str(e))
        return {
            "success": False,
            "message": str(e)
        }

from sqlalchemy import text
from database.db import db

def obtenir_historique_reservations(user_id: str):
    try:
        result = db.session.execute(
            text("CALL ObtenirHistoriqueReservations(:userID)"),
            {"userID": user_id}
        )

        rows = result.fetchall()
        reservations_dict = {}

        for row in rows:
            res_id = row.reservation_id
            if res_id not in reservations_dict:
                reservations_dict[res_id] = {
                    "id": res_id,
                    "date_reservation": row.date_reservation,
                    "date_fin": row.date_fin,
                    "montant_total": float(row.montant_total),
                    "produits": []
                }

            reservations_dict[res_id]["produits"].append({
                "produit_id": row.produit_id,
                "nom": row.produit_nom,
                "categorie": row.categorie,
                "annee": row.annee,
                "prix": float(row.prix),
                "quantite": row.quantite
            })

        return {
            "success": True,
            "reservations": list(reservations_dict.values())
        }

    except Exception as e:
        print("🛑 Erreur SQL ObtenirHistoriqueReservations :", e)
        return {"success": False, "message": str(e)}
