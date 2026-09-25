import os

from flask import Flask
from flask_login import LoginManager

from config import Config
from models import Usuario, db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.estoque import estoque_bp
from routes.produto import produto_bp
from routes.venda import venda_bp


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Entre para acessar a area administrativa."
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(venda_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()
        criar_usuario_admin_inicial()

    return app


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


def criar_usuario_admin_inicial():
    """Cria um administrador somente se as variáveis de bootstrap forem fornecidas.

    A inicialização nunca redefine a senha de contas existentes.
    """
    login = os.getenv("ADMIN_USERNAME")
    senha = os.getenv("ADMIN_PASSWORD")
    if bool(login) != bool(senha):
        raise RuntimeError("Defina ADMIN_USERNAME e ADMIN_PASSWORD em conjunto.")
    if not login:
        return

    if Usuario.query.filter_by(usuario=login).first() is None:
        usuario = Usuario(
            nome=os.getenv("ADMIN_NAME", login),
            usuario=login,
        )
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
