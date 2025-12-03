# app/models/categoria.py
from .base import db

class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    icone = db.Column(db.String(100))

    # subcategorias opcionais
    subcategoria = db.Column(db.String(100))

    produtos = db.relationship("Produto", back_populates="categoria")
    produtores = db.relationship("Produtor", secondary="produtor_categoria", back_populates="categorias")

    def __repr__(self):
        return f"<Categoria {self.nome}>"
    