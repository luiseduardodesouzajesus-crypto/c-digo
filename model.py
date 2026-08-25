from datetime import datetime

from database import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    telefone = db.Column(
        db.String(20)
    )

    cidade = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )

    tipo_usuario = db.Column(
        db.String(30),
        nullable=False
    )

    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    solicitacoes = db.relationship(
        "Solicitacao",
        back_populates="usuario"
    )


class Categoria(db.Model):
    __tablename__ = "categoria"

    id_categoria = db.Column(
        db.Integer,
        primary_key=True
    )

    nome_categoria = db.Column(
        db.String(100),
        nullable=False
    )

    descricao = db.Column(
        db.Text
    )

    solicitacoes = db.relationship(
        "Solicitacao",
        back_populates="categoria"
    )


class Solicitacao(db.Model):
    __tablename__ = "solicitacao"

    id_solicitacao = db.Column(
        db.Integer,
        primary_key=True
    )

    descricao = db.Column(
        db.Text,
        nullable=False
    )

    localizacao = db.Column(
        db.String(150)
    )

    urgente = db.Column(
        db.Boolean,
        default=False
    )

    status = db.Column(
        db.String(30),
        default="aberta"
    )

    data_solicitacao = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id_usuario"),
        nullable=False
    )

    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey("categoria.id_categoria"),
        nullable=False
    )

    usuario = db.relationship(
        "Usuario",
        back_populates="solicitacoes"
    )

    categoria = db.relationship(
        "Categoria",
        back_populates="solicitacoes"
    )