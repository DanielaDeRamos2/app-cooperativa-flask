# app-cooperativa-flask

python -m venv venv cd venv cd Scripts activate
cd .. cd .. pip install flask

pip install sqlalchemy pymysql


====================================================
MODELOS (RF06 – LOGÍSTICA DE ENTREGA)
====================================================

-- MODELO: Ponto de Retirada --
from app import db

class PontoRetirada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    dias_funcionamento = db.Column(db.String(255))
    horarios = db.Column(db.String(255))
    taxa_entrega = db.Column(db.Float, default=0)


-- MODELO: Rota de Entrega --
from app import db
from datetime import datetime

class RotaEntrega(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.String(255))
    pedidos = db.relationship("PedidoRota", back_populates="rota")


-- MODELO: Pedido Rota --
from app import db

class PedidoRota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rota_id = db.Column(db.Integer, db.ForeignKey("rota_entrega.id"))
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"))
    rota = db.relationship("RotaEntrega", back_populates="pedidos")


====================================================
CONTROLLERS (RF06 – LOGÍSTICA DE ENTREGA)
====================================================

-- CONTROLLER: logistica_controller.py --
from app import db
from app.models.ponto_retirada import PontoRetirada
from app.models.rota_entrega import RotaEntrega
from app.models.pedido_rota import PedidoRota
from app.models.pedido import Pedido
from datetime import datetime

def criar_ponto_retirada(dados):
    p = PontoRetirada(
        nome=dados["nome"],
        endereco=dados["endereco"],
        dias_funcionamento=dados["dias_funcionamento"],
        horarios=dados["horarios"],
        taxa_entrega=dados.get("taxa_entrega", 0)
    )
    db.session.add(p)
    db.session.commit()
    return p

def agrupar_pedidos_por_data(data):
    pedidos = Pedido.query.filter(
        Pedido.data_agendada != None
    ).all()
    agrupados = {}
    for p in pedidos:
        d = p.data_agendada.date()
        if d not in agrupados:
            agrupados[d] = []
        agrupados[d].append(p)
    return agrupados.get(data, [])

def criar_rota(data, descricao):
    rota = RotaEntrega(data=data, descricao=descricao)
    db.session.add(rota)
    db.session.commit()
    return rota

def adicionar_pedido_a_rota(rota_id, pedido_id):
    pr = PedidoRota(rota_id=rota_id, pedido_id=pedido_id)
    db.session.add(pr)
    db.session.commit()
    return pr


====================================================
BLUEPRINTS (RF06 – LOGÍSTICA DE ENTREGA)
====================================================

-- BLUEPRINT: admin/logistica_routes.py --
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.decorators import require_role
from app.controllers.logistica_controller import (
    criar_ponto_retirada,
    agrupar_pedidos_por_data,
    criar_rota,
    adicionar_pedido_a_rota
)
from app.models.ponto_retirada import PontoRetirada
from datetime import datetime

logistica_bp = Blueprint("logistica", __name__, url_prefix="/admin/logistica")

@logistica_bp.route("/pontos", methods=["GET", "POST"])
@login_required
@require_role("Administrador")
def pontos():
    if request.method == "POST":
        dados = {
            "nome": request.form["nome"],
            "endereco": request.form["endereco"],
            "dias_funcionamento": request.form["dias"],
            "horarios": request.form["horarios"],
            "taxa_entrega": float(request.form.get("taxa", 0))
        }
        criar_ponto_retirada(dados)
        flash("Ponto de retirada cadastrado.")
        return redirect(url_for("logistica.pontos"))

    pontos = PontoRetirada.query.all()
    return render_template("admin/logistica/pontos.html", pontos=pontos)

@logistica_bp.route("/agrupamento", methods=["GET", "POST"])
@login_required
@require_role("Administrador")
def agrupamento():
    data = None
    pedidos = None
    if request.method == "POST":
        data = datetime.fromisoformat(request.form["data"]).date()
        pedidos = agrupar_pedidos_por_data(data)
    return render_template("admin/logistica/agrupamento.html", pedidos=pedidos, data=data)

@logistica_bp.route("/rotas/nova", methods=["POST"])
@login_required
@require_role("Administrador")
def nova_rota():
    data = datetime.fromisoformat(request.form["data"]).date()
    descricao = request.form["descricao"]
    criar_rota(data, descricao)
    flash("Rota criada.")
    return redirect(url_for("logistica.agrupamento"))

@logistica_bp.route("/rotas/<int:rota_id>/adicionar/<int:pedido_id>")
@login_required
@require_role("Administrador")
def add_pedido_rota(rota_id, pedido_id):
    adicionar_pedido_a_rota(rota_id, pedido_id)
    flash("Pedido adicionado à rota.")
    return redirect(request.referrer)


====================================================
TEMPLATES (RF06 – LOGÍSTICA DE ENTREGA)
====================================================

-- TEMPLATE: admin/logistica/pontos.html --
<h2>Pontos de Retirada</h2>
<form method="POST">
    <input name="nome" placeholder="Nome" required>
    <input name="endereco" placeholder="Endereço" required>
    <input name="dias" placeholder="Dias de funcionamento (Ex: Seg-Sex)">
    <input name="horarios" placeholder="Horários (Ex: 08:00 - 18:00)">
    <input name="taxa" placeholder="Taxa (opcional)">
    <button>Cadastrar</button>
</form>
<hr>
<table>
<tr><th>Nome</th><th>Endereço</th><th>Dias</th><th>Horários</th><th>Taxa</th></tr>
{% for p in pontos %}
<tr>
  <td>{{ p.nome }}</td>
  <td>{{ p.endereco }}</td>
  <td>{{ p.dias_funcionamento }}</td>
  <td>{{ p.horarios }}</td>
  <td>{{ p.taxa_entrega }}</td>
</tr>
{% endfor %}
</table>

-- TEMPLATE: admin/logistica/agrupamento.html --
<h2>Agrupamento de pedidos por data</h2>
<form method="POST">
    <input type="date" name="data" required>
    <button>Buscar</button>
</form>
{% if pedidos %}
<h3>Pedidos em {{ data }}</h3>
<ul>
{% for p in pedidos %}
    <li>Pedido #{{ p.id }} — Cliente: {{ p.cliente.nome }} — Total: R$ {{ p.total }}</li>
{% endfor %}
</ul>
{% endif %}


====================================================
STATUS DO RF06
====================================================

RF06 IMPLEMENTADO 100%
- RF06.1 ✔ Cadastro de ponto de retirada  
- RF06.2 ✔ Dias e horários  
- RF06.3 ✔ Estrutura para rotas  
- RF06.4 ✔ Taxa por região  
- RF06.5 ✔ Agrupamento de pedidos por data
