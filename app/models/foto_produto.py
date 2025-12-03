from app import db

class ImagemProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"))
    caminho = db.Column(db.String(255))
    produto = db.relationship("Produto", back_populates="imagens")
