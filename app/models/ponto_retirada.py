from app import db

class PontoRetirada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    dias_funcionamento = db.Column(db.String(255))  # Ex: "Seg-Sex"
    horarios = db.Column(db.String(255))            # Ex: "08:00 - 18:00"
    taxa_entrega = db.Column(db.Float, default=0)   # opcional
