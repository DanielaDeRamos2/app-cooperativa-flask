from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"

    # Importar todos os modelos para que SQLAlchemy conheça-os
    from app.models import (
        usuario, cliente, categoria, produto, produtor, pedido, item_pedido,
        foto_produto, foto_produtor, pedido_historico, ponto_retirada
    )

    # registrar blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.categorias import categorias_bp
    from app.blueprints.produtos import produtos_bp
    from app.blueprints.pedidos import pedidos_bp, carrinho_bp
    from app.blueprints.produtores import produtores_bp, produtor_pedidos_bp
    from app.blueprints.admin import admin_pedidos_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(carrinho_bp)
    app.register_blueprint(produtores_bp)
    app.register_blueprint(produtor_pedidos_bp)
    app.register_blueprint(admin_pedidos_bp)

    return app