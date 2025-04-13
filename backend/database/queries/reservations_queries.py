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
