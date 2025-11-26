# app/models/item_pedido.py
from .base import db

class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)

    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<ItemPedido {self.id}>"
