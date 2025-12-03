from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.carrinho_controller import (
    adicionar_item, remover_item, editar_quantidade,
    obter_carrinho, calcular_total
)

carrinho_bp = Blueprint("carrinho", __name__, url_prefix="/carrinho")

# RF04.1 - adicionar item
@carrinho_bp.route("/adicionar/<int:id>", methods=["POST"])
def adicionar(id):
    quantidade = float(request.form["quantidade"])
    ok, msg = adicionar_item(id, quantidade)
    flash(msg)
    return redirect(request.referrer)

# RF04.2 - editar quantidades
@carrinho_bp.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    nova_qtd = float(request.form["quantidade"])
    editar_quantidade(id, nova_qtd)
    return redirect(url_for("carrinho.visualizar"))

# RF04.1 - remover
@carrinho_bp.route("/remover/<int:id>")
def remover(id):
    remover_item(id)
    return redirect(url_for("carrinho.visualizar"))

# RF04 - visualizar carrinho
@carrinho_bp.route("/")
def visualizar():
    carrinho = obter_carrinho()
    total = calcular_total()
    return render_template("carrinho/visualizar.html", carrinho=carrinho, total=total)
