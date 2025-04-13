-- Triggers pour le système de fidélité
USE brique_buster;

-- Supprime tous les triggers existants avant de les recréer
DROP TRIGGER IF EXISTS create_fidelite;
DROP TRIGGER IF EXISTS update_fidelite
DROP TRIGGER IF EXISTS



DELIMITER //

-- Trigger pour créer une entrée dans la table fidelite lorsque un utilisateur est créé
CREATE TRIGGER create_fidelite
AFTER INSERT ON utilisateurs
FOR EACH ROW
BEGIN
    DECLARE fidelite_id VARCHAR(36);
    SET fidelite_id = UUID();

    INSERT INTO fidelite (id, user_id, points, categorie_id)
    VALUES (fidelite_id, NEW.id, 0, 0);
END;
//

DELIMITER //

-- Trigger pour créer une entrée dans la table pniers lorsque un utilisateur est créé
CREATE TRIGGER create_panier
AFTER INSERT ON utilisateurs
FOR EACH ROW
BEGIN
    DECLARE panier_id VARCHAR(36);
    SET panier_id = UUID();

    INSERT INTO paniers (id, user_id)
    VALUES (panier_id, NEW.id);
END;
//

DELIMITER //

-- Trigger pour mettre à jour les points de fidélité après une réservation
CREATE TRIGGER update_fidelite
AFTER INSERT ON reservations
FOR EACH ROW
BEGIN
    DECLARE total_points INT;
    DECLARE nouvelle_categorie_id INT;

    SET total_points = NEW.montant_total;

    UPDATE fidelite
    SET points = points + total_points
    WHERE user_id = NEW.user_id;

    SELECT id INTO nouvelle_categorie_id
    FROM categorie_fidelite
    WHERE points_requis <= (SELECT points FROM fidelite WHERE user_id = NEW.user_id)
    ORDER BY points_requis DESC
    LIMIT 1;

    UPDATE fidelite
    SET categorie_id = nouvelle_categorie_id
    WHERE user_id = NEW.user_id;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER DecrementeStockApresReservation
AFTER INSERT ON reservations_items
FOR EACH ROW
BEGIN
    UPDATE produits
    SET en_stock = en_stock - NEW.quantite
    WHERE id = NEW.produit_id;
END;
//

DELIMITER ;

