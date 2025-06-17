from flask import make_response, request
from RankingMotoApp.app.services.race_service import RaceService

race_service = RaceService()

def add_race():
    if (race_service.add_race()):
        return make_response('la course a été ajoutée avec succès !')
    else:
        return make_response('la course n\'a pas pu être ajoutée !')           

def add_race_from_url():
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