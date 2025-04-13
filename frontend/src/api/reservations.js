import axios from 'axios'

const API_URL = 'http://localhost:5000/reservations'

export async function reserverPanier(userId) {
  try {
    const response = await axios.post(`${API_URL}/creer`, {
      user_id: userId
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Erreur lors de la réservation.')
  }
}

export async function obtenirHistoriqueReservations(userId){
  try {
    const response = await axios.post(`${API_URL}/utilisateur//${userId}`, {
      user_id: userId
    })
    return response.data
  }catch(error){
    throw new Error(error.response?.data?.message || 'Erreur lors de la réservation.')
  }
}