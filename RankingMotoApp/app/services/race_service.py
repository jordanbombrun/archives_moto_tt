from datetime import date
import os
from bs4 import BeautifulSoup
import requests
from RankingMotoApp.app.models.race import *
from RankingMotoApp.app.dao.race_dao import *
from RankingMotoApp.app.models.rider import Rider
from RankingMotoApp.app.services.racedatas_service import RaceDatasService
from RankingMotoApp.app.utils.DBReport import DBReport

racedatas_service = RaceDatasService()

class RaceService:

    HEADERS_USER_AGENT = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        } 

    # Ajoute une course à partir d'un fichier html (source motott)
    # Retourne True si traitement OK, False sinon
    def add_race(self, name_p: str, date_p: date, location_p: str, serie_id_p: int, format_id_p: int, categories_ids: list[str]) -> bool:
        try:
            result_serie = dao_get_serie_by_id(serie_id_p)
            if result_serie == DBReport.GET_NOT_FOUND:
                serie_l = None
            else:
                serie_l = result_serie

            result_format = dao_get_format_by_id(format_id_p)
            if result_format == DBReport.GET_NOT_FOUND:
                format_l = None
            else:
                format_l = result_format

            result_categories_l = dao_get_categories_by_ids(categories_ids)
            if result_categories_l == DBReport.GET_NOT_FOUND:
                categories_l = None
            else:
                categories_l = result_categories_l
            
            new_race = Race(
                name=name_p,
                date=date_p,
                format=format_l,
                location=location_p,
                serie=serie_l
            )
            if dao_create_race(new_race):
                new_list_race_category_l = []
                for category in categories_l:
                    new_race_category_l = Race_category(new_race.db_id, category.db_id)
                    dao_create_race_category(new_race_category_l)
                    new_list_race_category_l.append(new_race_category_l)
                return True
            return False
        except Exception as e:
            return False

    def add_race2(self, name_p: str, date_p: date, location_p: str, serie_id_p: int, format_id_p: int, categories_ids: list[str], url_p: str) -> bool:
        try:
            result_serie = dao_get_serie_by_id(serie_id_p)
            if result_serie == DBReport.GET_NOT_FOUND:
                serie_l = None
            else:
                serie_l = result_serie

            result_format = dao_get_format_by_id(format_id_p)
            if result_format == DBReport.GET_NOT_FOUND:
                format_l = None
            else:
                format_l = result_format

            new_race = Race(
                name=name_p,
                date=date_p,
                format=format_l,
                location=location_p,
                serie=serie_l
            )

            # todo : ajouter liste de race_category dans l'instance Race
            # result_racecategories_l = dao_get_race_categories_by_id(categories_ids)
            # if result_racecategories_l == DBReport.GET_NOT_FOUND:
            #     racecategories_l = None
            # else:
            #     racecategories_l = result_racecategories_l
            
            if dao_create_race(new_race):
                new_list_race_category_l = []
                # for category in categories_l:
                #     new_race_category_l = Race_category(new_race.db_id, category.db_id)
                #     dao_create_race_category(new_race_category_l)
                #     new_list_race_category_l.append(new_race_category_l)
                
            else:
                return DBReport.CREATE_ERROR

            soup_race_datas = racedatas_service.collect_datas_from_source(url_p)
            if (soup_race_datas is not None):
                if (racedatas_service.parse_datas(new_race, soup_race_datas)):
                    return True
            else:
                return False


            # get and parse datas from html file
            datas_list = []
            soup = BeautifulSoup()
            if (self.collect_datas_from_source(url_p, soup)):
                if (self.parse_race_datas_from_web_url(new_race, datas_list, soup)):
                    return True
            return False
                
        except Exception as e:
            return False

    def get_all_races(self):
        result = dao_get_all_races()
        return result

    def get_all_race_for_serie(self, serie_id_p: int):
        result = dao_get_all_races_for_serie(serie_id_p)
        return result

    def get_all_formats(self):
        result = dao_get_all_formats()
        return result

    def get_all_series(self):
        result = dao_get_all_series()
        return result  

    def get_serie_by_id(self, serie_id_p: int):
        result = dao_get_serie_by_id(serie_id_p)
        return result

    
    def get_all_categories(self):
        result = dao_get_all_categories()
        return result

    def add_serie(self, name_p = None, year_p = None):
        new_serie = Serie(name_p, year_p)
        get_result = dao_get_serie_id_by_name_and_year(name_p, year_p)
        if get_result is None:
            create_result = dao_create_serie(new_serie)
            if create_result in [None, DBReport.CREATE_ERROR]:
                return DBReport.CREATE_ERROR
            elif create_result in [DBReport.CREATE_ALREADY_EXISTS]:
                return DBReport.CREATE_ALREADY_EXISTS
            else:
                return DBReport.CREATE_OK
        else:
            return DBReport.CREATE_ALREADY_EXISTS


    # Récupération du classement et détails de la course via le web en html
    # Retourne True si traitement OK, False sinon
    def parse_race_datas_from_web_url(self, race_p :Race, datas_list_p: list[str], soup_p :BeautifulSoup) -> bool:
        try:
            # get race name in url
            # match_race_name = re.search(r'live/([^/]+)/', url_p)
            # if match_race_name:
            #     new_race = Race(match_race_name.group(1), date.today())
            # else:
            #     new_race = Race('Inconnue', date.today())

            rows = soup_p.find_all("tr")
            i = 0
            old_rider = None 
            current_rider = None
            init_nb_lap = False
            for row in rows:
                td_values = [td.text.strip() for td in row.find_all("td", recursive=False)]
                if (i == 3): # ligne des entêtes
                    race_p.nb_cp = len(td_values) - 4 
                elif (i > 3): # filtre les 1ères lignes 
                    if not init_nb_lap:
                        race_p.nb_lap = int(td_values[3])
                        init_nb_lap = True
                    if (td_values[1] != ''):
                        current_line_number = td_values[1]
                    if (old_rider is None or current_line_number != old_rider.number): # nouveau pilote
                        current_rider = Rider(td_values[0], td_values[1], td_values[2], td_values[3])
                        current_rider.chronos_lap_CP = [[] for _ in range(int(race_p.nb_lap))]
                        current_rider.positions_lap_CP = [[] for _ in range(int(race_p.nb_lap))]
                        race_p.riders.append(current_rider)
                    else : # même pilote, mais tour différent
                        current_rider.current_lap = td_values[3]
                    for j, chrono_CP in enumerate(td_values):
                        if (j > 3):
                            current_rider.add_chrono(chrono_CP)              
                    old_rider = current_rider
                i += 1
            race_p.save()
            datas_list_p.append(race_p.get_race())
            return True
        except Exception as e:
            datas_list_p.append('Erreur pendant le traitement des données html.')
            datas_list_p.append(str(e))
            return False

    # Récupére le contenu sur le web ou dans un fichier local
    # renvoie True si ok, False sinon
    # def collect_datas_from_source(self, url_p :str, raw_datas_p :BeautifulSoup) -> bool:
    #     try:
    #         if (url_p.startswith('http')):
    #             response = requests.get(url_p, headers=self.HEADERS_USER_AGENT)
    #             if response.status_code == 200:
    #                 raw_datas_p = BeautifulSoup(response.text, "html.parser")
    #                 return True
    #         else:
    #             html_content = ''
    #             current_dir = os.path.dirname(os.path.abspath(__file__))
    #             file_path = os.path.join(current_dir, url_p)
    #             with open(file_path, "r", encoding="utf-8") as file:
    #                 html_content = file.read()
    #                 if html_content != '':
    #                     raw_datas_p = BeautifulSoup(html_content, "html.parser")
    #                     return True
    #         return False
    #     except Exception as e:
    #         # todo : ajout logs BDD d'import
    #         return False

