# app/models/produtor.py
from .base import db

class Produtor(db.Model):
    __tablename__ = "produtores"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(255))
    certificacoes = db.Column(db.String(255))  # texto simples por enquanto
    descricao = db.Column(db.Text)
    foto_principal = db.Column(db.String(255))

    produtos = db.relationship("Produto", backref="produtor", lazy=True)

    def __repr__(self):
        return f"<Produtor {self.nome}>"
