import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.config.from_object(config.Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : 'Flask Api Course'
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

from src.database import models
from src import routes