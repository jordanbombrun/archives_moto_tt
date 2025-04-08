from flask import current_app as app
from .views.home_view import home

app.add_url_rule('/', 'home', home)

# @app.route('/')
# def home():
#     return "Bienvenue sur la page d'accueil !"