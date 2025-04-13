from database.models import Utilisateurs
from database.db import db
from sqlalchemy import text

def verifier_utilisateur_existant(courriel):
    return Utilisateurs.query.filter_by(courriel=courriel).first()

def ajouter_utilisateur(utilisateur):
    try:
        db.session.add(utilisateur)
        db.session.commit()
        return {"success": True, "message": "Utilisateur ajouté avec succès.", "utilisateurID": utilisateur.id}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}

def obtenir_profil_utilisateur(user_id: str):
    try:
        result = db.session.execute(
            text("CALL ObtenirProfilUtilisateur(:userID)"),
            {"userID": user_id}
        )

        row = result.fetchone()
        if row:
            return {
                "success": True,
                "nom": f"{row.prenom} {row.nom}",
                "courriel": row.courriel,
                "points": row.points or 0,
                "statut": row.categorie or "Cassette Basique"
            }
        else:
            return {"success": False, "message": "Utilisateur non trouvé."}

    except Exception as e:
        print("🛑 Erreur SQL ObtenirProfilUtilisateur :", e)
        return {"success": False, "message": str(e)}

def lister_utilisateurs():
    try:
        utilisateurs = Utilisateurs.query.all()
        return utilisateurs
    except Exception as e:
        return {"success": False, "message": str(e)}