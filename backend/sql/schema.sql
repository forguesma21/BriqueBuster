DROP TABLE IF EXISTS reservations_items;
DROP TABLE IF EXISTS panier_items;
DROP TABLE IF EXISTS paniers;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS fidelite;
DROP TABLE IF EXISTS utilisateurs;
DROP TABLE IF EXISTS produits;
DROP TABLE IF EXISTS categorie_fidelite;

CREATE TABLE utilisateurs (
    id VARCHAR(36) PRIMARY KEY,
    prenom VARCHAR(50) NOT NULL,
    nom VARCHAR(50) NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    courriel VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE produits (
    id VARCHAR(36) PRIMARY KEY,
    categorie VARCHAR(50) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    prix FLOAT NOT NULL,
    longueur INT NOT NULL,
    annee INT NOT NULL,
    en_stock INT
);

CREATE TABLE paniers (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
);

CREATE TABLE panier_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    panier_id VARCHAR(36) NOT NULL,
    produit_id VARCHAR(36) NOT NULL,
    quantite INT NOT NULL,
    FOREIGN KEY (panier_id) REFERENCES paniers(id),
    FOREIGN KEY (produit_id) REFERENCES produits(id)
);

CREATE TABLE reservations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    date_reservation DATETIME NOT NULL DEFAULT NOW(),
    date_fin DATETIME NOT NULL,
    montant_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
);

CREATE TABLE categorie_fidelite (
    id INT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    seuil_minimum INT NOT NULL
);

CREATE TABLE fidelite (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    points INT DEFAULT 0 NOT NULL,
    categorie_id INT DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES utilisateurs(id),
    FOREIGN KEY (categorie_id) REFERENCES categorie_fidelite(id)
);

CREATE TABLE reservations_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id VARCHAR(36) NOT NULL,
    produit_id VARCHAR(36) NOT NULL,
    quantite INT NOT NULL,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id),
    FOREIGN KEY (produit_id) REFERENCES produits(id)
);
