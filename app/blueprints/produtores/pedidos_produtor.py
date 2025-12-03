from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.pedido import Pedido

produtor_pedidos_bp = Blueprint("produtor_pedidos", __name__, url_prefix="/produtor/pedidos")

@produtor_pedidos_bp.route("/")
@login_required
def meus_pedidos():
    produtor_id = current_user.produtor.id
    pedidos = []

    todos = Pedido.query.all()
    for p in todos:
        for item in p.itens:
            if item.produto.produtor_id == produtor_id:
                pedidos.append(p)
                break

    return render_template("produtor/pedidos.html", pedidos=pedidos)
