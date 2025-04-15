import axios from 'axios';
const API_URL = "http://localhost:5000/produits";

export async function recuperer_produits() {
   try {
        const response = await axios.get(`${API_URL}/`);
        return response.data.produits;
   }catch(error){
       if (error.response) {
            throw new Error(error.response.data.message || "Erreur");
   }}
}

export async function recherche_produits(terme) {
  try {
    const response = await axios.get(`${API_URL}/recherche`, {
      params: { q: terme }
    });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la recherche :", error);
    return {
      success: false,
      message: "Erreur lors de la recherche des produits."
    };
  }
}
