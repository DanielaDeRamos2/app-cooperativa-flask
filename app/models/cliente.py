# app/models/cliente.py
from app import db
from sqlalchemy.dialects.postgresql import JSON

class Cliente(db.Model):
    __tablename__ = "cliente"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    telefone = db.Column(db.String(20))
    enderecos = db.Column(JSON)  # lista de endereços [{rua, numero, bairro, ...}]

    usuario = db.relationship("Usuario", back_populates="cliente")
    pedidos = db.relationship("Pedido", back_populates="cliente", lazy=True)

    def __repr__(self):
        return f"<Cliente {self.nome}>"
