from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from models import db
from models.produto import MovimentacaoEstoque, Produto
from services.estoque_service import movimentar_estoque


estoque_bp = Blueprint("estoque", __name__, url_prefix="/admin/estoque")


@estoque_bp.route("/", methods=["GET", "POST"])
@login_required
def estoque():
    if request.method == "POST":
        try:
            movimentar_estoque(
                request.form["produto_id"],
                request.form["tipo"],
                request.form["quantidade"],
            )
            db.session.commit()
            flash("Movimentacao registrada.", "success")
        except ValueError as erro:
            db.session.rollback()
            flash(str(erro), "danger")
        return redirect(url_for("estoque.estoque"))

    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    movimentacoes = MovimentacaoEstoque.query.order_by(
        MovimentacaoEstoque.data.desc()
    ).limit(80).all()
    return render_template(
        "estoque.html", produtos=produtos, movimentacoes=movimentacoes
    )
