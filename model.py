from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id_usuario = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    telefone = db.Column(
        db.String(20)
    )

    cidade = db.Column(
        db.String(80)
    )

    email = db.Column(
        db.String(150),
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

    # Solicitações feitas pelo usuário
    solicitacoes = db.relationship(
        "Solicitacao",
        foreign_keys="Solicitacao.id_usuario",
        back_populates="usuario"
    )

    # Solicitações atendidas pelo voluntário
    solicitacoes_voluntario = db.relationship(
        "Solicitacao",
        foreign_keys="Solicitacao.id_voluntario",
        back_populates="voluntario"
    )


class Categoria(db.Model):

    __tablename__ = "categorias"

    id_categoria = db.Column(
        db.Integer,
        primary_key=True
    )

    nome_categoria = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    descricao = db.Column(
        db.String(255)
    )

    solicitacoes = db.relationship(
        "Solicitacao",
        back_populates="categoria"
    )


class Solicitacao(db.Model):

    __tablename__ = "solicitacoes"

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

    # Usuário que fez a solicitação
    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id_usuario"),
        nullable=False
    )

    # Voluntário que irá atender
    id_voluntario = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id_usuario"),
        nullable=True
    )

    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id_categoria"),
        nullable=False
    )

    usuario = db.relationship(
        "Usuario",
        foreign_keys=[id_usuario],
        back_populates="solicitacoes"
    )

    voluntario = db.relationship(
        "Usuario",
        foreign_keys=[id_voluntario],
        back_populates="solicitacoes_voluntario"
    )

    categoria = db.relationship(
        "Categoria",
        back_populates="solicitacoes"
    )