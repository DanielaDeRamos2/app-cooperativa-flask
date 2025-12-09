from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.categoria import Categoria

categorias_bp = Blueprint("categorias", __name__, url_prefix="/categorias")

@categorias_bp.route("/")
@login_required
def lista():
    categorias = Categoria.query.all()
    return render_template("categorias/lista.html", categorias=categorias)

@categorias_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form.get("descricao", "")
        cat = Categoria(nome=nome, descricao=descricao)
        # db.session.add(cat)
        # db.session.commit()
        flash("Categoria criada com sucesso!")
        return redirect(url_for("categorias.lista"))
    return render_template("categorias/novo.html")

@categorias_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    cat = Categoria.query.get_or_404(id)
    if request.method == "POST":
        cat.nome = request.form["nome"]
        cat.descricao = request.form.get("descricao", "")
        # db.session.commit()
        flash("Categoria atualizada!")
        return redirect(url_for("categorias.lista"))
    return render_template("categorias/editar.html", categoria=cat)
