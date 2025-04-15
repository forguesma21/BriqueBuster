import axios from 'axios'

const API_URL = 'http://localhost:5000/fidelite'

export async function obtenirCategorieFidelite() {
  try {
    const response = await axios.get(`${API_URL}/categories`)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Erreur lors du retrait du produit')
  }
}
