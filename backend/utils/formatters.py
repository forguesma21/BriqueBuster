def formatter_info_utilisateur(utilisateur, panier):
    return {
        "prenom": utilisateur.prenom,
        "nom": utilisateur.nom,
        "courriel": utilisateur.courriel,
        "panier": panier
    }

def formatter_info_produit(produit):
    return {
        "produitID": produit.id,
        "categorie": produit.categorie,
        "nom": produit.nom,
        "description": produit.description,
        "prix": produit.prix,
        "annee": produit.annee,
        "longueur": produit.longueur,
        "enStock": produit.en_stock,
    }
