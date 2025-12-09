from app.models.usuario import Usuario, TipoUsuario
from app.models.cliente import Cliente
from app import db, mail
from flask_mail import Message
import re
import secrets

def validar_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def registrar_usuario(email, senha, tipo_usuario, nome=""):
    """RF01.1 - Cadastro com validação de email"""
    # Validar email
    if not validar_email(email):
        return False, "Email inválido."
    
    # Verificar se já existe
    if Usuario.query.filter_by(email=email).first():
        return False, "Email já cadastrado."
    
    # Validar senha
    if len(senha) < 6:
        return False, "Senha deve ter no mínimo 6 caracteres."
    
    try:
        # Criar usuário
        user = Usuario(
            email=email,
            tipo_usuario=TipoUsuario(tipo_usuario),
            ativo=True
        )
        user.set_password(senha)
        db.session.add(user)
        db.session.flush()  # Para obter o ID
        
        # Se for cliente, criar registro de cliente
        if tipo_usuario == "Cliente":
            cliente = Cliente(
                usuario_id=user.id,
                nome=nome or email.split('@')[0],
            )
            db.session.add(cliente)
        
        db.session.commit()
        return True, "Usuário criado com sucesso. Faça login para continuar."
    except Exception as e:
        db.session.rollback()
        return False, f"Erro ao cadastrar: {str(e)}"

def autenticar(email, senha):
    """RF01.2 - Login com verificação de usuario ativo"""
    user = Usuario.query.filter_by(email=email).first()
    
    # Verificar se usuário existe e está ativo
    if not user or not user.ativo:
        return None
    
    # Verificar senha
    if user.check_password(senha):
        return user
    return None

def enviar_email_recuperacao(email):
    """RF01.3 - Recuperação de senha com token"""
    user = Usuario.query.filter_by(email=email).first()
    if not user:
        return False, "Usuário não encontrado."
    
    # Gerar token
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_timestamp = db.func.now()
    db.session.commit()
    
    # Enviar email (placeholder)
    reset_url = f"http://localhost:5000/auth/reset-password/{token}"
    try:
        msg = Message(
            subject="Recuperação de senha - CoopVale",
            recipients=[email],
            body=f"Clique no link para recuperar sua senha: {reset_url}\n\nLink válido por 1 hora."
        )
        # mail.send(msg)  # Descomentado quando configurado
    except:
        pass
    
    return True, "Se o e-mail existir, enviaremos instruções de recuperação."

def resetar_senha(token, nova_senha):
    """RF01.3 - Recuperar senha com token"""
    from datetime import datetime, timedelta
    
    user = Usuario.query.filter_by(reset_token=token).first()
    if not user:
        return False, "Token inválido."
    
    # Verificar se token não expirou (1 hora)
    if user.reset_token_timestamp and (datetime.utcnow() - user.reset_token_timestamp) > timedelta(hours=1):
        return False, "Token expirado. Solicite uma nova recuperação."
    
    if len(nova_senha) < 6:
        return False, "Senha deve ter no mínimo 6 caracteres."
    
    user.set_password(nova_senha)
    user.reset_token = None
    user.reset_token_timestamp = None
    db.session.commit()
    
    return True, "Senha alterada com sucesso. Faça login."


