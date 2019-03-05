from flask import Flask

from config import app_config
from model import db, ma
from controller.TaxController import tax_api as tax_blueprint


def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    app.url_map.strict_slashes = False

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(tax_blueprint, url_prefix='/api/tax')

    return app


# env_name = os.getenv('FLASK_ENV')
app = create_app('development')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
