from flask import current_app as app
from RankingMotoApp.app.views.race_view import add_race, add_serie, home_race

# param :  rule = URL , view_func = fonction to be called in the view
app.add_url_rule(rule= '/', view_func= home_race)
app.add_url_rule('/add_race', add_race, methods=['POST']) # render race added
app.add_url_rule('/add_serie', add_serie, methods=['POST']) # render serie added
