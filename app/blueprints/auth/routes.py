from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.controllers.auth_controller import (
    registrar_usuario,
    autenticar,
    enviar_email_recuperacao,
    resetar_senha
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# RF01.1 - Cadastro com validação
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar_senha", "")
        tipo = request.form.get("tipo_usuario", "Cliente")
        
        # Validar se as senhas batem
        if senha != confirmar:
            flash("As senhas não conferem.", "danger")
            return redirect(url_for("auth.register"))
        
        ok, msg = registrar_usuario(email, senha, tipo)
        flash(msg, "success" if ok else "danger")
        if ok:
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

# RF01.2 - Login com sessão segura
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        user = autenticar(email, senha)
        
        if user:
            login_user(user, remember=request.form.get("remember_me"))
            next_page = request.args.get("next")
            return redirect(next_page if next_page else url_for("home"))
        
        flash("Email ou senha incorretos.", "danger")
    return render_template("auth/login.html")

# RF01.2 - Logout
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for("auth.login"))

# RF01.3 - Solicitar recuperação de senha
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        ok, msg = enviar_email_recuperacao(email)
        flash(msg, "success" if ok else "info")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/forgot_password.html")

# RF01.3 - Recuperar senha com token
@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        nova_senha = request.form.get("nova_senha", "")
        confirmar = request.form.get("confirmar_senha", "")
        
        if nova_senha != confirmar:
            flash("As senhas não conferem.", "danger")
            return redirect(url_for("auth.reset_password", token=token))
        
        ok, msg = resetar_senha(token, nova_senha)
        flash(msg, "success" if ok else "danger")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/reset_password.html", token=token)

