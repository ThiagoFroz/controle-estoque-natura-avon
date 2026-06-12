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
        criar_usuarios_admin()

    return app


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


def criar_usuarios_admin():
    Usuario.query.filter_by(usuario="admin").delete()

    admins = {
        "anafroz": "Ana Froz",
        "sandrafroz": "Sandra Froz",
        "thifroz": "Thi Froz",
    }

    for login, nome in admins.items():
        usuario = Usuario.query.filter_by(usuario=login).first()
        if usuario is None:
            usuario = Usuario(nome=nome, usuario=login)
            db.session.add(usuario)
        usuario.set_senha("181085")

    db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
