from app import create_app, db
from app.models.usuario import Usuario, TipoUsuario
import os

app = create_app()

with app.app_context():
    # ensure DB tables
    db.create_all()

    # ensure admin exists
    admin = Usuario.query.filter_by(email='admin@test.local').first()
    if not admin:
        admin = Usuario(email='admin@test.local')
        admin.set_password('Admin123!')
        admin.tipo_usuario = TipoUsuario.ADMIN
        db.session.add(admin)
        db.session.commit()
        print('Admin criado')
    else:
        admin.set_password('Admin123!')
        admin.tipo_usuario = TipoUsuario.ADMIN
        db.session.commit()
        print('Admin atualizado')

    # ensure produtor user exists
    prod_user = Usuario.query.filter_by(email='produtor_user@test.local').first()
    if not prod_user:
        prod_user = Usuario(email='produtor_user@test.local')
        prod_user.set_password('Prod123!')
        prod_user.tipo_usuario = TipoUsuario.PRODUTOR
        db.session.add(prod_user)
        db.session.commit()
        print('Produtor user criado')
    else:
        prod_user.set_password('Prod123!')
        prod_user.tipo_usuario = TipoUsuario.PRODUTOR
        db.session.commit()
        print('Produtor user atualizado')

    client = app.test_client()

    # Anonymous access
    r = client.get('/produtores/novo')
    print('Anonymous GET /produtores/novo ->', r.status_code)

    # Login as produtor (follow redirects to set session cookie)
    r = client.post('/auth/login', data={'email':'produtor_user@test.local','senha':'Prod123!'}, follow_redirects=True)
    print('Produtor login POST ->', r.status_code)
    r2 = client.get('/produtores/novo')
    print('Produtor GET /produtores/novo ->', r2.status_code)

    # Logout by creating new client (fresh)
    client = app.test_client()

    # Login as admin (follow redirects to set session cookie)
    r = client.post('/auth/login', data={'email':'admin@test.local','senha':'Admin123!'}, follow_redirects=True)
    print('Admin login POST ->', r.status_code)
    r2 = client.get('/produtores/novo')
    print('Admin GET /produtores/novo ->', r2.status_code)
