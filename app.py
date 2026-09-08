from flask import Flask, render_template, request, redirect
from sqlalchemy.exc import IntegrityError

from database import db
from model import Usuario, Categoria, Solicitacao


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "chave-do-projeto"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dispositivos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        criar_categorias()

    @app.route("/")
    def index():

        usuarios = Usuario.query.all()
        categorias = Categoria.query.all()
        solicitacoes = Solicitacao.query.order_by(
            Solicitacao.id_solicitacao.desc()
        ).all()

        return render_template(
            "index.html",
            usuarios=usuarios,
            categorias=categorias,
            solicitacoes=solicitacoes
        )

    @app.route("/usuario", methods=["GET", "POST"])
    def usuario():

        if request.method == "POST":

            novo = Usuario(
                nome=request.form["nome"],
                telefone=request.form["telefone"],
                cidade=request.form["cidade"],
                email=request.form["email"],
                senha=request.form["senha"],
                tipo_usuario=request.form["tipo_usuario"]
            )

            try:
                db.session.add(novo)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return "E-mail já cadastrado."

            return redirect("/")

        return render_template("usuario.html")

    @app.route("/usuario/editar/<int:id>", methods=["GET", "POST"])
    def editar_usuario(id):

        usuario = Usuario.query.get_or_404(id)

        if request.method == "POST":

            usuario.nome = request.form["nome"]
            usuario.telefone = request.form["telefone"]
            usuario.cidade = request.form["cidade"]
            usuario.email = request.form["email"]
            usuario.senha = request.form["senha"]
            usuario.tipo_usuario = request.form["tipo_usuario"]

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return "E-mail já cadastrado."

            return redirect("/")

        return render_template(
            "editar_usuario.html",
            usuario=usuario
        )

    @app.route("/usuario/excluir/<int:id>", methods=["POST"])
    def excluir_usuario(id):

        usuario = Usuario.query.get_or_404(id)

        db.session.delete(usuario)
        db.session.commit()

        return redirect("/")

    @app.route("/solicitacao", methods=["GET", "POST"])
    def solicitacao():

        usuarios = Usuario.query.all()
        categorias = Categoria.query.all()

        if request.method == "POST":

            nova = Solicitacao(
                descricao=request.form["descricao"],
                localizacao=request.form["localizacao"],
                urgente="urgente" in request.form,
                status="aberta",
                id_usuario=int(request.form["id_usuario"]),
                id_categoria=int(request.form["id_categoria"])
            )

            db.session.add(nova)
            db.session.commit()

            return redirect("/")

        return render_template(
            "solicitacao.html",
            usuarios=usuarios,
            categorias=categorias
        )

    @app.route("/solicitacao/editar/<int:id>", methods=["GET", "POST"])
    def editar_solicitacao(id):

        solicitacao = Solicitacao.query.get_or_404(id)

        if request.method == "POST":

            solicitacao.descricao = request.form["descricao"]
            solicitacao.localizacao = request.form["localizacao"]
            solicitacao.urgente = "urgente" in request.form
            solicitacao.status = request.form["status"]
            solicitacao.id_usuario = int(request.form["id_usuario"])
            solicitacao.id_categoria = int(request.form["id_categoria"])

            db.session.commit()

            return redirect("/")

        return render_template(
            "editar_solicitacao.html",
            solicitacao=solicitacao,
            usuarios=Usuario.query.all(),
            categorias=Categoria.query.all()
        )

    @app.route("/solicitacao/excluir/<int:id>", methods=["POST"])
    def excluir_solicitacao(id):

        solicitacao = Solicitacao.query.get_or_404(id)

        db.session.delete(solicitacao)
        db.session.commit()

        return redirect("/")

    return app


def criar_categorias():

    if Categoria.query.count() == 0:

        db.session.add_all([
            Categoria(
                nome_categoria="Alimentação",
                descricao="Necessidades de alimentação."
            ),
            Categoria(
                nome_categoria="Transporte",
                descricao="Necessidades de transporte."
            ),
            Categoria(
                nome_categoria="Educação",
                descricao="Necessidades de educação."
            ),
            Categoria(
                nome_categoria="Saúde",
                descricao="Necessidades de saúde."
            )
        ])

        db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)