from decimal import Decimal

from models import db
from models.produto import Produto
from models.venda import ItemVenda, Venda
from services.estoque_service import movimentar_estoque


def cadastrar_venda(itens):
    venda = Venda(valor_total=Decimal("0.00"))
    db.session.add(venda)

    total = Decimal("0.00")
    for produto_id, quantidade in itens:
        produto = Produto.query.get_or_404(produto_id)
        quantidade = int(quantidade)
        if quantidade <= 0:
            continue

        movimentar_estoque(produto.id, "saida", quantidade)
        item = ItemVenda(
            venda=venda,
            produto=produto,
            quantidade=quantidade,
            valor_unitario=produto.preco,
        )
        total += Decimal(str(produto.preco)) * quantidade
        db.session.add(item)

    if total == 0:
        raise ValueError("Informe ao menos um item para a venda.")

    venda.valor_total = total
    return venda
