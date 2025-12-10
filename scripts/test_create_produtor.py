from app import create_app, db
from app.models.usuario import Usuario, TipoUsuario
from app.models.categoria import Categoria
from app.controllers.produtorController import criar_produtor

app = create_app()
with app.app_context():
    # criar tabelas se não existirem
    db.create_all()

    # criar categoria de teste se não existir
    cat = Categoria.query.filter_by(nome='Hortifruti').first()
    if not cat:
        cat = Categoria(nome='Hortifruti', descricao='Hortifruti')
        db.session.add(cat)
        db.session.commit()

    # criar usuário admin de teste
    admin = Usuario.query.filter_by(email='admin@test.local').first()
    if not admin:
        admin = Usuario(email='admin@test.local')
        admin.set_password('password')
        admin.tipo_usuario = TipoUsuario.ADMIN
        db.session.add(admin)
        db.session.commit()
        print('Usuário admin criado:', admin.email)
    else:
        print('Usuário admin já existe:', admin.email)

    dados = {
        'nome': 'Produtor Teste',
        'cpf': '000.000.000-00',
        'telefone': '(11) 99999-0000',
        'email': 'produtor@teste.local',
        'endereco': 'Rua Teste, 123',
        'certificacoes': 'Orgânico',
        'descricao': 'Pequena propriedade de teste',
        'categorias': [str(cat.id)]
    }

    produtor = criar_produtor(admin, dados, imagens=None)
    print('Produtor criado, id=', produtor.id, 'nome=', produtor.nome)
