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
