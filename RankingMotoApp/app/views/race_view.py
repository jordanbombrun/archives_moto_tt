from flask import make_response, request
from RankingMotoApp.app.services.race_service import RaceService


def add_race():
    datas_list = []
    datas_to_print = ''
    race_url = request.form['race_url']

    # filtre si url ou document
    # appel service
    if (race_url.startswith('http')):
        if(RaceService.add_race_from_web_url(race_url, datas_list)):
            # récup datas OK
            return make_response(datas_list)
            # return classement sous forme de tableau ?
        else:
            for item in datas_list:
                datas_to_print += item + " / "
            # récup KO 
            return make_response(datas_to_print)
    else: # autre source ?
        return make_response('URL non http non implémenté.')
               