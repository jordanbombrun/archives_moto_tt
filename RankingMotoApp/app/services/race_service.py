from datetime import date
from RankingMotoApp.app.models.race import *
from RankingMotoApp.app.dao.race_dao import *
from RankingMotoApp.app.utils.DBReport import DBReport

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
            
            new_race = Race(name_p, date_p, format_l ,location_p, serie_l)
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

        #     soup = self.get_datas_from_source(os.path.join(os.path.dirname(__file__), "..", "templates", "page_utf8_short.html"))
        #     if (soup is not None):
        #         rows = soup.find_all("tr")
        #         i = 0
        #         old_rider = None 
        #         current_rider = None
        #         init_nb_lap = False
        #         for row in rows:
        #             td_values = [td.text.strip() for td in row.find_all("td", recursive=False)]
        #             if (i == 3): # ligne des entêtes
        #                 new_race.nb_CP = len(td_values) - 4 
        #             elif (i > 3): # filtre les 1ères lignes 
        #                 if not init_nb_lap:
        #                     new_race.nb_laps = int(td_values[3])
        #                     init_nb_lap = True
        #                 if (td_values[1] != ''):
        #                     current_line_number = td_values[1]
        #                 if (old_rider is None or current_line_number != old_rider.number): # nouveau pilote
        #                     current_rider = Rider(td_values[0], td_values[1], td_values[2], td_values[3])
        #                     current_rider.chronos_lap_CP = [[] for _ in range(int(new_race.nb_laps))]
        #                     current_rider.positions_lap_CP = [[] for _ in range(int(new_race.nb_laps))]
        #                     new_race.riders.append(current_rider)
        #                 else : # même pilote, mais tour différent
        #                     current_rider.current_lap = td_values[3]
        #                 for j, chrono_CP in enumerate(td_values):
        #                     if (j > 3):
        #                         current_rider.add_chrono(chrono_CP)              
        #                 old_rider = current_rider
        #             i += 1
        #         new_race.save()
        #         return True
        #     else:
        #         return False
        # except Exception as e:
        #     return False

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

    # return DBReport : OK , ERROR OR ALREADY EXISTS
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
    # def add_race_from_web_url(self, url_p, datas_list_p):
    #   # traitement beautifoulSoup
    #     try:
    #         response = requests.get(url_p,headers=self.HEADERS_USER_AGENT)
    #     except Exception as e:
    #         datas_list_p.append('Erreur pendant la récupération des données html.')
    #         datas_list_p.append(str(e))
    #         return False
        
    #     # get race name in url
    #     match_race_name = re.search(r'live/([^/]+)/', url_p)
    #     if match_race_name:
    #         new_race = Race(match_race_name.group(1), date.today())
    #     else:
    #         new_race = Race('Inconnue', date.today())
            
    #     if response.status_code == 200:
    #         soup = BeautifulSoup(response.text, "html.parser")
    #         if (soup is not None):
    #             rows = soup.find_all("tr")
    #             i = 0
    #             old_rider = None 
    #             current_rider = None
    #             init_nb_lap = False
    #             for row in rows:
    #                 td_values = [td.text.strip() for td in row.find_all("td", recursive=False)]
    #                 if (i == 3): # ligne des entêtes
    #                     new_race.nb_cp = len(td_values) - 4 
    #                 elif (i > 3): # filtre les 1ères lignes 
    #                     if not init_nb_lap:
    #                         new_race.nb_lap = int(td_values[3])
    #                         init_nb_lap = True
    #                     if (td_values[1] != ''):
    #                         current_line_number = td_values[1]
    #                     if (old_rider is None or current_line_number != old_rider.number): # nouveau pilote
    #                         current_rider = Rider(td_values[0], td_values[1], td_values[2], td_values[3])
    #                         current_rider.chronos_lap_CP = [[] for _ in range(int(new_race.nb_lap))]
    #                         current_rider.positions_lap_CP = [[] for _ in range(int(new_race.nb_lap))]
    #                         new_race.riders.append(current_rider)
    #                     else : # même pilote, mais tour différent
    #                         current_rider.current_lap = td_values[3]
    #                     for j, chrono_CP in enumerate(td_values):
    #                         if (j > 3):
    #                             current_rider.add_chrono(chrono_CP)              
    #                     old_rider = current_rider
    #                 i += 1
    #             new_race.save()
    #             datas_list_p.append(new_race.get_race())
    #             return True
    #         else:
    #             datas_list_p.append('Erreur pendant la récupération des données.')
    #     else:
    #         datas_list_p.append('Ressource non trouvée.')
    #     return False


    # Récupére le contenu sur le web ou dans un fichier local
    # renvoie un objet BeautifulSoup si OK , un string vide si KO
    # def get_datas_from_source(self, url_p):
    #     if (url_p.startswith('http')):
    #         response = requests.get(url_p, headers=self.HEADERS_USER_AGENT)
    #         if response.status_code == 200:
    #             return BeautifulSoup(response.text, "html.parser")
    #     else:
    #         html_content = ''
    #         with open(url_p, "r", encoding="utf-8") as file:
    #             html_content = file.read()
    #             if html_content != '':
    #                 return BeautifulSoup(html_content, "html.parser")
    #     return None
