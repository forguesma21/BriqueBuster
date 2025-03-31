from database.models import Utilisateurs
from database.db import db

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

def recuperer_utilisateur_par_id(utilisateur_id):
    try:
        utilisateur = Utilisateurs.query.get(utilisateur_id)
        if utilisateur:
            return utilisateur
        else:
            return {"success": False, "message": "Utilisateur introuvable."}
    except Exception as e:
        return {"success": False, "message": str(e)}

def lister_utilisateurs():
    try:
        utilisateurs = Utilisateurs.query.all()
        return utilisateurs
    except Exception as e:
        return {"success": False, "message": str(e)}