from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.decorators import require_role
from app.models.pedido import Pedido
from app.controllers.pedido_gestao_controller import alterar_status, dividir_itens_por_produtor, cancelar_pedido

admin_pedidos_bp = Blueprint("admin_pedidos", __name__, url_prefix="/admin/pedidos")

# RF05.1 - lista com filtro por status
@admin_pedidos_bp.route("/")
@login_required
@require_role("Administrador")
def lista():
    status = request.args.get("status", "Aguardando confirmação")
    pedidos = Pedido.query.filter_by(status=status).all()
    return render_template("admin/pedidos/lista.html", pedidos=pedidos, status=status)

# RF05.2 - atualizar status
@admin_pedidos_bp.route("/status/<int:id>", methods=["POST"])
@login_required
@require_role("Administrador")
def atualizar_status(id):
    novo = request.form["status"]
    ok, msg = alterar_status(id, novo)
    flash(msg)
    return redirect(request.referrer)

# RF05.3 - divisão automática de pedido por produtor
@admin_pedidos_bp.route("/divisao/<int:id>")
@login_required
@require_role("Administrador")
def divisao_produtores(id):
    pedido = Pedido.query.get_or_404(id)
    grupos = dividir_itens_por_produtor(pedido)
    return render_template("admin/pedidos/divisao.html", pedido=pedido, grupos=grupos)

# RF05.7 - cancelamento
@admin_pedidos_bp.route("/cancelar/<int:id>", methods=["POST"])
@login_required
@require_role("Administrador")
def cancelar(id):
    motivo = request.form["motivo"]
    ok, msg = cancelar_pedido(id, motivo)
    flash(msg)
    return redirect(url_for("admin_pedidos.lista"))
