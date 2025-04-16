import type * as specialType from '@/SpecialType'

const SERVEUR = 'http://127.0.0.1:5000/'

export async function obtenirUtilisateur(utilisateurID: string): Promise<specialType.Utilisateur> {
  const requete = new Request(SERVEUR + 'utilisateurs/' + utilisateurID + '/', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  })

  const resultat = await fetch(requete)
  if (resultat.status != 200) {
    throw new Error("Impossible d'obtenir les informations de l'utilisateur pour le moment.")
  } else {
    return (await resultat.json()) as specialType.Utilisateur
  }
}
