from app import db
from datetime import datetime

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(20), nullable=False)   # kg, un, L, dz etc.

    estoque = db.Column(db.Float, default=0)
    disponivel = db.Column(db.Boolean, default=True)

    # Sazonalidade
    inicio_sazonal = db.Column(db.Date)
    fim_sazonal = db.Column(db.Date)

    # Promoções
    promocao = db.Column(db.Boolean, default=False)
    preco_promocional = db.Column(db.Float)

    # Tags (orgânico, artesanal etc.)
    tags = db.Column(db.String(200))

    # Chaves estrangeiras
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))
    produtor_id = db.Column(db.Integer, db.ForeignKey("produtor.id"))

    categoria = db.relationship("Categoria", back_populates="produtos")
    produtor = db.relationship("Produtor", back_populates="produtos")
    imagens = db.relationship("ImagemProduto", back_populates="produto", lazy=True)

    itens = db.relationship("ItemPedido", back_populates="produto")  # histórico de vendas
