# !importante: instale as dependências necessárias:
# pip install sqlalchemy pymysql

from __future__ import annotations
import os
from contextlib import contextmanager
from typing import Generator, Iterable, Optional, List
from sqlalchemy.orm import declarative_base, relationship, Session, sessionmaker

# arquivo: app/databases/sqlalchemy_db_manager.py
# -------------------------------------------------------------
# Este arquivo mostra um exemplo completo de configuração do SQLAlchemy
# para conectar-se a um banco MySQL chamado "empresa", definir os modelos
# (Clientes, Produtos, Vendas) e implementar rotinas CRUD de forma simples
# e bem comentada para fins didáticos.
#
# Pré-requisitos (instale no seu ambiente virtual):
#   pip install sqlalchemy pymysql
#
# Observação:
# - Evite colocar credenciais no código. Aqui usamos variáveis de ambiente,
#   mas deixamos valores padrão para facilitar os testes locais.
# - Estes exemplos usam SQLAlchemy no estilo "ORM" com Session.
# -------------------------------------------------------------


from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    func,
    select,
    update as sa_update,
    delete as sa_delete,
)

# -------------------------------------------------------------
# 1) Configuração da conexão com o MySQL
# -------------------------------------------------------------
# Definimos as credenciais pelo ambiente com valores padrão para desenvolvimento.
DB_USER = os.getenv("DB_USER", "root")  # Usuário do MySQL
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")  # Senha do MySQL
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")  # Host do MySQL (localhost)
DB_PORT = os.getenv("DB_PORT", "3306")  # Porta padrão do MySQL
DB_NAME = os.getenv("DB_NAME", "empresa")  # Nome do banco de dados

# Montamos a URL de conexão usando o driver PyMySQL.
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criamos o "engine" (objeto que gerencia a conexão com o banco).
# - echo=False para não poluir o console, mude para True para "logar" os SQLs.
# - pool_pre_ping=True ajuda a validar conexões antes de reutilizá-las.
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

# Criamos um "Session factory" que será usado para abrir sessões (transações).
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,  # Evita "flush" automático, dando mais controle
    autocommit=False,  # Nunca autocomitar, sempre commit/rollback explícito
    expire_on_commit=False,  # Evita expirar objetos após commit (facilita o reuso)
    future=True,
)

# Base de modelos ORM (as tabelas herdarão desta classe)
Base = declarative_base()


# -------------------------------------------------------------
# 2) Definição dos modelos (tabelas): Clientes, Produtos, Vendas
# -------------------------------------------------------------


class Cliente(Base):
    """
    Representa a tabela 'clientes'.
    Cada cliente pode ter várias vendas (relação 1:N com Vendas).
    """

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False, unique=False)  # Nome do cliente
    email = Column(
        String(120), nullable=True, unique=True
    )  # Email único (pode ser NULL)
    telefone = Column(String(20), nullable=True)  # Telefone (opcional)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relação com Vendas (back_populates deve bater com o nome no outro lado)
    vendas = relationship(
        "Venda", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Cliente id={self.id} nome={self.nome!r}>"


class Produto(Base):
    """
    Representa a tabela 'produtos'.
    Um produto pode aparecer em várias vendas (relação 1:N com Vendas).
    """

    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)  # Nome do produto
    preco = Column(Float(asdecimal=False), nullable=False)  # Preço do produto
    estoque = Column(Integer, nullable=False, default=0)  # Quantidade em estoque
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    vendas = relationship(
        "Venda", back_populates="produto", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Produto id={self.id} nome={self.nome!r} preco={self.preco} estoque={self.estoque}>"


class Venda(Base):
    """
    Representa a tabela 'vendas'.
    Para fins didáticos, cada venda referencia exatamente um cliente e um produto,
    incluindo a quantidade vendida, o valor unitário na hora da venda e o valor total.
    Em cenários reais, é comum haver uma tabela de itens de venda para N produtos.
    """

    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(
        Integer, ForeignKey("clientes.id", ondelete="RESTRICT"), nullable=False
    )
    produto_id = Column(
        Integer, ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False
    )
    quantidade = Column(Integer, nullable=False, default=1)  # Qtd vendida
    valor_unitario = Column(
        Float(asdecimal=False), nullable=False
    )  # Preço unitário no momento da venda
    valor_total = Column(
        Float(asdecimal=False), nullable=False
    )  # quantidade * valor_unitario
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relações (lado "muitos" referenciando o "um")
    cliente = relationship("Cliente", back_populates="vendas")
    produto = relationship("Produto", back_populates="vendas")

    def __repr__(self) -> str:
        return f"<Venda id={self.id} cliente_id={self.cliente_id} produto_id={self.produto_id} qtd={self.quantidade} total={self.valor_total}>"


# -------------------------------------------------------------
# 3) Funções utilitárias: obter sessão e inicializar o banco
# -------------------------------------------------------------


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Cria e gerencia o ciclo de vida de uma sessão (transação).
    - Abre a sessão ao entrar no bloco "with".
    - Faz commit se nada der errado.
    - Faz rollback se ocorrer uma exceção.
    - Fecha a sessão ao final.
    Uso:
        with get_session() as db:
            # usar 'db' normalmente
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db(create_all: bool = True) -> None:
    """
    Inicializa o banco de dados.
    - Se create_all=True cria as tabelas caso não existam.
    Observação: Para criar o banco 'empresa', faça isso fora do SQLAlchemy
    (por linha de comando ou cliente MySQL), ou use permissões apropriadas.
    """
    if create_all:
        Base.metadata.create_all(bind=engine)


# -------------------------------------------------------------
# 4) CRUD - Clientes
# -------------------------------------------------------------


def create_cliente(
    db: Session, nome: str, email: Optional[str] = None, telefone: Optional[str] = None
) -> Cliente:
    """
    Cria um novo cliente.
    Passos:
    - Instancia o modelo Cliente
    - Adiciona à sessão
    - Faz flush para obter o ID (opcional)
    - Retorna o objeto persistido
    """
    novo = Cliente(nome=nome, email=email, telefone=telefone)
    db.add(novo)
    db.flush()  # garante que novo.id esteja preenchido ainda nesta transação
    return novo


def get_cliente_by_id(db: Session, cliente_id: int) -> Optional[Cliente]:
    """
    Busca um cliente pelo ID, retornando None se não existir.
    """
    return db.get(Cliente, cliente_id)


def list_clientes(db: Session, limit: int = 50, offset: int = 0) -> List[Cliente]:
    """
    Lista clientes com paginação simples (limit/offset).
    """
    stmt = select(Cliente).offset(offset).limit(limit)
    return list(db.scalars(stmt))


def update_cliente(
    db: Session,
    cliente_id: int,
    *,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    telefone: Optional[str] = None,
) -> Optional[Cliente]:
    """
    Atualiza os campos informados de um cliente.
    - Retorna o cliente atualizado, ou None se não encontrado.
    """
    cliente = db.get(Cliente, cliente_id)
    if not cliente:
        return None

    if nome is not None:
        cliente.nome = nome
    if email is not None:
        cliente.email = email
    if telefone is not None:
        cliente.telefone = telefone

    # Como expire_on_commit=False, o objeto permanece utilizável após commit
    db.flush()
    return cliente


def delete_cliente(db: Session, cliente_id: int) -> bool:
    """
    Exclui um cliente pelo ID.
    - Retorna True se excluiu, False se não encontrou.
    - Observação: Não permite excluir se houver vendas (por causa do ondelete=RESTRICT).
    """
    cliente = db.get(Cliente, cliente_id)
    if not cliente:
        return False
    db.delete(cliente)
    # O commit será feito pelo gerenciador de contexto (get_session)
    return True


# -------------------------------------------------------------
# 5) CRUD - Produtos
# -------------------------------------------------------------


def create_produto(db: Session, nome: str, preco: float, estoque: int = 0) -> Produto:
    """
    Cria um novo produto com nome, preço e estoque inicial.
    """
    novo = Produto(nome=nome, preco=float(preco), estoque=int(estoque))
    db.add(novo)
    db.flush()
    return novo


def get_produto_by_id(db: Session, produto_id: int) -> Optional[Produto]:
    """
    Busca um produto pelo ID, retornando None se não existir.
    """
    return db.get(Produto, produto_id)


def list_produtos(db: Session, limit: int = 50, offset: int = 0) -> List[Produto]:
    """
    Lista produtos com paginação simples (limit/offset).
    """
    stmt = select(Produto).offset(offset).limit(limit)
    return list(db.scalars(stmt))


def update_produto(
    db: Session,
    produto_id: int,
    *,
    nome: Optional[str] = None,
    preco: Optional[float] = None,
    estoque: Optional[int] = None,
) -> Optional[Produto]:
    """
    Atualiza os campos informados de um produto.
    - Retorna o produto atualizado, ou None se não encontrado.
    """
    produto = db.get(Produto, produto_id)
    if not produto:
        return None

    if nome is not None:
        produto.nome = nome
    if preco is not None:
        produto.preco = float(preco)
    if estoque is not None:
        produto.estoque = int(estoque)

    db.flush()
    return produto


def delete_produto(db: Session, produto_id: int) -> bool:
    """
    Exclui um produto pelo ID.
    - Retorna True se excluiu, False se não encontrou.
    - Observação: Não permite excluir se houver vendas (por causa do ondelete=RESTRICT).
    """
    produto = db.get(Produto, produto_id)
    if not produto:
        return False
    db.delete(produto)
    return True


# -------------------------------------------------------------
# 6) CRUD - Vendas
# -------------------------------------------------------------
# Observações importantes sobre Vendas:
# - No create_venda verificamos se há estoque suficiente do produto.
# - Ao criar a venda, baixamos o estoque do produto.
# - No update_venda, se a quantidade for alterada, ajustamos o estoque de acordo
#   com a diferença (pode aumentar ou devolver ao estoque).
# - No delete_venda, devolvemos ao estoque a quantidade que havia sido vendida.


def create_venda(
    db: Session,
    cliente_id: int,
    produto_id: int,
    quantidade: int,
    valor_unitario: Optional[float] = None,
) -> Optional[Venda]:
    """
    Cria uma nova venda para um cliente e um produto.
    Regras:
    - Checa se cliente e produto existem.
    - Checa se o estoque é suficiente.
    - Usa o preço atual do produto como valor_unitario se não for informado.
    - Calcula valor_total = quantidade * valor_unitario.
    - Baixa o estoque do produto.
    - Retorna a Venda criada ou None se algo impedir a criação.
    """
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    cliente = db.get(Cliente, cliente_id)
    if not cliente:
        return None

    produto = db.get(Produto, produto_id)
    if not produto:
        return None

    # Usa o preço do produto se valor_unitario não foi passado
    vu = float(valor_unitario if valor_unitario is not None else produto.preco)

    # Verifica estoque disponível
    if produto.estoque < quantidade:
        raise ValueError(
            f"Estoque insuficiente para o produto {produto.nome}. Disponível: {produto.estoque}, solicitado: {quantidade}"
        )

    # Calcula o total
    total = float(quantidade * vu)

    # Atualiza o estoque
    produto.estoque -= quantidade

    # Cria o registro da venda
    venda = Venda(
        cliente_id=cliente.id,
        produto_id=produto.id,
        quantidade=quantidade,
        valor_unitario=vu,
        valor_total=total,
    )
    db.add(venda)
    db.flush()
    return venda


def get_venda_by_id(db: Session, venda_id: int) -> Optional[Venda]:
    """
    Busca uma venda pelo ID, retornando None se não existir.
    """
    return db.get(Venda, venda_id)


def list_vendas(db: Session, limit: int = 50, offset: int = 0) -> List[Venda]:
    """
    Lista vendas com paginação simples (limit/offset).
    """
    stmt = select(Venda).offset(offset).limit(limit)
    return list(db.scalars(stmt))


def update_venda(
    db: Session,
    venda_id: int,
    *,
    cliente_id: Optional[int] = None,
    produto_id: Optional[int] = None,
    quantidade: Optional[int] = None,
    valor_unitario: Optional[float] = None,
) -> Optional[Venda]:
    """
    Atualiza os campos informados de uma venda.
    Regras de estoque:
    - Se a quantidade mudar, ajusta o estoque do produto associado.
    - Se também mudar o produto, devolve estoque ao produto antigo e baixa do novo.
    - Recalcula o valor_total ao final.
    Retorna a venda atualizada, ou None se não encontrada.
    """
    venda = db.get(Venda, venda_id)
    if not venda:
        return None

    # Guardamos o estado anterior para calcular diferenças
    produto_antigo = db.get(Produto, venda.produto_id)
    if not produto_antigo:
        raise RuntimeError("Produto da venda não encontrado (dados inconsistentes).")

    cliente_novo_id = venda.cliente_id if cliente_id is None else cliente_id
    produto_novo_id = venda.produto_id if produto_id is None else produto_id
    quantidade_nova = venda.quantidade if quantidade is None else int(quantidade)
    valor_unitario_novo = (
        venda.valor_unitario if valor_unitario is None else float(valor_unitario)
    )

    if quantidade_nova <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    # Caso o produto mude, precisamos devolver o estoque ao produto antigo
    # e debitar do novo produto.
    if produto_novo_id != venda.produto_id:
        produto_novo = db.get(Produto, produto_novo_id)
        if not produto_novo:
            raise ValueError("Novo produto informado não existe.")

        # Devolve quantidade antiga ao produto antigo
        produto_antigo.estoque += venda.quantidade

        # Debita quantidade nova do produto novo (checa estoque)
        if produto_novo.estoque < quantidade_nova:
            raise ValueError(
                f"Estoque insuficiente no novo produto {produto_novo.nome}. Disponível: {produto_novo.estoque}, solicitado: {quantidade_nova}"
            )
        produto_novo.estoque -= quantidade_nova

        # Atualiza referencias
        venda.produto_id = produto_novo.id
        # Se valor_unitario não foi informado, usa o preço atual do novo produto
        if valor_unitario is None:
            valor_unitario_novo = float(produto_novo.preco)
    else:
        # Produto não mudou. Ajuste apenas a diferença de quantidade, se houver.
        diff = quantidade_nova - venda.quantidade
        if diff != 0:
            # Se diff > 0, precisa debitar mais do estoque
            if diff > 0:
                if produto_antigo.estoque < diff:
                    raise ValueError(
                        f"Estoque insuficiente para aumentar a venda. Disponível: {produto_antigo.estoque}, necessário: {diff}"
                    )
                produto_antigo.estoque -= diff
            else:
                # diff < 0, devolve ao estoque (cancelou parte da venda)
                produto_antigo.estoque += abs(diff)

    # Atualiza cliente, quantidade e valor_unitario
    venda.cliente_id = cliente_novo_id
    venda.quantidade = quantidade_nova

    # Se valor_unitario não foi passado e o produto não foi trocado, mantém o atual.
    # Se quiser sempre usar o valor do produto, passe explicitamente.
    venda.valor_unitario = float(valor_unitario_novo)

    # Recalcula o total
    venda.valor_total = float(venda.quantidade * venda.valor_unitario)

    db.flush()
    return venda


def delete_venda(db: Session, venda_id: int) -> bool:
    """
    Exclui uma venda pelo ID.
    - Antes de excluir, devolve a quantidade ao estoque do produto relacionado.
    - Retorna True se excluiu, False se não encontrou.
    """
    venda = db.get(Venda, venda_id)
    if not venda:
        return False

    produto = db.get(Produto, venda.produto_id)
    if produto:
        # Devolve ao estoque a quantidade que havia sido vendida
        produto.estoque += venda.quantidade

    db.delete(venda)
    return True


# -------------------------------------------------------------
# 7) Exemplos de uso (opcional)
# -------------------------------------------------------------
# Execute este arquivo diretamente para:
# - Garantir a criação das tabelas
# - (Opcional) Criar alguns registros de exemplo
#
# Observação: Em um projeto real, estas funções seriam chamadas a partir de
# controladores, serviços ou camadas de API (FastAPI, Flask, etc).

if __name__ == "__main__":
    # Cria as tabelas (se não existirem)
    init_db(create_all=True)

    # Exemplo rápido (descomente para testar):
    # with get_session() as db:
    #     # Criar cliente
    #     c = create_cliente(db, nome="Maria Silva", email="maria@example.com", telefone="(44) 9999-0000")
    #     # Criar produto
    #     p = create_produto(db, nome="Teclado Mecânico", preco=250.0, estoque=10)
    #     # Criar venda (baixa estoque)
    #     v = create_venda(db, cliente_id=c.id, produto_id=p.id, quantidade=2)
    #     print("Criados:", c, p, v)
    #
    # with get_session() as db:
    #     # Listar vendas
    #     vendas = list_vendas(db, limit=10)
    #     for venda in vendas:
    #         print("Venda:", venda)
    #     # Atualizar venda (aumentar quantidade)
    #     if vendas:
    #         v0 = vendas[0]
    #         v0 = update_venda(db, v0.id, quantidade=v0.quantidade + 1)
    #         print("Venda atualizada:", v0)
    #
    # with get_session() as db:
    #     # Excluir venda e devolver estoque
    #     vendas = list_vendas(db, limit=10)
    #     if vendas:
    #         ok = delete_venda(db, vendas[0].id)
    #         print("Venda excluída:", ok)
