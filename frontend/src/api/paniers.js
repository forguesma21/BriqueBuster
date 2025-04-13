import axios from 'axios'

const API_URL = 'http://localhost:5000/panier_items'

export async function ajouterAuPanier(userId, produitId, quantite = 1) {
  const response = await axios.post(`${API_URL}/ajouter`, {
    user_id: userId,
    produit_id: produitId,
    quantite
  })
  return response.data
}

export async function obtenirPanier(userId) {
  const response = await axios.get(`${API_URL}/${userId}`)
  return response.data
}

export async function retirerProduitDuPanier(userId, produitId) {
  try {
    const response = await axios.delete(`${API_URL}/retirer`, {
      data: {
        user_id: userId,
        produit_id: produitId
      }
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Erreur lors du retrait du produit')
  }
}

