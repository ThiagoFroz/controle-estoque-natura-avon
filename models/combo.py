from . import db


class Combo(db.Model):
    __tablename__ = "combos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(140), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    ciclo_id = db.Column(db.Integer, db.ForeignKey("ciclos.id"))
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    ciclo = db.relationship("Ciclo", back_populates="combos")
    itens = db.relationship(
        "ComboProduto", back_populates="combo", cascade="all, delete-orphan", lazy=True
    )


class ComboProduto(db.Model):
    __tablename__ = "combo_produtos"

    id = db.Column(db.Integer, primary_key=True)
    combo_id = db.Column(db.Integer, db.ForeignKey("combos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    combo = db.relationship("Combo", back_populates="itens")
    produto = db.relationship("Produto")
