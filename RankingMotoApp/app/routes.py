from flask import current_app as app
from RankingMotoApp.app.views.home_view import home
from RankingMotoApp.app.views.race_view import add_race, add_serie

# paramètres :  URL , fonction de vue , nom de la vue
app.add_url_rule('/', 'home', home) #
app.add_url_rule('/add_race', 'add_race', add_race, methods=['POST']) # render race added
app.add_url_rule('/add_serie', 'add_serie', add_serie, methods=['POST']) # render serie added
