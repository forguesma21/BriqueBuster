from database.db import get_connection

def verifier_utilisateur_existant(courriel: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("VerifierUtilisateurExistant", (courriel,))
            result = cursor.fetchone()
            return result["id"] if result else None
    finally:
        conn.close()


def ajouter_utilisateur(user_id, prenom, nom, courriel, mot_de_passe):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("AjouterUtilisateur", (user_id, prenom, nom, courriel, mot_de_passe))
            conn.commit()
            return {"success": True, "utilisateurID": user_id}
    except Exception as e:
        print("🛑 Erreur AjouterUtilisateur:", e)
        return False
    finally:
        conn.close()


def obtenir_profil_utilisateur(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("ObtenirProfilUtilisateur", (user_id,))
            row = cursor.fetchone()

            if row:
                return {
                    "success": True,
                    "profil": dict(row)
                }
            else:
                return {
                    "success": False,
                    "message": "Utilisateur non trouvé."
                }
    except Exception as e:
        print("🛑 Erreur SQL ObtenirProfilUtilisateur :", e)
        return {
            "success": False,
            "message": str(e)
        }
    finally:
        conn.close()

def verifier_connexion(courriel):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("ConnexionUtilisateur", (courriel,))
            return cursor.fetchone()
    finally:
        conn.close()
