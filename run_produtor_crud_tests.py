from app import create_app, db
from app.models.usuario import Usuario, TipoUsuario
from app.models.categoria import Categoria
import random

app = create_app()

with app.app_context():
    db.create_all()

    # create a test admin with unique email
    email = f'admin_test_{random.randint(1000,9999)}@test.local'
    admin = Usuario(email=email)
    admin.set_password('Admin123!')
    admin.tipo_usuario = TipoUsuario.ADMIN
    db.session.add(admin)
    db.session.commit()
    print('Criado admin:', email)

    # ensure at least one categoria exists
    cat = Categoria.query.first()
    if not cat:
        cat = Categoria(nome='Hortifruti', descricao='Hortifruti')
        db.session.add(cat)
        db.session.commit()
        print('Categoria criada: Hortifruti')

    client = app.test_client()

    # login as this admin (follow redirects to set session cookie)
    r = client.post('/auth/login', data={'email': email, 'senha': 'Admin123!'}, follow_redirects=True)
    print('Login admin status:', r.status_code)

    # create produtor via POST /produtores/novo
    dados = {
        'nome': 'Produtor Test CRUD',
        'cpf': '111.222.333-44',
        'telefone': '(11) 98888-7777',
        'email': 'produtor_crud@test.local',
        'endereco': 'Rua do Teste, 123',
        'certificacoes': 'Teste Cert',
        'descricao': 'Descrição teste CRUD',
        'categorias': [str(cat.id)]
    }

    r = client.post('/produtores/novo', data=dados, follow_redirects=True)
    print('POST /produtores/novo ->', r.status_code)

    # find created produtor
    from app.models.produtor import Produtor
    produtor = Produtor.query.filter_by(nome='Produtor Test CRUD').first()
    print('Produtor criado?', bool(produtor), 'id=', getattr(produtor, 'id', None))

    # GET edit page
    if produtor:
        r = client.get(f'/produtores/editar/{produtor.id}')
        print('GET editar ->', r.status_code)

        # POST update
        dados_update = dados.copy()
        dados_update['nome'] = 'Produtor Test CRUD EDIT'
        r = client.post(f'/produtores/editar/{produtor.id}', data=dados_update, follow_redirects=True)
        print('POST editar ->', r.status_code)

        produtor = Produtor.query.get(produtor.id)
        print('Nome atualizado ->', produtor.nome)

        # attempt delete
        r = client.post(f'/produtores/excluir/{produtor.id}', follow_redirects=True)
        print('POST excluir ->', r.status_code)

        produtor_after = Produtor.query.get(produtor.id)
        print('Produtor existe após exclusão?:', bool(produtor_after))
    else:
        print('Produtor não foi criado, abortando.')
