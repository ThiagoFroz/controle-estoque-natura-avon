from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from .usuario import Usuario  # noqa: E402,F401
from .produto import Produto, MovimentacaoEstoque  # noqa: E402,F401
from .venda import Venda, ItemVenda  # noqa: E402,F401
from .ciclo import Ciclo, Promocao  # noqa: E402,F401
from .combo import Combo, ComboProduto  # noqa: E402,F401
