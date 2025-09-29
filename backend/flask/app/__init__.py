from flask import Flask, jsonify
from .db import init_cors, init_db
from .routes import api_bp
from .seed import seed_defaults

def create_app() -> Flask:
    app = Flask(__name__)
    init_cors(app)

    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        init_db()
        seed_defaults()

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app
