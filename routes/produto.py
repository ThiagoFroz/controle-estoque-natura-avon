import os
from decimal import Decimal
from uuid import uuid4

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from werkzeug.utils import secure_filename

from models import db
from models.ciclo import Ciclo, Promocao
from models.combo import Combo
from models.produto import Produto


produto_bp = Blueprint("produto", __name__)
EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "webp", "gif"}


def salvar_imagem(arquivo):
    if not arquivo or not arquivo.filename:
        return None
    extensao = arquivo.filename.rsplit(".", 1)[-1].lower()
    if extensao not in EXTENSOES_PERMITIDAS:
        flash("Formato de imagem nao permitido.", "warning")
        return None
    nome = secure_filename(f"{uuid4().hex}.{extensao}")
    caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome)
    arquivo.save(caminho)
    return nome


@produto_bp.route("/")
def index():
    ciclo = ciclo_atual()
    promocoes = []
    combos = []
    if ciclo:
        promocoes = (
            Promocao.query.filter_by(ciclo_id=ciclo.id, ativa=True)
            .join(Produto)
            .filter(Produto.ativo.is_(True))
            .all()
        )
        combos = Combo.query.filter_by(ciclo_id=ciclo.id, ativo=True).all()

    destaques = Produto.query.filter_by(ativo=True, destaque=True).limit(8).all()
    return render_template(
        "index.html",
        ciclo=ciclo,
        promocoes=promocoes,
        combos=combos,
        destaques=destaques,
    )


@produto_bp.route("/catalogo")
def catalogo():
    busca = request.args.get("busca", "").strip()
    marca = request.args.get("marca", "").strip()
    categoria = request.args.get("categoria", "").strip()

    query = Produto.query.filter_by(ativo=True)
    if busca:
        query = query.filter(
            db.or_(Produto.nome.ilike(f"%{busca}%"), Produto.codigo.ilike(f"%{busca}%"))
        )
    if marca:
        query = query.filter_by(marca=marca)
    if categoria:
        query = query.filter_by(categoria=categoria)

    produtos = query.order_by(Produto.nome).all()
    marcas = [m[0] for m in db.session.query(Produto.marca).distinct().all()]
    categorias = [c[0] for c in db.session.query(Produto.categoria).distinct().all()]
    return render_template(
        "produtos.html",
        produtos=produtos,
        marcas=marcas,
        categorias=categorias,
        filtros={"busca": busca, "marca": marca, "categoria": categoria},
        publico=True,
    )


@produto_bp.route("/produto/<int:produto_id>")
def detalhe_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return render_template("produto_detalhe.html", produto=produto)


@produto_bp.route("/admin/produtos")
@login_required
def admin_produtos():
    produtos = Produto.query.order_by(Produto.ativo.desc(), Produto.nome).all()
    return render_template("produtos.html", produtos=produtos, publico=False)


@produto_bp.route("/admin/produtos/novo", methods=["GET", "POST"])
@login_required
def criar_produto():
    if request.method == "POST":
        produto = Produto()
        preencher_produto(produto)
        db.session.add(produto)
        db.session.commit()
        flash("Produto criado com sucesso.", "success")
        return redirect(url_for("produto.admin_produtos"))
    return render_template("produto_form.html", produto=None)


@produto_bp.route("/admin/produtos/<int:produto_id>/editar", methods=["GET", "POST"])
@login_required
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    if request.method == "POST":
        preencher_produto(produto)
        db.session.commit()
        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("produto.admin_produtos"))
    return render_template("produto_form.html", produto=produto)


@produto_bp.route("/admin/produtos/<int:produto_id>/remover", methods=["POST"])
@login_required
def remover_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    produto.ativo = False
    db.session.commit()
    flash("Produto desativado.", "info")
    return redirect(url_for("produto.admin_produtos"))


def preencher_produto(produto):
    produto.nome = request.form["nome"]
    produto.codigo = request.form["codigo"]
    produto.marca = request.form["marca"]
    produto.preco = Decimal(request.form.get("preco", "0").replace(",", "."))
    produto.quantidade = int(request.form.get("quantidade") or 0)
    produto.categoria = request.form["categoria"]
    produto.descricao = request.form.get("descricao")
    produto.destaque = bool(request.form.get("destaque"))
    produto.estoque_minimo = int(request.form.get("estoque_minimo") or 3)
    imagem = salvar_imagem(request.files.get("imagem"))
    if imagem:
        produto.imagem = imagem


def ciclo_atual():
    from datetime import date

    hoje = date.today()
    return (
        Ciclo.query.filter(Ciclo.data_inicio <= hoje, Ciclo.data_fim >= hoje)
        .order_by(Ciclo.data_inicio.desc())
        .first()
    )
