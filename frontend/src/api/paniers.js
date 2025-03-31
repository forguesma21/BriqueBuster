import axios from 'axios';

const API_URL = 'http://localhost:5000/paniers';  // Remplace par l'URL de ton serveur Flask

export async function obtenirPanier(userID) {
    try {
        const response = await axios.get(`${API_URL}/utilisateur/${userID}`);
        return response.data;  // Retourne un objet contenant {produits, total}
    } catch (error) {
        console.error("Erreur lors de la récupération du panier :", error);
        throw error;
    }
}
