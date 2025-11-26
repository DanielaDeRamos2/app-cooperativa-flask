# app/models/pedido.py
from .base import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(30), default="aguardando")  # aguardando, preparação, pronto, concluído
    forma_pagamento = db.Column(db.String(20))
    tipo_recebimento = db.Column(db.String(20))  # retirada / entrega
    total = db.Column(db.Float, default=0.0)

    data_agendada = db.Column(db.DateTime)
    observacoes = db.Column(db.Text)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)

    def __repr__(self):
        return f"<Pedido #{self.id}>"
