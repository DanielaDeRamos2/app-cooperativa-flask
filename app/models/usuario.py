from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class TipoUsuario(enum.Enum):
    ADMIN = "Administrador"
    PRODUTOR = "Produtor"
    CLIENTE = "Cliente"
    VISITANTE = "Visitante"

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.Enum(TipoUsuario), default=TipoUsuario.VISITANTE)
    ativo = db.Column(db.Boolean, default=True)

    # relacionamento com cliente e produtor
    produtor = db.relationship("Produtor", back_populates="usuario", uselist=False)
    cliente = db.relationship("Cliente", back_populates="usuario", uselist=False)

    def set_password(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))
