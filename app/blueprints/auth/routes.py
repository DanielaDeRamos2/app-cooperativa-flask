from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.controllers.auth_controller import (
    registrar_usuario,
    autenticar,
    enviar_email_recuperacao
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# RF01.1 - Cadastro
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        tipo = request.form["tipo_usuario"]
        ok, msg = registrar_usuario(email, senha, tipo)
        flash(msg)
        if ok:
            return redirect(url_for("auth.login"))
    return render_template("register.html")

# RF01.2 - Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        user = autenticar(email, senha)
        if user:
            login_user(user)
            return redirect(url_for("index"))
        flash("Credenciais inválidas.")
    return render_template("login.html")

# RF01.2 - Logout
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

# RF01.3 - Recuperação de senha
@auth_bp.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == "POST":
        email = request.form["email"]
        enviar_email_recuperacao(email)
        flash("Se o e-mail existir, enviaremos instruções.")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html")
