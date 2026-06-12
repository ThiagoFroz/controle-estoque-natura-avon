from . import db


class Ciclo(db.Model):
    __tablename__ = "ciclos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)

    promocoes = db.relationship("Promocao", back_populates="ciclo", lazy=True)
    combos = db.relationship("Combo", back_populates="ciclo", lazy=True)


class Promocao(db.Model):
    __tablename__ = "promocoes"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    preco_promocional = db.Column(db.Numeric(10, 2), nullable=False)
    ciclo_id = db.Column(db.Integer, db.ForeignKey("ciclos.id"), nullable=False)
    ativa = db.Column(db.Boolean, nullable=False, default=True)

    produto = db.relationship("Produto")
    ciclo = db.relationship("Ciclo", back_populates="promocoes")
