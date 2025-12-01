from flask import current_app as app
from RankingMotoApp.app.views.home_view import *
from RankingMotoApp.app.views.race_view import *

# param :  rule = URL , view_func = fonction to be called in the view
app.add_url_rule(rule= '/', view_func= render_home)

# races
app.add_url_rule(rule='/lister_courses', view_func=render_list_all_race)
app.add_url_rule(rule='/course_ajoutee', view_func=race_added, methods=['POST']) # render race added
app.add_url_rule(rule='/ajouter_course', view_func= render_form_add_race)
app.add_url_rule(rule='/course_importee', view_func= race_added2, methods=['POST'])
app.add_url_rule(rule='/lister_courses/serie_id=<int:serie_id>', view_func=render_list_races_for_serie)
app.add_url_rule(rule='/details_courses/course_id=<int:race_id>', view_func=render_race_details)
app.add_url_rule(rule='/details_courses/course_id=<int:race_id>&rider_id=<int:rider_id>', view_func=render_rider_details_on_race)

# series 
app.add_url_rule(rule='/lister_championnats', view_func=render_list_all_serie)
app.add_url_rule(rule='/ajouter_championnat', view_func=add_serie, methods=['POST']) # render serie added
