from datetime import date
import re
from bs4 import BeautifulSoup
import requests
from RankingMotoApp.app.models.race import Race
from RankingMotoApp.app.models.rider import Rider

class RaceService:

    # Récupération du classement et détails de la course via le web en html
    # Retourne True si traitement OK, False sinon
    @staticmethod
    def add_race_from_web_url(url_p, datas_list_p):
        HEADERS_USER_AGENT = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }        # traitement beautifoulSoup
        try:
            response = requests.get(url_p,headers=HEADERS_USER_AGENT)
        except Exception as e:
            datas_list_p.append('Erreur pendant la récupération des données html.')
            datas_list_p.append(str(e))
            return False
        
        # get race name in url
        match_race_name = re.search(r'live/([^/]+)/', url_p)
        if match_race_name:
            new_race = Race(match_race_name.group(1), date.today())
        else:
            new_race = Race('Inconnue', date.today())
            
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            if (soup is not None):
                rows = soup.find_all("tr")
                i = 0
                old_rider = None 
                current_rider = None
                init_nb_lap = False
                for row in rows:
                    td_values = [td.text.strip() for td in row.find_all("td", recursive=False)]
                    if (i == 3): # ligne des entêtes
                        new_race.nb_CP = len(td_values) - 4 
                    elif (i > 3): # filtre les 1ères lignes 
                        if not init_nb_lap:
                            new_race.nb_laps = int(td_values[3])
                            init_nb_lap = True
                        if (td_values[1] != ''):
                            current_line_number = td_values[1]
                        if (old_rider is None or current_line_number != old_rider.number): # nouveau pilote
                            current_rider = Rider(td_values[0], td_values[1], td_values[2], td_values[3])
                            current_rider.chronos_lap_CP = [[] for _ in range(int(new_race.nb_laps))]
                            current_rider.positions_lap_CP = [[] for _ in range(int(new_race.nb_laps))]
                            new_race.riders.append(current_rider)
                        else : # même pilote, mais tour différent
                            current_rider.current_lap = td_values[3]
                        for j, chrono_CP in enumerate(td_values):
                            if (j > 3):
                                current_rider.add_chrono(chrono_CP)              
                        old_rider = current_rider
                    i += 1
                new_race.save()
                datas_list_p.append(new_race.get_race())
                return True
            else:
                datas_list_p.append('Erreur pendant la récupération des données.')
        else:
            datas_list_p.append('Ressource non trouvée.')
        return False

