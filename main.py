import time
import os
from dotenv import load_dotenv

from flask import Flask
from flask_dance.contrib.google import make_google_blueprint
from flask_migrate import Migrate

from blueprints.mainpage import mainpage_bp
from blueprints.user_blueprint import user_bp
from blueprints.auth import auth_bp
from blueprints.question_blueprint import question_bp
from blueprints.page_transition import page_transition_bp

from extensions import db, login_manager, csrf

# Dev mode only!!!
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development-key')
    app.config['JSON_AS_ASCII'] = False
    app.config['GOOGLE_OAUTH_CLIENT_ID'] = '777033964912-0l815o4iqbmbj3obqgpdpggqc6djqv9n.apps.googleusercontent.com'
    app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get(
        'GOOGLE_OAUTH_CLIENT_SECRET')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI')

    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)

    google_bp = make_google_blueprint(
        scope=['profile', 'email'], redirect_to='auth.google_login')

    app.register_blueprint(mainpage_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(question_bp, url_prefix='/questions')
    app.register_blueprint(auth_bp)
    app.register_blueprint(page_transition_bp)
    app.register_blueprint(google_bp, url_prefix='/google-login')

    with app.app_context():
        time.sleep(1)
        db.create_all()
    print("Flask app created!")
    return app
