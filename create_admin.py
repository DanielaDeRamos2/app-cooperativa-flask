#!/usr/bin/env python
"""
Cria um usuário ADMIN (idempotente). Uso:
    py -3 create_admin.py

Credenciais padrão criadas (se não existirem):
  email: admin@test.local
  senha : Admin123!

Se o usuário existir, o script atualiza a senha para o valor acima.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.usuario import Usuario, TipoUsuario

EMAIL = "admin@test.local"
SENHA = "Admin123!"

app = create_app()
with app.app_context():
    db.create_all()
    user = Usuario.query.filter_by(email=EMAIL).first()
    if user:
        print(f"Usuário existente encontrado: {EMAIL} (id={user.id}). Atualizando senha e tipo para ADMIN.")
        user.set_password(SENHA)
        user.tipo_usuario = TipoUsuario.ADMIN
        user.ativo = True
        db.session.commit()
        print("Senha atualizada.")
    else:
        user = Usuario(email=EMAIL, tipo_usuario=TipoUsuario.ADMIN, ativo=True)
        user.set_password(SENHA)
        db.session.add(user)
        db.session.commit()
        print(f"Usuário admin criado: {EMAIL} (id={user.id})")

    print("\nAgora você pode acessar /auth/login com as credenciais acima.")
