from flask import session
from app.models.produto import Produto

def obter_carrinho():
    return session.get("carrinho", {})

def salvar_carrinho(carrinho):
    session["carrinho"] = carrinho
    session.modified = True

def adicionar_item(produto_id, quantidade):
    carrinho = obter_carrinho()

    produto = Produto.query.get(produto_id)

    if not produto:
        return False, "Produto não encontrado."

    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]["quantidade"] += quantidade
    else:
        carrinho[str(produto_id)] = {
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": quantidade,
            "unidade": produto.unidade,
            "produtor_id": produto.produtor_id
        }

    salvar_carrinho(carrinho)
    return True, "Produto adicionado ao carrinho."

def remover_item(produto_id):
    carrinho = obter_carrinho()
    carrinho.pop(str(produto_id), None)
    salvar_carrinho(carrinho)

def editar_quantidade(produto_id, quantidade):
    carrinho = obter_carrinho()
    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]["quantidade"] = quantidade
        salvar_carrinho(carrinho)

def calcular_total():
    carrinho = obter_carrinho()
    return sum(item["preco"] * item["quantidade"] for item in carrinho.values())
