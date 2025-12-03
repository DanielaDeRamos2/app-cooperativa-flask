from app.models.usuario import Usuario, TipoUsuario
from app import db, mail
from flask_mail import Message

def registrar_usuario(email, senha, tipo_usuario):
    if Usuario.query.filter_by(email=email).first():
        return False, "Email já cadastrado."

    user = Usuario(
        email=email,
        tipo_usuario=TipoUsuario(tipo_usuario)
    )
    user.set_password(senha)
    db.session.add(user)
    db.session.commit()
    return True, "Usuário criado com sucesso."

def autenticar(email, senha):
    user = Usuario.query.filter_by(email=email).first()
    if user and user.check_password(senha):
        return user
    return None

def enviar_email_recuperacao(email):
    user = Usuario.query.filter_by(email=email).first()
    if not user:
        return False

    msg = Message(
        subject="Recuperação de senha - CoopVale",
        recipients=[email],
        body="Link de recuperação de senha (placeholder)."
    )
    mail.send(msg)
    return True
