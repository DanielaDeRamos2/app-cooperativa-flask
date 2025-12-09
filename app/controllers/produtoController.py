from app import db
from app.models.produto import Produto
from app.models.foto_produto import ImagemProduto
from werkzeug.utils import secure_filename
import os

def criar_produto(dados, imagens):
    produto = Produto(
        nome=dados["nome"],
        descricao=dados["descricao"],
        preco=float(dados["preco"]),
        unidade=dados["unidade"],
        estoque=float(dados["estoque"]),
        produtor_id=dados["produtor_id"],
        categoria_id=dados["categoria_id"],
        tags=",".join(dados.get("tags", [])),
        inicio_sazonal=dados.get("inicio_sazonal"),
        fim_sazonal=dados.get("fim_sazonal"),
        promocao=dados.get("promocao", False),
        preco_promocional=dados.get("preco_promocional")
    )

    db.session.add(produto)
    db.session.commit()

    # upload de imagens (máximo 5)
    if imagens:
        for img in imagens[:5]:
            filename = secure_filename(img.filename)
            path = os.path.join("app/static/uploads/produtos", filename)
            img.save(path)
            db.session.add(ImagemProduto(produto_id=produto.id, caminho=filename))

        db.session.commit()

    return produto


def atualizar_produto(produto_id, dados, imagens=None):
    produto = Produto.query.get(produto_id)

    produto.nome = dados["nome"]
    produto.descricao = dados["descricao"]
    produto.preco = float(dados["preco"])
    produto.unidade = dados["unidade"]
    produto.estoque = float(dados["estoque"])
    produto.categoria_id = dados["categoria_id"]
    produto.tags = ",".join(dados.get("tags", []))

    produto.promocao = dados.get("promocao", False)
    produto.preco_promocional = dados.get("preco_promocional")

    # sazonalidade
    produto.inicio_sazonal = dados.get("inicio_sazonal")
    produto.fim_sazonal = dados.get("fim_sazonal")

    # novas imagens
    if imagens:
        for img in imagens[:5]:
            filename = secure_filename(img.filename)
            path = os.path.join("app/static/uploads/produtos", filename)
            img.save(path)
            db.session.add(ImagemProduto(produto_id=produto.id, caminho=filename))

    db.session.commit()
    return produto


def buscar_produtos(filtros):
    query = Produto.query

    if filtros.get("categoria"):
        query = query.filter_by(categoria_id=filtros["categoria"])

    if filtros.get("produtor"):
        query = query.filter_by(produtor_id=filtros["produtor"])

    if filtros.get("tag"):
        tag = filtros["tag"]
        query = query.filter(Produto.tags.contains(tag))

    if filtros.get("min_preco"):
        query = query.filter(Produto.preco >= float(filtros["min_preco"]))

    if filtros.get("max_preco"):
        query = query.filter(Produto.preco <= float(filtros["max_preco"]))

    if filtros.get("texto"):
        texto = filtros["texto"]
        query = query.filter(Produto.nome.ilike(f"%{texto}%"))

    return query.all()
