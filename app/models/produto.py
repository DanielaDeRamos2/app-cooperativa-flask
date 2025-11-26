# app/models/produto.py
from .base import db
from sqlalchemy.dialects.postgresql import JSON

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(20), nullable=False)

    produtor_id = db.Column(db.Integer, db.ForeignKey("produtores.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)

    estoque = db.Column(db.Integer, default=0)
    imagens = db.Column(JSON)  # lista de URLs
    tags = db.Column(db.String(255))  # orgânico, artesanal, etc.

    itens_pedido = db.relationship("ItemPedido", backref="produto", lazy=True)

    def __repr__(self):
        return f"<Produto {self.nome}>"
