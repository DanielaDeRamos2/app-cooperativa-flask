from app import db
from app.models.produtor import Produtor
from app.models.categoria import Categoria
from app.models.foto_produtor import FotoProdutor
from werkzeug.utils import secure_filename
import os

def criar_produtor(usuario, dados, imagens=None):
    produtor = Produtor(
        usuario_id=usuario.id,
        nome=dados["nome"],
        cpf=dados["cpf"],
        telefone=dados["telefone"],
        email=dados["email"],
        endereco=dados["endereco"],
        certificacoes=dados.get("certificacoes", ""),
        descricao=dados.get("descricao", "")
    )

    # categorias
    categorias_ids = dados.get("categorias", [])
    produtor.categorias = Categoria.query.filter(Categoria.id.in_(categorias_ids)).all()

    db.session.add(produtor)
    db.session.commit()

    # salvar fotos
    if imagens:
        for img in imagens:
            filename = secure_filename(img.filename)
            filepath = os.path.join("app/static/uploads/produtores", filename)
            img.save(filepath)

            foto = FotoProdutor(produtor_id=produtor.id, imagem=filename)
            db.session.add(foto)

        db.session.commit()

    return produtor


def atualizar_status_produtor(produtor_id, ativo):
    produtor = Produtor.query.get(produtor_id)
    produtor.ativo = ativo
    db.session.commit()
    return produtor


def obter_historico_vendas(produtor_id):
    produtor = Produtor.query.get(produtor_id)
    vendas = []

    for produto in produtor.produtos:
        for item in produto.itens:
            vendas.append({
                "produto": produto.nome,
                "quantidade": item.quantidade,
                "valor": item.quantidade * item.preco_unitario,
                "data": item.pedido.data
            })

    return sorted(vendas, key=lambda x: x["data"], reverse=True)
