import axios from 'axios';
const API_URL = "http://localhost:5000/utilisateurs";

export async function inscriptionUtilisateur(utilisateur) {
   try {
        const response = await axios.post(`${API_URL}/inscription`, utilisateur, {
            headers: {
                'Content-Type': 'application/json'
            },
            timeout: 5000 // Timeout de 5 secondes
        });

        return response.data;
   }catch(error){
       if (error.response) {
            // Le backend a répondu avec un code d'erreur (ex: 400, 500)
            throw new Error(error.response.data.message || "Erreur lors de l'inscription.");
   }}
}

export async function connexionUtilisateur(utilisateur) {
    try {
        const response = await axios.post(`${API_URL}/connexion`, utilisateur, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return response.data;
    }catch(error){
    if (error.response) {
            // Le backend a répondu avec un code d'erreur (ex: 400, 500)
            throw new Error(error.response.data.message || "Erreur.");
    }
    }}
