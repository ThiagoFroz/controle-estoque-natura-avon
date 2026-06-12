import csv
from io import StringIO

from flask import Blueprint, Response, render_template
from flask_login import login_required

from models import db
from models.combo import Combo
from models.produto import Produto
from models.venda import ItemVenda, Venda


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/admin")


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    produtos = Produto.query.filter_by(ativo=True).all()
    total_vendido = db.session.query(db.func.coalesce(db.func.sum(Venda.valor_total), 0)).scalar()
    return render_template(
        "dashboard.html",
        total_produtos=len(produtos),
        sem_estoque=sum(1 for p in produtos if p.sem_estoque),
        estoque_baixo=sum(1 for p in produtos if p.estoque_baixo),
        total_vendido=total_vendido,
        total_combos=Combo.query.filter_by(ativo=True).count(),
    )


@dashboard_bp.route("/relatorios/estoque.csv")
@login_required
def relatorio_estoque_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Codigo", "Nome", "Marca", "Categoria", "Preco", "Quantidade"])
    for p in Produto.query.filter_by(ativo=True).order_by(Produto.nome).all():
        writer.writerow([p.codigo, p.nome, p.marca, p.categoria, p.preco, p.quantidade])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=estoque.csv"},
    )


@dashboard_bp.route("/relatorios/vendas.csv")
@login_required
def relatorio_vendas_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Data", "Produto", "Quantidade", "Valor Unitario", "Valor Total"])
    itens = ItemVenda.query.join(Venda).order_by(Venda.data.desc()).all()
    for item in itens:
        writer.writerow(
            [
                item.venda.data.strftime("%d/%m/%Y %H:%M"),
                item.produto.nome,
                item.quantidade,
                item.valor_unitario,
                item.quantidade * item.valor_unitario,
            ]
        )
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=vendas.csv"},
    )


@dashboard_bp.route("/relatorios/estoque")
@login_required
def relatorio_estoque_print():
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    return render_template("relatorio_estoque.html", produtos=produtos)


@dashboard_bp.route("/relatorios/vendas")
@login_required
def relatorio_vendas_print():
    itens = ItemVenda.query.join(Venda).order_by(Venda.data.desc()).all()
    return render_template("relatorio_vendas.html", itens=itens)
