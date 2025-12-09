from flask import Flask, render_template, request
from app import create_app, db

app = create_app()

# Criar tabelas do banco de dados
with app.app_context():
    db.create_all()

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
        {"nome": "Cenoura Fresca", "preco": 5.99},
        {"nome": "Alface Crocante", "preco": 4.50},
        {"nome": "Tomate Vermelho", "preco": 7.99},
        {"nome": "Queijo Artesanal", "preco": 28.50},
        {"nome": "Carne Bovina Premium", "preco": 42.90},
        {"nome": "Pão Integral", "preco": 8.50},
        {"nome": "Iogurte Natural", "preco": 6.99},
        {"nome": "Mel Puro", "preco": 18.90},
        {"nome": "Ovos Caipiras", "preco": 12.50},
        {"nome": "Leite Fresco", "preco": 5.50},
    ]
    return render_template("produtos.html", titulo="Produtos", produtos=produtos)

@app.route("/smart-tv")
def smart_tv():
    return render_template("smart_tvs.html", titulo="Smart TVs")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html", titulo="Sobre Nós")

@app.route("/faq")
def faq():
    return render_template("faq.html", titulo="FAQ")

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        mensagem = request.form.get("mensagem")
        print(f"Contato: {nome} ({email}) - {mensagem}")
    return render_template("contato.html", titulo="Contato")

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

if __name__ == "__main__":
    app.run(debug=True)
