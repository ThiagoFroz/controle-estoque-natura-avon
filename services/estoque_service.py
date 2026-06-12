from flask_login import current_user

from models import db
from models.produto import MovimentacaoEstoque, Produto


def movimentar_estoque(produto_id, tipo, quantidade, responsavel=None):
    produto = Produto.query.get_or_404(produto_id)
    quantidade = int(quantidade)

    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    if tipo == "entrada":
        produto.quantidade += quantidade
    elif tipo == "saida":
        if produto.quantidade < quantidade:
            raise ValueError("Estoque insuficiente para esta saida.")
        produto.quantidade -= quantidade
    else:
        raise ValueError("Tipo de movimentacao invalido.")

    nome_responsavel = responsavel
    if nome_responsavel is None and current_user.is_authenticated:
        nome_responsavel = current_user.nome

    movimentacao = MovimentacaoEstoque(
        produto=produto,
        tipo=tipo,
        quantidade=quantidade,
        responsavel=nome_responsavel or "Sistema",
    )
    db.session.add(movimentacao)
    return movimentacao
