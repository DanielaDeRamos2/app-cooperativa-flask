from app import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = "pedido"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))

    data = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Aguardando confirmação")

    forma_pagamento = db.Column(db.String(50))    # dinheiro, pix, cartão
    tipo_recebimento = db.Column(db.String(50))  # retirada / entrega
    data_agendada = db.Column(db.DateTime)

    total = db.Column(db.Float, default=0)

    observacoes = db.Column(db.Text)

    itens = db.relationship("ItemPedido", back_populates="pedido")
    cliente = db.relationship("Cliente", back_populates="pedidos")
