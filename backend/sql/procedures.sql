-- UTILISATEURS
DROP PROCEDURE IF EXISTS VerifierUtilisateurExistant;
DROP PROCEDURE IF EXISTS AjouterUtilisateur;
DROP PROCEDURE IF EXISTS ObtenirProfilUtilisateur;
DROP PROCEDURE IF EXISTS ConnexionUtilisateur;
DROP PROCEDURE IF EXISTS RechercherProduitsParNom;
DROP PROCEDURE IF EXISTS GetAllProduits;

DELIMITER //

CREATE PROCEDURE VerifierUtilisateurExistant(
    IN email VARCHAR(100)
)
BEGIN
    SELECT id FROM utilisateurs WHERE courriel = email;
END;//

CREATE PROCEDURE AjouterUtilisateur(
    IN userID VARCHAR(36),
    IN prenom VARCHAR(50),
    IN nom VARCHAR(50),
    IN courriel VARCHAR(100),
    IN mot_de_passe VARCHAR(255)
)
BEGIN
    INSERT INTO utilisateurs (id, prenom, nom, courriel, mot_de_passe)
    VALUES (userID, prenom, nom, courriel, mot_de_passe);
END;//

CREATE PROCEDURE ObtenirProfilUtilisateur(IN userID VARCHAR(36))
BEGIN
    SELECT u.prenom, u.nom, u.courriel, cf.nom as statut, f.points
    FROM utilisateurs u
    JOIN fidelite f ON f.user_id = u.id
    JOIN categorie_fidelite cf ON f.categorie_id = cf.id
    WHERE u.id = userID;
END;//

CREATE PROCEDURE ConnexionUtilisateur(IN courriel VARCHAR(100))
BEGIN
    SELECT id, mot_de_passe FROM utilisateurs WHERE utilisateurs.courriel = courriel;
END;//

-- PANIER
DROP PROCEDURE IF EXISTS AjoutPanier;
DROP PROCEDURE IF EXISTS ObtenirPanier;
DROP PROCEDURE IF EXISTS RetirerDuPanier;

CREATE PROCEDURE AjoutPanier(
    IN userID VARCHAR(36),
    IN produitID VARCHAR(36),
    IN quantiteAjoutee INT
)
BEGIN
    DECLARE panierID VARCHAR(36);
    DECLARE stockDisponible INT;
    DECLARE itemCount INT;

    SELECT id INTO panierID FROM paniers WHERE user_id = userID LIMIT 1;

    SELECT en_stock INTO stockDisponible FROM produits WHERE id = produitID;

    IF stockDisponible IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le produit spécifié n''existe pas.';
    ELSEIF stockDisponible < quantiteAjoutee THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantité demandée supérieure au stock disponible.';
    END IF;

    SELECT COUNT(*) INTO itemCount
    FROM panier_items
    WHERE panier_id = panierID AND produit_id = produitID;

    IF itemCount > 0 THEN
        UPDATE panier_items
        SET quantite = quantite + quantiteAjoutee
        WHERE panier_id = panierID AND produit_id = produitID;
    ELSE
        INSERT INTO panier_items (panier_id, produit_id, quantite)
        VALUES (panierID, produitID, quantiteAjoutee);
    END IF;
END;//

CREATE PROCEDURE ObtenirPanier(IN userID VARCHAR(36))
proc_label: BEGIN
    DECLARE panierID VARCHAR(36);

    SELECT id INTO panierID FROM paniers WHERE user_id = userID LIMIT 1;

    IF panierID IS NULL THEN
        SELECT NULL AS produit_id, NULL AS nom, NULL AS prix, NULL AS quantite, NULL AS en_stock LIMIT 0;
        LEAVE proc_label;
    END IF;

    SELECT
        pi.id as panierItemID,
        pi.produit_id,
        pi.quantite,
        p.nom,
        p.prix,
        p.en_stock
    FROM panier_items pi
    JOIN produits p ON pi.produit_id = p.id
    WHERE pi.panier_id = panierID;
END;//

-- RESERVATIONS
DROP PROCEDURE IF EXISTS CreerReservation;
DROP PROCEDURE IF EXISTS ObtenirHistoriqueReservations;

CREATE PROCEDURE CreerReservation(IN userID VARCHAR(36))
BEGIN
    DECLARE panierID VARCHAR(36);
    DECLARE total NUMERIC(10, 2);
    DECLARE reservationID VARCHAR(36);

    SELECT id INTO panierID FROM paniers WHERE user_id = userID LIMIT 1;

    IF panierID IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Aucun panier trouvé pour cet utilisateur.';
    END IF;

    SELECT SUM(p.quantite * pr.prix) INTO total
    FROM panier_items p
    JOIN produits pr ON p.produit_id = pr.id
    WHERE p.panier_id = panierID;

    IF total IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le panier est vide.';
    END IF;

    INSERT INTO reservations(id, user_id, date_reservation, date_fin, montant_total)
    VALUES (
        UUID(),
        userID,
        NOW(),
        DATE_ADD(NOW(), INTERVAL 7 DAY),
        total
    );

    SELECT id INTO reservationID
    FROM reservations
    WHERE user_id = userID
    ORDER BY date_reservation DESC
    LIMIT 1;

    INSERT INTO reservations_items (reservation_id, produit_id, quantite)
    SELECT reservationID, produit_id, quantite
    FROM panier_items
    WHERE panier_id = panierID;

    DELETE FROM panier_items WHERE panier_id = panierID;
END;//

CREATE PROCEDURE ObtenirHistoriqueReservations(IN userID VARCHAR(36))
BEGIN
    SELECT
        r.id AS reservation_id,
        r.date_reservation,
        r.date_fin,
        r.montant_total,
        ri.produit_id,
        ri.quantite,
        p.nom AS produit_nom,
        p.categorie,
        p.annee,
        p.prix
    FROM reservations r
    JOIN reservations_items ri ON r.id = ri.reservation_id
    JOIN produits p ON p.id = ri.produit_id
    WHERE r.user_id = userID
    ORDER BY r.date_reservation DESC;
END;//


-- PRODUITS
CREATE PROCEDURE RechercherProduitsParNom(IN recherche VARCHAR(255))
BEGIN
    SELECT *
    FROM Produits
    WHERE nom LIKE CONCAT('%', recherche, '%');
END //

CREATE PROCEDURE GetAllProduits()
BEGIN
    SELECT * FROM Produits;
END //

DELIMITER ;
