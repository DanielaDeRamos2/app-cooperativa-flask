# app/models/usuario.py
from .base import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)  # admin, produtor, cliente
    ativo = db.Column(db.Boolean, default=True)

    produtor = db.relationship("Produtor", uselist=False, backref="usuario")
    cliente = db.relationship("Cliente", uselist=False, backref="usuario")

    def __repr__(self):
        return f"<Usuario {self.email}>"
