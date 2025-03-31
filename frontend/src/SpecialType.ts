export type Produit = {
    produitID: number;
    categorie: string;
    nom: string;
    description: string;
    prix: number;
    longueur: number;
    annee: number;
    enStock: number;
}

export type ListeProduits = {
    produits: Produit[];
    nombreProduit: number;
}

export type Vin = {
    cepage: string | null;
    sucre: number | null;
    pastille: string | null;
}

export type Utilisateur = {
    prenom: string;
    nom: string;
    courriel: string;
    panier: Panier;
    nombreProduitAchete: number;
    totalVente: number;
}

export type utilisateurID = {
    utilisateurID: string;
}

export type infoUtilisateur = {
    prenom: string;
    nom: string;
}

export type Panier = {
    produits: ProduitPanier[];
    coutTotal: number;
}

export type ProduitPanier = {
    produitID: string;
    nomProduit: string;
    quantite: number;
    prix: number;
}