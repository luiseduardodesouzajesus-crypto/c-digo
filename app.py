from flask import Flask, render_template, request, redirect, url_for
from model import db, Usuario, Categoria, Solicitacao


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# =========================
# BANCO DE DADOS
# =========================

with app.app_context():

    db.create_all()

    categorias_padrao = [
        ("Alimentação", "Ajuda com alimentação"),
        ("Transporte", "Ajuda com transporte"),
        ("Educação", "Ajuda com estudos"),
        ("Saúde", "Ajuda relacionada à saúde")
    ]

    for nome, descricao in categorias_padrao:

        if not Categoria.query.filter_by(
            nome_categoria=nome
        ).first():

            db.session.add(
                Categoria(
                    nome_categoria=nome,
                    descricao=descricao
                )
            )

    db.session.commit()


# =========================
# INÍCIO
# =========================

@app.route("/")
def index():

    usuarios = Usuario.query.all()

    categorias = Categoria.query.all()

    solicitacoes = Solicitacao.query.all()

    return render_template(
        "index.html",
        usuarios=usuarios,
        categorias=categorias,
        solicitacoes=solicitacoes
    )


# =========================
# USUÁRIOS
# =========================

@app.route("/usuario", methods=["GET", "POST"])
def usuario():

    if request.method == "POST":

        nome = request.form["nome"]
        telefone = request.form.get("telefone")
        cidade = request.form.get("cidade")
        email = request.form["email"]
        senha = request.form["senha"]
        tipo_usuario = request.form["tipo_usuario"]

        if Usuario.query.filter_by(email=email).first():

            return "E-mail já cadastrado."

        novo_usuario = Usuario(
            nome=nome,
            telefone=telefone,
            cidade=cidade,
            email=email,
            senha=senha,
            tipo_usuario=tipo_usuario
        )

        db.session.add(novo_usuario)

        db.session.commit()

        return redirect(url_for("usuario"))

    usuarios = Usuario.query.all()

    return render_template(
        "usuario.html",
        usuarios=usuarios
    )


# =========================
# EDITAR USUÁRIO
# =========================

@app.route(
    "/editar_usuario/<int:id>",
    methods=["GET", "POST"]
)
def editar_usuario(id):

    usuario = db.session.get(
        Usuario,
        id
    )

    if not usuario:

        return "Usuário não encontrado."

    if request.method == "POST":

        usuario.nome = request.form["nome"]

        usuario.telefone = request.form.get(
            "telefone"
        )

        usuario.cidade = request.form.get(
            "cidade"
        )

        usuario.email = request.form["email"]

        usuario.senha = request.form["senha"]

        usuario.tipo_usuario = request.form[
            "tipo_usuario"
        ]

        db.session.commit()

        return redirect(url_for("usuario"))

    return render_template(
        "editar_usuario.html",
        usuario=usuario
    )


# =========================
# EXCLUIR USUÁRIO
# =========================

@app.route("/excluir_usuario/<int:id>")
def excluir_usuario(id):

    usuario = db.session.get(
        Usuario,
        id
    )

    if not usuario:

        return "Usuário não encontrado."

    # Verifica se ele possui solicitações
    solicitacoes = Solicitacao.query.filter(
        (Solicitacao.id_usuario == id) |
        (Solicitacao.id_voluntario == id)
    ).all()

    if solicitacoes:

        return (
            "Não é possível excluir este usuário "
            "porque ele está relacionado a uma ou "
            "mais solicitações."
        )

    db.session.delete(usuario)

    db.session.commit()

    return redirect(url_for("usuario"))


# =========================
# NOVA SOLICITAÇÃO
# =========================

@app.route(
    "/solicitacao",
    methods=["GET", "POST"]
)
def solicitacao():

    # SOMENTE usuários comuns
    usuarios = Usuario.query.filter_by(
        tipo_usuario="usuario"
    ).all()

    # SOMENTE voluntários
    voluntarios = Usuario.query.filter_by(
        tipo_usuario="voluntario"
    ).all()

    categorias = Categoria.query.all()

    if request.method == "POST":

        descricao = request.form["descricao"]

        localizacao = request.form.get(
            "localizacao"
        )

        urgente = (
            "urgente" in request.form
        )

        id_usuario = request.form[
            "id_usuario"
        ]

        id_categoria = request.form[
            "id_categoria"
        ]

        id_voluntario = request.form.get(
            "id_voluntario"
        )

        if id_voluntario == "":
            id_voluntario = None

        nova_solicitacao = Solicitacao(

            descricao=descricao,

            localizacao=localizacao,

            urgente=urgente,

            id_usuario=id_usuario,

            id_categoria=id_categoria,

            id_voluntario=id_voluntario

        )

        db.session.add(
            nova_solicitacao
        )

        db.session.commit()

        return redirect(
            url_for("index")
        )

    return render_template(
        "solicitacao.html",

        usuarios=usuarios,

        voluntarios=voluntarios,

        categorias=categorias
    )


# =========================
# EDITAR SOLICITAÇÃO
# =========================

@app.route(
    "/editar_solicitacao/<int:id>",
    methods=["GET", "POST"]
)
def editar_solicitacao(id):

    solicitacao = db.session.get(
        Solicitacao,
        id
    )

    if not solicitacao:

        return "Solicitação não encontrada."

    # Somente usuários
    usuarios = Usuario.query.filter_by(
        tipo_usuario="usuario"
    ).all()

    # Somente voluntários
    voluntarios = Usuario.query.filter_by(
        tipo_usuario="voluntario"
    ).all()

    categorias = Categoria.query.all()

    if request.method == "POST":

        solicitacao.descricao = request.form[
            "descricao"
        ]

        solicitacao.localizacao = request.form.get(
            "localizacao"
        )

        solicitacao.urgente = (
            "urgente" in request.form
        )

        solicitacao.id_usuario = request.form[
            "id_usuario"
        ]

        solicitacao.id_categoria = request.form[
            "id_categoria"
        ]

        solicitacao.status = request.form[
            "status"
        ]

        id_voluntario = request.form.get(
            "id_voluntario"
        )

        if id_voluntario == "":
            id_voluntario = None

        solicitacao.id_voluntario = id_voluntario

        db.session.commit()

        return redirect(
            url_for("index")
        )

    return render_template(
        "editar_solicitacao.html",

        solicitacao=solicitacao,

        usuarios=usuarios,

        voluntarios=voluntarios,

        categorias=categorias
    )


# =========================
# EXCLUIR SOLICITAÇÃO
# =========================

@app.route(
    "/excluir_solicitacao/<int:id>"
)
def excluir_solicitacao(id):

    solicitacao = db.session.get(
        Solicitacao,
        id
    )

    if not solicitacao:

        return "Solicitação não encontrada."

    db.session.delete(
        solicitacao
    )

    db.session.commit()

    return redirect(
        url_for("index")
    )


# =========================
# EXECUTAR
# =========================

if __name__ == "__main__":

    app.run(debug=True)