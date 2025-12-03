from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.controllers.produto_controller import (
    criar_produto,
    atualizar_produto,
    buscar_produtos
)
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.produtor import Produtor
from app.decorators import require_role

produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")

# RF03.1 - Cadastro de Produto
@produtos_bp.route("/novo", methods=["GET", "POST"])
@login_required
@require_role("Produtor", "Administrador")
def novo_produto():
    categorias = Categoria.query.all()
    produtores = Produtor.query.all()

    if request.method == "POST":
        dados = {
            "nome": request.form["nome"],
            "descricao": request.form["descricao"],
            "preco": request.form["preco"],
            "unidade": request.form["unidade"],
            "estoque": request.form["estoque"],
            "categoria_id": request.form["categoria"],
            "produtor_id": request.form["produtor"],
            "tags": request.form.getlist("tags"),
            "promocao": bool(request.form.get("promocao")),
            "preco_promocional": request.form.get("preco_promocional"),
            "inicio_sazonal": request.form.get("inicio_sazonal"),
            "fim_sazonal": request.form.get("fim_sazonal")
        }

        imagens = request.files.getlist("imagens")

        criar_produto(dados, imagens)
        flash("Produto criado com sucesso.")
        return redirect(url_for("produtos.lista"))

    return render_template("produtos/novo.html", categorias=categorias, produtores=produtores)


# RF03.3 / RF03.6 - Catálogo com filtros
@produtos_bp.route("/")
def lista():
    filtros = {
        "categoria": request.args.get("categoria"),
        "produtor": request.args.get("produtor"),
        "tag": request.args.get("tag"),
        "min_preco": request.args.get("min_preco"),
        "max_preco": request.args.get("max_preco"),
        "texto": request.args.get("q")
    }
    produtos = buscar_produtos(filtros)
    categorias = Categoria.query.all()
    produtores = Produtor.query.all()

    return render_template("produtos/lista.html", produtos=produtos, categorias=categorias, produtores=produtores)


# RF03.5 - Página do produto com sazonalidade, origem etc.
@produtos_bp.route("/<int:id>")
def detalhes(id):
    produto = Produto.query.get_or_404(id)
    return render_template("produtos/detalhes.html", produto=produto)
