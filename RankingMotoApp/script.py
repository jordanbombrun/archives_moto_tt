import os
import sys
from datetime import date, time
from bs4 import BeautifulSoup
import requests
from rider import Rider 
from race import Race

#############
# CONST
#############
HEADERS_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


#############
# GLOBALS
#############
race = Race('MyRace', date(2025, 1, 26))


#############
# Functions
#############
# Traite toutes les données pilotes et chronos pour alimenter les chronos des pilotes
def parse_datas(url_p, race):
    soup = get_datas_from_source(url_p)
    if (soup is not None):
        rows = soup.find_all("tr")
        i = 0
        old_rider = None 
        current_rider = None
        init_nb_lap = False
        for row in rows:
            td_values = [td.text.strip() for td in row.find_all("td", recursive=False)]
            if (i == 3): # ligne des entêtes
                race.nb_CP = len(td_values) - 4 
            elif (i > 3): # filtre les 1ères lignes 
                if not init_nb_lap:
                    race.nb_tours = int(td_values[3])
                    init_nb_lap = True
                if (td_values[1] != ''):
                    current_line_number = td_values[1]
                if (old_rider is None or current_line_number != old_rider.number): # nouveau pilote
                    current_rider = Rider(td_values[0], td_values[1], td_values[2], td_values[3])
                    current_rider.chronos_tour_CP = [[] for _ in range(int(race.nb_tours))]
                    current_rider.positions_tour_CP = [[] for _ in range(int(race.nb_tours))]
                    race.riders.append(current_rider)
                else : # même pilote, mais tour différent
                    current_rider.current_tour = td_values[3]
                for j, chrono_CP in enumerate(td_values):
                    if (j > 3):
                        current_rider.add_chrono(chrono_CP)              
                old_rider = current_rider
            i += 1
    else:
        return None

# Récupére le contenu sur le web ou dans un fichier local
# renvoie un objet BeautifulSoup si OK , un string vide si KO
def get_datas_from_source(url_p):
    if (url_p.startswith('http')):
        response = requests.get(url_p, headers=HEADERS_USER_AGENT)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
    else:
        html_content = ''
        with open(url_p, "r", encoding="utf-8") as file:
            html_content = file.read()
            if html_content != '':
                return BeautifulSoup(html_content, "html.parser")
    return None

# Donne le classement d'un pilote pour un tour et un CP donnés
# ex : get_current_rank(1, 1, ...) : tour 1 et CP 1  
def get_current_rank(current_tour_P, current_CP_P, rider_P):
    current_position_L = 1
    if (len(rider_P.chronos_tour_CP[current_tour_P-1]) == 0):
        return 0
    current_chrono_L = rider_P.chronos_tour_CP[current_tour_P-1][current_CP_P-1]
    if current_chrono_L == time(0, 0): # cas d'un CP non tracké/vide
        return 0
    for k, rider_to_compare in enumerate(race.riders):
        if (len(rider_to_compare.chronos_tour_CP[current_tour_P-1]) > 0):
            chrono_to_compare = rider_to_compare.chronos_tour_CP[current_tour_P-1][current_CP_P-1]
            if rider_to_compare != rider_P and chrono_to_compare != time(0,0) and current_chrono_L > chrono_to_compare:
                current_position_L +=1
    return current_position_L

    
#############
# Main code
#############

# Vérifier les arguments

# avec 2 arguments : url et numéro du pilote
# if len(sys.argv) > 2:
#     url = sys.argv[1]  
#     number_arg = sys.argv[2]  
# else:
#     print("Il manque un ou des argument(s).")

def process(rider_number_P, url_P):
    # url = os.path.join(os.path.dirname(__file__), 'templates', 'ALESTREM2025.html')
    # avec 1 arguments : numéro du pilote
    if (int(rider_number_P) > 0):
        parse_datas(url_P, race)
        rider_P = race.get_rider_by_number(rider_number_P)
        if (rider_P is not None):
            # ajout de tous les chronos de tous les tours pour 1 pilote
            for tour_L in range(race.nb_laps):    
                for cp_L in range(race.nb_CP) :
                    rider_P.positions_tour_CP[tour_L].append(get_current_rank(tour_L+1, cp_L+1, rider_P))
            # rider_P.print_positions()
        else:
            print("Aucun pilote trouvé pour le numéro " + rider_number_P)
    else:
        print('Argument du script non valide : ' + rider_number_P + ' doit être > 0')
    return rider_P.final_position
    
    



