-- sql/functions.sql
DROP FUNCTION IF EXISTS total_utilisateurs;
DROP FUNCTION IF EXISTS calculer_total_reservations;

DELIMITER //

CREATE FUNCTION total_utilisateurs()
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT;
    SELECT COUNT(*) INTO total FROM utilisateurs;
    RETURN total;
END;

CREATE FUNCTION calculer_total_reservations(user_id VARCHAR(36))
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10, 2);
    SELECT SUM(montant_total) INTO total
    FROM reservations
    WHERE user_id = user_id;

    RETURN IFNULL(total, 0);
END;

//
