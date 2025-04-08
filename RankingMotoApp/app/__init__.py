from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importer les vues pour enregistrer les routes
    # from .views import home_view

    # Enregistrement des routes
    with app.app_context():
        from . import routes

    return app