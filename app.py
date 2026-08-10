from flask import Flask,render_template
from flask_jwt_extended import JWTManager

from config import Config
from database.db import db
from models.user import User
from models.document import Document
from routes.auth import auth_bp
from routes.documents import documents_bp


def create_app():

    app = Flask(__name__)

    # Configuration
    app.config.from_object(Config)

    # Database
    db.init_app(app)

    # JWT
    JWTManager(app)

    # Register routes
    app.register_blueprint(auth_bp)

    app.register_blueprint(documents_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )