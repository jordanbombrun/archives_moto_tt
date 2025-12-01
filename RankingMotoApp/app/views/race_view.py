from flask import make_response, render_template, request
from RankingMotoApp.app.services.race_service import RaceService
from RankingMotoApp.app.services.rider_service import RiderService
from RankingMotoApp.app.utils.DBReport import DBReport
from datetime import date

race_service = RaceService()
rider_service = RiderService()

def render_form_add_race():
    result_get_series = race_service.get_all_series()
    if result_get_series != DBReport.GET_NOT_FOUND and result_get_series != DBReport.GET_ERROR:
        series = result_get_series
    else:
        series = None
    result_get_formats = race_service.get_all_formats()
    if result_get_formats != DBReport.GET_NOT_FOUND and result_get_formats != DBReport.GET_ERROR:
        formats = result_get_formats
    else:
        formats = None
    result_get_categories = race_service.get_all_categories()
    if result_get_categories != DBReport.GET_NOT_FOUND and result_get_categories != DBReport.GET_ERROR:
        categories = result_get_categories
    else:
        categories = None
    return render_template('add_race.html', active_page='add_race',series=series, formats=formats, categories=categories)
    
def render_list_all_race():
    res_get_races = race_service.get_all_races()
    if res_get_races != DBReport.GET_NOT_FOUND and res_get_races != DBReport.GET_ERROR: 
        return render_template('list_race.html', active_page='list_race', races=res_get_races)
    return make_response('Erreur pendant la récupération des courses')

def render_list_races_for_serie(serie_id: int):
    try:
        serie_id_int = int(serie_id)
        if serie_id_int <= 0:
            return make_response('Identifiant de série invalide.', 400)
    except (ValueError, TypeError):
        return make_response('Identifiant de série invalide.', 400)

    res_get_serie = race_service.get_serie_by_id(serie_id_int)
    if res_get_serie == DBReport.GET_NOT_FOUND or res_get_serie == DBReport.GET_ERROR:
        return make_response('Série non trouvée.', 404)
    res_get_races = race_service.get_all_race_for_serie(serie_id_int)
    if res_get_races != DBReport.GET_NOT_FOUND and res_get_races != DBReport.GET_ERROR:
        return render_template('list_race.html', active_page='', races=res_get_races, serie=res_get_serie)
    return make_response('Erreur pendant la récupération des courses pour cette série')

def render_race_details(race_id: int):
    try:
        race_id_int = int(race_id)
    except (ValueError, TypeError):
        return make_response('Identifiant de course invalide.', 400)

    res_get_race = race_service.get_race_by_id(race_id_int)
    if res_get_race == DBReport.GET_NOT_FOUND:
        return make_response('Course non trouvée.', 404)
    if res_get_race == DBReport.GET_ERROR:
        return make_response('Erreur pendant la récupération de la course', 500)
    race_obj = res_get_race 

    # participations = dao_get_participations_by_race(race_obj.db_id)
    participations = rider_service.get_participations_by_race(race_obj.db_id)
    if participations == DBReport.GET_ERROR:
        participations = None
    elif participations == DBReport.GET_NOT_FOUND:
        participations = []

    return render_template('race_details.html', race=race_obj, participations=participations)

def render_rider_details_on_race(race_id: int, rider_id: int):
    try:
        race_id_int = int(race_id)
        if race_id_int <= 0:
            return make_response('Identifiant de course invalide.', 400)
    except (ValueError, TypeError):
        return make_response('Identifiant de course invalide.', 400)

    try:
        rider_id_int = int(rider_id)
        if rider_id_int <= 0:
            return make_response('Identifiant de pilote invalide.', 400)
    except (ValueError, TypeError):
        return make_response('Identifiant de pilote invalide.', 400)

    # récupère la course
    res_get_race = race_service.get_race_by_id(race_id_int)
    if res_get_race == DBReport.GET_NOT_FOUND:
        return make_response('Course non trouvée.', 404)
    if res_get_race == DBReport.GET_ERROR:
        return make_response('Erreur pendant la récupération de la course', 500)
    race_obj = res_get_race

    # récupère les participations de la course
    participations = rider_service.get_participations_by_race(race_obj.db_id)
    if participations == DBReport.GET_ERROR:
        return make_response('Erreur pendant la récupération des participations', 500)
    if participations == DBReport.GET_NOT_FOUND:
        participations = []

    # recherche la participation correspondant au rider_id fourni
    selected_participation = None
    for p in participations:
        if not p or not getattr(p, 'rider', None):
            continue
        rider_obj = p.rider
        # robust check: db_id or id attribute
        rider_db_id = getattr(rider_obj, 'db_id', None) or getattr(rider_obj, 'id', None)
        if rider_db_id == rider_id_int:
            selected_participation = p
            break

    if not selected_participation:
        return make_response('Pilote non trouvé pour cette course.', 404)
    else:
        # todo formater données pariticpant
        return make_response('Pilote non trouvé pour cette course.', 404)
        

    # render a template showing rider details on the race
    return render_template('rider_details_on_race.html', race=race_obj, participation=selected_participation)
# ...existing code...

def race_added():
    name = request.form.get('race_name')
    date = request.form.get('race_date')
    location = request.form.get('race_location') 
    serie_id = request.form.get('race_serie_id')
    format_id = request.form.get('race_format_id')
    categories_ids = request.form.getlist('race_category_id');

    if (race_service.add_race(name, date, location, serie_id, format_id, categories_ids)):
        return make_response('la course a été ajoutée avec succès !')
    else:
        return make_response('la course n\'a pas pu être ajoutée !')           

def race_added2():
    # todo : enlever ces infos en dur
    name = 'race_name'
    race_date = date(2025, 1, 26)
    location = 'race_location'
    serie_id = 1
    format_id = 4
    categories_ids = ['1','2','3','4','5']; 
    url = '../templates/ALESTREM2025.html'
    # /todo

    res_add_race = race_service.add_race2(name, race_date, location, serie_id, format_id, categories_ids, url)
    if res_add_race == DBReport.CREATE_OK:
        return make_response('la course a été ajoutée avec succès !')
    else:
        return make_response('la course n\'a pas pu être ajoutée !')  

def add_serie():
    name = request.form.get('new_serie_name')
    year = request.form.get('new_serie_year')
    if (race_service.add_serie(name, year) == DBReport.CREATE_OK):
        return make_response('la série a été ajoutée avec succès !')
    else:
        return make_response('la série n\'a pas pu être ajoutée !')

def render_list_all_serie():
    res_get_series = race_service.get_all_series()
    if res_get_series != DBReport.GET_NOT_FOUND and res_get_series != DBReport.GET_ERROR: 
        return render_template('list_serie.html', active_page='list_serie', series=res_get_series)
    return make_response('Erreur pendant la récupération des courses')

# def add_race_from_url():
#     datas_list = []
#     datas_to_print = ''
#     race_url = request.form['race_url']

#     # filtre si url ou document
#     # appel service
#     if (race_url.startswith('http')):
#         if(RaceService.add_race_from_web_url(race_url, datas_list)):
#             # récup datas OK
#             return make_response(datas_list)
#             # return classement sous forme de tableau ?
#         else:
#             for item in datas_list:
#                 datas_to_print += item + " / "
#             # récup KO 
#             return make_response(datas_to_print)
#     else: # autre source ?
#         return make_response('URL non http non implémenté.')