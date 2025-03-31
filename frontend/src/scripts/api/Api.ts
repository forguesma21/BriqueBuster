import type * as specialType from "@/SpecialType.js"

const SERVEUR = "http://127.0.0.1:5000/";

export async function connexion(courriel: string, motDePasse: string): Promise<specialType.utilisateurID> {
    const requete = new Request((SERVEUR+"connexion"), {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: window.JSON.stringify({
            courriel : courriel,
            motDePasse: motDePasse
        }),
    });

    const resultat = await fetch(requete);
    
    if(resultat.status != 200){
        throw new Error("Le courriel ou le mot de passe de l'utilisateur n'est pas valide.");
    } else {
        return (await resultat.json()) as specialType.utilisateurID;
    }
}

export async function inscription(prenom: string, nom: string, nomUtilisateur: string, courriel: string, motDePasse: string, dateNaissance: string): Promise<specialType.utilisateurID> {
    const requete = new Request((SERVEUR+"inscription"), {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: window.JSON.stringify({
            prenom: prenom,
            nom: nom,
            nomUtilisateur: nomUtilisateur,
            courriel : courriel,
            motDePasse: motDePasse,
            dateNaissance: dateNaissance,
        }),
    });

    const resultat = await fetch(requete);
    
    if(resultat.status != 200){
        throw new Error("Le courriel est déjà utilisé par un autre utilisateur.");
    } else {
        return (await resultat.json()) as specialType.utilisateurID;
    }
}

export async function obtenirUtilisateur(utilisateurID: string): Promise<specialType.Utilisateur> {
    const requete = new Request((SERVEUR+"utilisateurs/"+utilisateurID+"/"), {
        method: "GET",
        headers: { "Content-Type": "application/json"}
    });

    const resultat = await fetch(requete);
    if(resultat.status != 200){
        throw new Error("Impossible d'obtenir les informations de l'utilisateur pour le moment.");
    } else {
        return (await resultat.json()) as specialType.Utilisateur;
    }
}

export async function obtenirProduit(produitID: string): Promise<specialType.Produit> {
    const requete = new Request((SERVEUR+"produits/"+produitID+"/"), {
        method: "GET",
        headers: { "Content-Type": "application/json"}
    });

    const resultat = await fetch(requete);
    if(resultat.status != 200){
        throw new Error("Impossible d'obtenir les informations du produit pour le moment.");
    } else {
        return (await resultat.json()) as specialType.Produit;
    }
}

export async function obtenirTousLesProduit(): Promise<specialType.ListeProduits> {
    const requete = new Request((SERVEUR+"produits"), {
        method: "GET",
        headers: { "Content-Type": "application/json"}
    });

    const resultat = await fetch(requete);
    
    if(resultat.status != 200){
        throw new Error("Impossible d'obtenir les informations des produits pour le moment.");
    } else {
        return (await resultat.json()) as specialType.ListeProduits;
    }
}

export async function acheterPanier(utilisateurID: string): Promise<specialType.Utilisateur> {
    const requete = new Request((SERVEUR+"utilisateurs/panier"), {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: window.JSON.stringify({
            utilisateurID: utilisateurID
        }),
    });

    const resultat = await fetch(requete);
    
    if(resultat.status != 200){
        throw new Error("Impossible de passer la commande pour le moment.");
    } else {
        return (await resultat.json()) as specialType.Utilisateur;
    }
}

export async function ajouterProduitPanier(produitID: string, utilisateurID: string): Promise<specialType.Utilisateur> {
    const requete = new Request((SERVEUR+"utilisateurs/panier"), {
        method: "PUT",
        headers: { "Content-Type": "application/json"},
        body: window.JSON.stringify({
            utilisateurID: Number(utilisateurID),
            produitID: Number(produitID)
        }),
    });

    const resultat = await fetch(requete);
    
    if(resultat.status != 200){
        throw new Error("Impossible d'ajouter le produit dans le panier pour le moment.");
    } else {
        return (await resultat.json()) as specialType.Utilisateur;
    }
}

export async function enleverProduitPanier(produitID: string, utilisateurID: string): Promise<specialType.Utilisateur> {
    const requete = new Request((SERVEUR+"utilisateurs/panier"), {
        method: "DELETE",
        headers: { "Content-Type": "application/json"},
        body: window.JSON.stringify({
            utilisateurID: utilisateurID,
            produitID: produitID
        }),
    });

    const resultat = await fetch(requete);
    
    if(resultat.status != 200){
        throw new Error("Impossible d'enlever le produit du panier pour le moment.");
    } else {
        return (await resultat.json()) as specialType.Utilisateur;
    }
}