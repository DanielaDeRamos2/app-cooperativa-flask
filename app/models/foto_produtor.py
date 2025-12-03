from app import db

class FotoProdutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produtor_id = db.Column(db.Integer, db.ForeignKey("produtor.id"))
    imagem = db.Column(db.String(255))
