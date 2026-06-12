from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from models.usuario import Usuario


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = Usuario.query.filter_by(usuario=request.form.get("usuario")).first()
        senha = request.form.get("senha", "")

        if usuario and usuario.check_senha(senha):
            login_user(usuario)
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("dashboard.dashboard"))

        flash("Usuario ou senha invalidos.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Voce saiu do sistema.", "info")
    return redirect(url_for("produto.index"))
