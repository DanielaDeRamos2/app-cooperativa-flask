from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.controllers.pedido_controller import criar_pedido
from app.controllers.carrinho_controller import obter_carrinho, calcular_total
from datetime import datetime

pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")

# RF04.7 - resumo e confirmação de pedido
@pedidos_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    carrinho = obter_carrinho()
    total = calcular_total()

    if request.method == "POST":
        dados = {
            "forma_pagamento": request.form["forma_pagamento"],
            "tipo_recebimento": request.form["tipo_recebimento"],
            "data_agendada": datetime.fromisoformat(request.form["data_agendada"]) if request.form["data_agendada"] else None,
            "observacoes": request.form.get("observacoes")
        }

        pedido = criar_pedido(current_user.cliente.id, dados)
        flash("Pedido realizado com sucesso!")
        return redirect(url_for("pedidos.detalhes", id=pedido.id))

    return render_template("pedidos/checkout.html", carrinho=carrinho, total=total)

# RF04.7 - detalhes do pedido
@pedidos_bp.route("/<int:id>")
@login_required
def detalhes(id):
    from app.models.pedido import Pedido
    pedido = Pedido.query.get_or_404(id)
    return render_template("pedidos/detalhes.html", pedido=pedido)

@pedidos_bp.route("/nota/<int:id>")
@login_required
def nota(id):
    from app.models.pedido import Pedido
    pedido = Pedido.query.get_or_404(id)
    return render_template("pedidos/nota.html", pedido=pedido)
