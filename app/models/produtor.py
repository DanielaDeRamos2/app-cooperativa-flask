from app import db
from datetime import datetime

produtor_categoria = db.Table(
    "produtor_categoria",
    db.Column("produtor_id", db.Integer, db.ForeignKey("produtor.id")),
    db.Column("categoria_id", db.Integer, db.ForeignKey("categoria.id"))
)

class Produtor(db.Model):
    __tablename__ = "produtor"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), unique=True)

    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    endereco = db.Column(db.Text, nullable=False)
    certificacoes = db.Column(db.Text)
    descricao = db.Column(db.Text)

    fotos = db.relationship("FotoProdutor", backref="produtor", lazy=True)

    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship("Usuario", back_populates="produtor")
    categorias = db.relationship("Categoria", secondary=produtor_categoria, back_populates="produtores")
    produtos = db.relationship("Produto", back_populates="produtor")

    def total_vendas(self):
        total = 0
        for produto in self.produtos:
            for item in produto.itens:
                total += item.preco_unitario * item.quantidade
        return total
