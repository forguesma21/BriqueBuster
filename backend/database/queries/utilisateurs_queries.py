from database.models import Utilisateurs
from database.db import db
from sqlalchemy import text


def verifier_utilisateur_existant(courriel: str):
    try:
        result = db.session.execute(
            text("CALL VerifierUtilisateurExistant(:courriel)"),
            {"courriel": courriel}
        )
        return result.fetchone() is not None
    except Exception as e:
        print("Erreur VerifierUtilisateurExistant:", e)
        return False


def ajouter_utilisateur(utilisateur):
    try:
        db.session.execute(
            text("CALL AjouterUtilisateur(:userID, :prenom, :nom, :courriel, :motDePasse)"),
            utilisateur)
        db.session.commit()
        return {"success": True, "utilisateurID": utilisateur["userID"]}
    except Exception as e:
        db.session.rollback()
        print("Erreur AjouterUtilisateur:", e)
        return {"success": False, "message": str(e)}


def obtenir_profil_utilisateur(user_id: str):
    try:
        result = db.session.execute(
            text("CALL ObtenirProfilUtilisateur(:userID)"),
            {"userID": user_id}
        )

        row = result.fetchone()
        if row:
            print("👤 Profil trouvé :", row)

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

def verifier_connexion(courriel: str):
    try:
        result = db.session.execute(
            text("CALL ConnexionUtilisateur(:courriel)"),
            {"courriel": courriel}
        )
        row = result.fetchone()
        if row:
            return {"id": row.id, "mot_de_passe": row.mot_de_passe}
        return None
    except Exception as e:
        print("Erreur ConnexionUtilisateur:", e)
        return None