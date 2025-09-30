from flask import current_app as app
from RankingMotoApp.app.views.home_view import render_home
from RankingMotoApp.app.views.race_view import add_race, add_serie, render_form_add_race, render_list_all_race

# param :  rule = URL , view_func = fonction to be called in the view
app.add_url_rule(rule= '/', view_func= render_home)
app.add_url_rule(rule='/lister_courses', view_func=render_list_all_race)
app.add_url_rule(rule= '/ajouter_course', view_func= render_form_add_race)
app.add_url_rule(rule='/add_race', view_func=add_race, methods=['POST']) # render race added
app.add_url_rule('/add_serie', add_serie, methods=['POST']) # render serie added
