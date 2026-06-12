from datetime import datetime
from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from models import db
from models.ciclo import Ciclo, Promocao
from models.combo import Combo, ComboProduto
from models.produto import Produto
from models.venda import Venda
from services.venda_service import cadastrar_venda


venda_bp = Blueprint("venda", __name__, url_prefix="/admin")


@venda_bp.route("/vendas", methods=["GET", "POST"])
@login_required
def vendas():
    if request.method == "POST":
        itens = []
        for produto_id, quantidade in zip(
            request.form.getlist("produto_id"), request.form.getlist("quantidade")
        ):
            if produto_id and quantidade:
                itens.append((produto_id, quantidade))
        try:
            cadastrar_venda(itens)
            db.session.commit()
            flash("Venda cadastrada e estoque atualizado.", "success")
        except ValueError as erro:
            db.session.rollback()
            flash(str(erro), "danger")
        return redirect(url_for("venda.vendas"))

    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    vendas_lista = Venda.query.order_by(Venda.data.desc()).limit(60).all()
    return render_template("vendas.html", produtos=produtos, vendas=vendas_lista)


@venda_bp.route("/combos", methods=["GET", "POST"])
@login_required
def combos():
    if request.method == "POST":
        combo = Combo(
            nome=request.form["nome"],
            descricao=request.form.get("descricao"),
            preco=Decimal(request.form.get("preco", "0").replace(",", ".")),
            ciclo_id=request.form.get("ciclo_id") or None,
        )
        db.session.add(combo)
        for produto_id, quantidade in zip(
            request.form.getlist("produto_id"), request.form.getlist("quantidade")
        ):
            if produto_id and quantidade:
                combo.itens.append(
                    ComboProduto(produto_id=int(produto_id), quantidade=int(quantidade))
                )
        db.session.commit()
        flash("Combo criado com sucesso.", "success")
        return redirect(url_for("venda.combos"))

    return render_template(
        "combos.html",
        combos=Combo.query.order_by(Combo.ativo.desc(), Combo.nome).all(),
        produtos=Produto.query.filter_by(ativo=True).order_by(Produto.nome).all(),
        ciclos=Ciclo.query.order_by(Ciclo.data_inicio.desc()).all(),
    )


@venda_bp.route("/combos/<int:combo_id>/remover", methods=["POST"])
@login_required
def remover_combo(combo_id):
    combo = Combo.query.get_or_404(combo_id)
    combo.ativo = False
    db.session.commit()
    flash("Combo desativado.", "info")
    return redirect(url_for("venda.combos"))


@venda_bp.route("/promocoes", methods=["GET", "POST"])
@login_required
def promocoes():
    if request.method == "POST":
        promocao = Promocao(
            produto_id=int(request.form["produto_id"]),
            preco_promocional=Decimal(
                request.form.get("preco_promocional", "0").replace(",", ".")
            ),
            ciclo_id=int(request.form["ciclo_id"]),
        )
        db.session.add(promocao)
        db.session.commit()
        flash("Promocao criada com sucesso.", "success")
        return redirect(url_for("venda.promocoes"))

    return render_template(
        "promocoes.html",
        promocoes=Promocao.query.order_by(Promocao.id.desc()).all(),
        produtos=Produto.query.filter_by(ativo=True).order_by(Produto.nome).all(),
        ciclos=Ciclo.query.order_by(Ciclo.data_inicio.desc()).all(),
    )


@venda_bp.route("/promocoes/<int:promocao_id>/remover", methods=["POST"])
@login_required
def remover_promocao(promocao_id):
    promocao = Promocao.query.get_or_404(promocao_id)
    promocao.ativa = False
    db.session.commit()
    flash("Promocao desativada.", "info")
    return redirect(url_for("venda.promocoes"))


@venda_bp.route("/ciclos", methods=["GET", "POST"])
@login_required
def ciclos():
    if request.method == "POST":
        ciclo = Ciclo(
            nome=request.form["nome"],
            data_inicio=datetime.strptime(request.form["data_inicio"], "%Y-%m-%d").date(),
            data_fim=datetime.strptime(request.form["data_fim"], "%Y-%m-%d").date(),
        )
        db.session.add(ciclo)
        db.session.commit()
        flash("Ciclo cadastrado.", "success")
        return redirect(url_for("venda.ciclos"))

    return render_template(
        "ciclos.html", ciclos=Ciclo.query.order_by(Ciclo.data_inicio.desc()).all()
    )
