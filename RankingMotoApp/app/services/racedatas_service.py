from datetime import date, time
import os
from bs4 import BeautifulSoup
import requests
from RankingMotoApp.app.models.race import Race
from RankingMotoApp.app.models.rider import Rider
from RankingMotoApp.app.models.participation import Participation
from RankingMotoApp.app.models.participation import Participation
from RankingMotoApp.app.dao.participation_dao import *


class RaceDatasService:
    #############
    # CONST
    #############
    HEADERS_USER_AGENT = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    #############
    # Functions
    #############
    # Traite toutes les données pilotes et chronos pour alimenter les chronos des pilotes
    # Retourne True si ok, False sinon
    def parse_datas(self, race :Race, soup :BeautifulSoup) -> bool:
        try:
            if soup is not None:
                rows = soup.find_all("tr")
                i = 0
                old_number = None
                current_participation = None
                init_nb_lap = False

                for row in rows:
                    td_values = [td.text.strip() for td in row.find_all("td", recursive=False)]

                    if (i == 3):  # ligne des entêtes
                        race.nb_CP = max(0, len(td_values) - 4)
                    elif (i > 3):  # filtre les 1ères lignes
                        if not init_nb_lap:
                            try:
                                race.nb_laps = int(td_values[3])
                            except Exception:
                                race.nb_laps = 0
                            init_nb_lap = True

                        current_line_number = td_values[1] if len(td_values) > 1 else ''

                        # nouveau pilote / nouvelle participation
                        if current_line_number != '' and (old_number is None or current_line_number != old_number):
                            rider_name = td_values[2] if len(td_values) > 2 else ''
                            try:
                                final_pos = int(td_values[0]) if td_values[0] != '' else None
                            except Exception:
                                final_pos = None
                            try:
                                number = int(td_values[1]) if td_values[1] != '' else None
                            except Exception:
                                number = None
                            try:
                                current_lap = int(td_values[3]) if td_values[3] != '' else 0
                            except Exception:
                                current_lap = 0

                            rider = Rider()
                            rider.name = rider_name
                            current_participation = Participation()
                            current_participation.race = race
                            current_participation.rider = rider
                            current_participation.final_position = final_pos
                            current_participation.number = number

                            nb_laps = int(race.nb_laps) if getattr(race, "nb_laps", None) else 0
                            current_participation.chronos_lap_CP = [[] for _ in range(nb_laps)]
                            current_participation.positions_lap_CP = [[] for _ in range(nb_laps)]

                            race.participations.append(current_participation)  # Changed from riders.append()

                        else:  # même pilote, mais tour différent
                            if current_participation is not None:
                                try:
                                    current_participation.current_lap = int(td_values[3]) if td_values[3] != '' else current_participation.current_lap
                                except Exception:
                                    pass

                        # ajout des chronos/positions pour la participation courante
                        for j, chrono_CP in enumerate(td_values):
                            if (j > 3) and current_participation is not None:
                                current_participation.add_chrono(chrono_CP)

                        old_number = str(current_participation.number) if (current_participation and current_participation.number is not None) else old_number

                    i += 1
                return True
            else:
                return False
        except Exception as e:
            # todo : ajout logs BDD d'import
            return False

    # Récupére le contenu sur le web ou dans un fichier local
    # Retourne le contenu BeautifulSoup si ok, None sinon
    def collect_datas_from_source(self, url_p :str) -> BeautifulSoup | None:
        try:
            if (url_p.startswith('http')):
                response = requests.get(url_p, headers=self.HEADERS_USER_AGENT)
                if response.status_code == 200:
                    raw_datas_p = BeautifulSoup(response.text, "html.parser")
                    return raw_datas_p
            else:
                html_content = ''
                current_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(current_dir, url_p)
                with open(file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()
                    if html_content != '':
                        raw_datas_p = BeautifulSoup(html_content, "html.parser")
                        return raw_datas_p
            return None
        except Exception as e:
            return None

    # Donne le classement d'un pilote pour un tour et un CP donnés
    # ex : get_current_rank(1, 1, ...) : tour 1 et CP 1  
    def get_current_rank(self, current_lap_P, current_CP_P, rider_P, race_p):
        current_position_L = 1
        if (len(rider_P.chronos_lap_CP[current_lap_P-1]) == 0):
            return 0
        current_chrono_L = rider_P.chronos_lap_CP[current_lap_P-1][current_CP_P-1]
        if current_chrono_L == time(0, 0): # cas d'un CP non tracké/vide
            return 0
        for k, rider_to_compare in enumerate(race_p.riders):
            if (len(rider_to_compare.chronos_lap_CP[current_lap_P-1]) > 0):
                chrono_to_compare = rider_to_compare.chronos_lap_CP[current_lap_P-1][current_CP_P-1]
                if rider_to_compare != rider_P and chrono_to_compare != time(0,0) and current_chrono_L > chrono_to_compare:
                    current_position_L +=1
        return current_position_L

    def get_chronos_by_participation(self, participation_id_p :int):
        return dao_get_chronos_by_participation(participation_id_p)




