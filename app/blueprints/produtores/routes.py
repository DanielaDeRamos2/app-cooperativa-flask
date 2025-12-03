from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.controllers.produtor_controller import (
    criar_produtor,
    atualizar_status_produtor,
    obter_historico_vendas
)
from app.models.categoria import Categoria
from app.models.produtor import Produtor
from app.decorators import require_role

produtores_bp = Blueprint("produtores", __name__, url_prefix="/produtores")

# RF02.1 - Cadastro de produtor
@produtores_bp.route("/novo", methods=["GET", "POST"])
@login_required
@require_role("Administrador")
def novo_produtor():
    categorias = Categoria.query.all()

    if request.method == "POST":
        dados = {
            "nome": request.form["nome"],
            "cpf": request.form["cpf"],
            "telefone": request.form["telefone"],
            "email": request.form["email"],
            "endereco": request.form["endereco"],
            "certificacoes": request.form.get("certificacoes", ""),
            "descricao": request.form.get("descricao", ""),
            "categorias": request.form.getlist("categorias")
        }

        imagens = request.files.getlist("fotos")

        produtor = criar_produtor(current_user, dados, imagens)
        flash("Produtor cadastrado com sucesso!")
        return redirect(url_for("produtores.lista"))

    return render_template("produtores/novo.html", categorias=categorias)

# RF02.4 - Ativar/desativar produtor
@produtores_bp.route("/status/<int:id>/<acao>")
@login_required
@require_role("Administrador")
def alterar_status(id, acao):
    ativo = True if acao == "ativar" else False
    atualizar_status_produtor(id, ativo)
    flash("Status atualizado.")
    return redirect(url_for("produtores.lista"))

# RF02.3 - Histórico de vendas por produtor
@produtores_bp.route("/vendas/<int:id>")
@login_required
@require_role("Administrador", "Produtor")
def vendas(id):
    vendas = obter_historico_vendas(id)
    return render_template("produtores/vendas.html", vendas=vendas)

# RF02.5 - Perfil público do produtor
@produtores_bp.route("/perfil/<int:id>")
def perfil(id):
    produtor = Produtor.query.get_or_404(id)
    return render_template("produtores/perfil.html", produtor=produtor)

# Lista de produtores
@produtores_bp.route("/")
def lista():
    produtores = Produtor.query.all()
    return render_template("produtores/lista.html", produtores=produtores)
