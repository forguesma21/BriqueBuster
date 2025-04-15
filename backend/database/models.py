import uuid

from database.db import db

class Utilisateurs(db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    courriel = db.Column(db.String(100), unique=True, nullable=False)

class Produits(db.Model):
    __tablename__ = 'produits'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    categorie = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    prix = db.Column(db.Float, nullable=False)
    longueur = db.Column(db.Integer, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    en_stock = db.Column(db.Integer)

class Paniers(db.Model):
    __tablename__ = 'paniers'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('utilisateurs.id'), nullable=False)

class PaniersProduits(db.Model):
    __tablename__ = 'panier_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    panier_id = db.Column(db.String(36), db.ForeignKey('paniers.id'), nullable=False)
    produit_id = db.Column(db.String(36), db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

class Reservations(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('utilisateurs.id'), nullable=False)
    date_reservation = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    montant_total = db.Column(db.Numeric(10, 2), nullable=False)

class Fidelite(db.Model):
    __tablename__ = 'fidelite'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('utilisateurs.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie_fidelite.id'), nullable=True, default=1)

class CategorieFidelite(db.Model):
    __tablename__ = 'categorie_fidelite'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    seuil_minimum = db.Column(db.Integer, nullable=False)

class Reservations_items(db.Model):
    __tablename__ = 'reservations_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reservation_id = db.Column(db.String(36), db.ForeignKey('reservations.id'), nullable=False)
    produit_id = db.Column(db.String(36), db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
