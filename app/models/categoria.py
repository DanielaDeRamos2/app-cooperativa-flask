# app/models/categoria.py
from .base import db

class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.String(255))
    icone = db.Column(db.String(100))

    produtos = db.relationship("Produto", backref="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.nome}>"
