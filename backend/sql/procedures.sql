-- backend/scripts/procedures.sql
DROP PROCEDURE IF EXISTS AjoutPanier;
DROP PROCEDURE IF EXISTS ObtenirPanier;
DROP PROCEDURE IF EXISTS CreerReservation;

DELIMITER //

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
        SET MESSAGE_TEXT = 'Le produit spécifié n\'existe pas.';
    ELSEIF stockDisponible < quantiteAjoutee THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantité demandée supérieure au stock disponible.';
    END IF;

     -- Vérifie si le produit existe déjà dans le panier
    SELECT COUNT(*) INTO itemCount
    FROM panier_items
    WHERE panier_id = panierID AND produit_id = produitID;

    IF itemCount > 0 THEN
        -- Si le produit est déjà dans le panier, on met à jour la quantité
        UPDATE panier_items
        SET quantite = quantite + quantiteAjoutee
        WHERE panier_id = panierID AND produit_id = produitID;
    ELSE
        -- Sinon, on ajoute le produit au panier
        INSERT INTO panier_items (panier_id, produit_id, quantite)
        VALUES (panierID, produitID, quantiteAjoutee);
    END IF;

END;


CREATE PROCEDURE ObtenirPanier(IN userID VARCHAR(36))
proc_label: BEGIN
    DECLARE panierID VARCHAR(36);

    -- Trouver l'id du panier de l'utilisateur
    SELECT id INTO panierID FROM paniers WHERE user_id = userID LIMIT 1;

    IF panierID IS NULL THEN
        SELECT 'Aucun panier trouvé pour cet utilisateur' AS message;
        LEAVE proc_label;
    END IF;

    -- Récupérer les produits du panier
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

END;

//

DELIMITER ;
