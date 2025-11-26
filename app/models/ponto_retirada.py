# app/models/ponto_retirada.py
from .base import db

class PontoRetirada(db.Model):
    __tablename__ = "pontos_retirada"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    dias_funcionamento = db.Column(db.String(120))  # "Seg-Sex"
    horarios = db.Column(db.String(120))  # "08:00 - 18:00"

    def __repr__(self):
        return f"<PontoRetirada {self.nome}>"
