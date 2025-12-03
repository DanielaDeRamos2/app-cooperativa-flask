from app import db

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"))
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"))

    quantidade = db.Column(db.Float, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    pedido = db.relationship("Pedido", back_populates="itens")
    produto = db.relationship("Produto", back_populates="itens")
