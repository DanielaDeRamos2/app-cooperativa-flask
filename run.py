from flask import Flask, render_template
from flask import request


app = Flask(__name__)


# Define a rota principal da aplicação Flask
@app.route("/")
def home():
    return render_template("index.html", titulo="App Cooperativa")


# rota para a página de celulares
@app.route("/celulares")
def celulares():
    return render_template("celulares.html", titulo="Celulares")


@app.route("/notebooks")
def notebooks():
    return render_template("notebooks.html", titulo="Notebooks")


# rota para retornar uma lista de produtos
@app.route("/produtos")
def produtos():
    produtos = [
        {"nome": "Smartphone Samsung Galaxy S23", "preco": 40000.99},
        {"nome": "Notebook Dell Inspiron 15", "preco": 4299.90},
        {"nome": "Smart TV LG 50'' 4K", "preco": 2499.00},
        {"nome": "Fone de Ouvido JBL Tune 510BT", "preco": 199.99},
        {"nome": "Tablet Apple iPad 9ª Geração", "preco": 3499.00},
        {"nome": "Console PlayStation 5", "preco": 4499.00},
        {"nome": "Caixa de Som Bluetooth JBL Flip 6", "preco": 599.90},
        {"nome": "Monitor Samsung 24'' LED", "preco": 899.00},
        {"nome": "Smartwatch Xiaomi Mi Band 7", "preco": 299.90},
        {"nome": "Impressora HP DeskJet Ink Advantage", "preco": 499.00},
    ]
    return render_template("produtos.html", titulo="Produtos", produtos=produtos)


@app.route("/smart-tv")
def smart_tv():
    return render_template("smart_tvs.html", titulo="Smart TVs")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html", titulo="Sobre Nós")


################################################################
# Métodos para manipular dados via formulários HTML ou rotas


# rota para receber um inteiro na URL (um id, por exemplo)
@app.route("/numero/<int:num>")
def numero(num):
    return f"<h2>O número recebido foi: {num}</h2>"


# rota para receber uma string na URL (um nome, por exemplo)
@app.route("/texto/<string:txt>")
def texto(txt):
    return f"<h2>O texto recebido foi: {txt}</h2>"


# rota para cadastrar um usuário via formulário HTML
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    # Se o método for POST, processa os dados do formulário
    if request.method == "POST":
        data = request.get_json()
        nome = data.get("nome")
        email = data.get("email")
        senha = data.get("senha")
        print(f"Nome: {nome}, E-mail: {email}, Senha: {senha}")
        # RETORNA UM JSON COM OS DADOS CADASTRADOS
        return {
            "status": "ok",
            "code": 200,
            "dados": {"nome": nome, "email": email, "senha": senha},
        }
    # Se o método for GET, exibe o formulário de cadastro
    return render_template("cadastrar_usuario.html", titulo="Cadastrar Usuário")


# rota para logar um usuário via formulário HTML
@app.route("/login", methods=["GET", "POST"])
def login():
    # Se o método for POST, processa os dados do formulário
    if request.method == "POST":
        data = request.get_json()
        usuario = data.get("usuario")
        senha = data.get("senha")
        print(f"Usuário: {usuario}, Senha: {senha}")

        if usuario:
            return {
                "status": "ok",
                "code": 200,
                "dados": {"usuario": usuario, "senha": senha},
            }
    # Se o método for GET, exibe o formulário de login
    return render_template("login_de_usuario.html", titulo="Login de Usuário")



if __name__ == "__main__":
    app.run(debug=True)
