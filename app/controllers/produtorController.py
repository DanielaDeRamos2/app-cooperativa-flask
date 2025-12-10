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
        nome_propriedade=dados.get('nome_propriedade'),
        especialidade=dados.get('especialidade'),
        endereco=dados.get("endereco"),
        certificacoes=dados.get("certificacoes", ""),
        descricao=dados.get("descricao", "")
    )

    # categorias
    categorias_ids = dados.get("categorias", [])
    produtor.categorias = Categoria.query.filter(Categoria.id.in_(categorias_ids)).all()

    db.session.add(produtor)
    db.session.commit()

    # salvar fotos: cria pasta e usa nome único com prefixo do id
    upload_dir = os.path.join('app', 'static', 'uploads', 'produtores')
    os.makedirs(upload_dir, exist_ok=True)

    if imagens:
        for img in imagens:
            if not getattr(img, 'filename', None):
                continue
            filename = secure_filename(img.filename)
            unique_name = f"{produtor.id}_{filename}"
            filepath = os.path.join(upload_dir, unique_name)
            img.save(filepath)

            foto = FotoProdutor(produtor_id=produtor.id, imagem=unique_name)
            db.session.add(foto)

        db.session.commit()

    return produtor


def atualizar_status_produtor(produtor_id, ativo):
    produtor = Produtor.query.get(produtor_id)
    produtor.ativo = ativo
    db.session.commit()
    return produtor


def atualizar_produtor(produtor_id, dados, imagens=None, remover_fotos_ids=None):
    produtor = Produtor.query.get(produtor_id)
    if not produtor:
        return None

    produtor.nome = dados.get('nome', produtor.nome)
    produtor.cpf = dados.get('cpf', produtor.cpf)
    produtor.telefone = dados.get('telefone', produtor.telefone)
    produtor.email = dados.get('email', produtor.email)
    produtor.nome_propriedade = dados.get('nome_propriedade', produtor.nome_propriedade)
    produtor.especialidade = dados.get('especialidade', produtor.especialidade)
    produtor.endereco = dados.get('endereco', produtor.endereco)
    produtor.certificacoes = dados.get('certificacoes', produtor.certificacoes)
    produtor.descricao = dados.get('descricao', produtor.descricao)

    categorias_ids = dados.get('categorias', None)
    if categorias_ids is not None:
        produtor.categorias = Categoria.query.filter(Categoria.id.in_(categorias_ids)).all() if len(categorias_ids) > 0 else []

    # remover fotos
    if remover_fotos_ids:
        for fid in remover_fotos_ids:
            foto = FotoProdutor.query.get(fid)
            if foto:
                try:
                    path = os.path.join('app', 'static', 'uploads', 'produtores', foto.imagem)
                    if os.path.exists(path):
                        os.remove(path)
                except Exception:
                    pass
                db.session.delete(foto)

    # adicionar novas imagens
    upload_dir = os.path.join('app', 'static', 'uploads', 'produtores')
    os.makedirs(upload_dir, exist_ok=True)
    if imagens:
        for img in imagens:
            if not getattr(img, 'filename', None):
                continue
            filename = secure_filename(img.filename)
            unique_name = f"{produtor.id}_{filename}"
            filepath = os.path.join(upload_dir, unique_name)
            img.save(filepath)
            foto = FotoProdutor(produtor_id=produtor.id, imagem=unique_name)
            db.session.add(foto)

    if 'ativo' in dados:
        val = dados.get('ativo')
        produtor.ativo = True if str(val).lower() in ('1','true','on','yes') else False

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
