from datetime import datetime

from . import db


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(160), nullable=False)
    codigo = db.Column(db.String(60), unique=True, nullable=False)
    marca = db.Column(db.String(40), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    categoria = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    destaque = db.Column(db.Boolean, nullable=False, default=False)
    estoque_minimo = db.Column(db.Integer, nullable=False, default=3)

    movimentacoes = db.relationship(
        "MovimentacaoEstoque", back_populates="produto", lazy=True
    )

    @property
    def sem_estoque(self):
        return self.quantidade <= 0

    @property
    def estoque_baixo(self):
        return 0 < self.quantidade <= self.estoque_minimo


class MovimentacaoEstoque(db.Model):
    __tablename__ = "movimentacoes_estoque"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    responsavel = db.Column(db.String(120))

    produto = db.relationship("Produto", back_populates="movimentacoes")
