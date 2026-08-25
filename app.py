from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from database import db
from model import Usuario, Categoria, Solicitacao


def create_app(database_url="sqlite:///dispositivos.db"):

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "chave-do-projeto"

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

        criar_categorias_iniciais()

    @app.route("/")
    def index():

        usuarios = Usuario.query.all()

        categorias = Categoria.query.all()

        solicitacoes = (
            Solicitacao.query
            .order_by(
                Solicitacao.id_solicitacao.desc()
            )
            .all()
        )

        return render_template(
            "index.html",
            usuarios=usuarios,
            categorias=categorias,
            solicitacoes=solicitacoes
        )

    @app.route("/usuario", methods=["GET", "POST"])
    def usuario():

        if request.method == "POST":

            novo_usuario = Usuario(

                nome=request.form["nome"],

                telefone=request.form["telefone"],

                cidade=request.form["cidade"],

                email=request.form["email"],

                senha=request.form["senha"],

                tipo_usuario=request.form["tipo_usuario"]
            )

            db.session.add(novo_usuario)

            db.session.commit()

            return redirect(
                url_for("index")
            )

        return render_template(
            "usuario.html"
        )

    @app.route(
        "/solicitacao",
        methods=["GET", "POST"]
    )
    def solicitacao():

        usuarios = Usuario.query.all()

        categorias = Categoria.query.all()

        if request.method == "POST":

            nova_solicitacao = Solicitacao(

                descricao=request.form["descricao"],

                localizacao=request.form["localizacao"],

                urgente=(
                    request.form.get("urgente")
                    == "on"
                ),

                status="aberta",

                id_usuario=int(
                    request.form["id_usuario"]
                ),

                id_categoria=int(
                    request.form["id_categoria"]
                )
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
            categorias=categorias
        )

    return app


def criar_categorias_iniciais():

    if Categoria.query.count() > 0:
        return

    categorias = [

        Categoria(
            nome_categoria="Alimentação",
            descricao="Necessidades relacionadas à alimentação."
        ),

        Categoria(
            nome_categoria="Transporte",
            descricao="Necessidades relacionadas ao transporte."
        ),

        Categoria(
            nome_categoria="Educação",
            descricao="Necessidades relacionadas à educação."
        ),

        Categoria(
            nome_categoria="Saúde",
            descricao="Necessidades relacionadas à saúde."
        )

    ]

    db.session.add_all(categorias)

    db.session.commit()


app = create_app()


if __name__ == "__main__":

    app.run(
        debug=True
    )