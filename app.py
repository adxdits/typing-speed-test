# Simple, one file Flask App
from flask import Flask
from src.routes.api import api_bp
from src.routes.template import template_bp
from src.models import create_tables

app = Flask(__name__, template_folder='src/templates')
app.config['SECRET_KEY'] = ''

app.register_blueprint(api_bp)
app.register_blueprint(template_bp)



# Charger les tables au lancement de l'app
with app.app_context():
    create_tables()