from flask import current_app as app
from RankingMotoApp.app.views.home_view import home
from RankingMotoApp.app.views.race_view import add_race

# paramètres :  URL , fonction de vue , nom de la vue
app.add_url_rule('/', 'home', home) # vue formulaire détails pilote et ajout course via son url
app.add_url_rule('/course_details', 'add_race', add_race, methods=['POST']) # rendu course sauvegardée
# app.add_url_rule('/add_race', 'add_race', add_race, methods=['POST']) # traitement form add_race