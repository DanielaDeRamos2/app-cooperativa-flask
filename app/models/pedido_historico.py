from app import db
from datetime import datetime

class PedidoHistorico(db.Model):
    __tablename__ = "pedido_historico"
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"))
    status = db.Column(db.String(50))
    data = db.Column(db.DateTime, default=datetime.utcnow)

    pedido = db.relationship("Pedido", backref="historico")
