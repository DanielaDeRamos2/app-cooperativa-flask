from app import db
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.controllers.carrinhoController import obter_carrinho, calcular_total
from datetime import datetime

def criar_pedido(cliente_id, dados):
    carrinho = obter_carrinho()
    total = calcular_total()

    pedido = Pedido(
        cliente_id=cliente_id,
        forma_pagamento=dados["forma_pagamento"],
        tipo_recebimento=dados["tipo_recebimento"],
        data_agendada=dados.get("data_agendada"),
        observacoes=dados.get("observacoes"),
        total=total
    )

    db.session.add(pedido)
    db.session.commit()

    # Criar itens do pedido
    for pid, item in carrinho.items():
        novo_item = ItemPedido(
            pedido_id=pedido.id,
            produto_id=int(pid),
            quantidade=item["quantidade"],
            preco_unitario=item["preco"]
        )
        db.session.add(novo_item)

    db.session.commit()
    return pedido
