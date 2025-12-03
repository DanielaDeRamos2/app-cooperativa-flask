from app import db
from app.models.pedido import Pedido
from app.models.pedido_historico import PedidoHistorico

STATUS_VALIDOS = [
    "Aguardando confirmação",
    "Em preparação",
    "Pronto para retirada/entrega",
    "Concluído",
    "Cancelado"
]

def registrar_historico(pedido, novo_status):
    h = PedidoHistorico(
        pedido_id=pedido.id,
        status=novo_status
    )
    db.session.add(h)
    db.session.commit()

def alterar_status(pedido_id, novo_status):
    if novo_status not in STATUS_VALIDOS:
        return False, "Status inválido."

    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return False, "Pedido não encontrado."

    pedido.status = novo_status
    db.session.commit()

    # salvar no histórico
    registrar_historico(pedido, novo_status)
    return True, "Status atualizado."

def dividir_itens_por_produtor(pedido):
    """Retorna itens agrupados por produtor."""
    grupos = {}
    for item in pedido.itens:
        prod_id = item.produto.produtor_id
        if prod_id not in grupos:
            grupos[prod_id] = []
        grupos[prod_id].append(item)
    return grupos

def cancelar_pedido(pedido_id, motivo):
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return False, "Pedido não encontrado."

    if pedido.status in ["Concluído"]:
        return False, "Pedido já concluído — não pode cancelar."

    pedido.status = "Cancelado"
    db.session.commit()

    registrar_historico(pedido, f"Cancelado ({motivo})")
    return True, "Pedido cancelado com sucesso."
