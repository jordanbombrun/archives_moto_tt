import os
import sys
from datetime import date, time
from bs4 import BeautifulSoup
import requests
from pilote import Pilote 
from race import Race

#############
# CONST
#############
HEADERS_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

#############
# Functions
#############
# Traite toutes les données pilotes et chronos pour alimenter les chronos des pilotes
def parse_datas(url_p, race):
    soup = get_datas_from_source(url_p)
    if (soup is not None):
        rows = soup.find_all("tr")
        i = 0
        old_pilote = None 
        current_pilote = None
        init_nb_tour = False
        for row in rows:
            td_values = [td.text.strip() for td in row.find_all("td", recursive=False)]
            if (i == 3): # ligne des entêtes
                race.nb_CP = len(td_values) - 4 
            elif (i > 3): # filtre les 1ères lignes 
                if not init_nb_tour:
                    race.nb_tours = int(td_values[3])
                    init_nb_tour = True
                if (td_values[1] != ''):
                    current_line_number = td_values[1]
                if (old_pilote is None or current_line_number != old_pilote.number): # nouveau pilote
                    current_pilote = Pilote(td_values[0], td_values[1], td_values[2], td_values[3])
                    current_pilote.chronos_tour_CP = [[] for _ in range(int(race.nb_tours))]
                    current_pilote.positions_tour_CP = [[] for _ in range(int(race.nb_tours))]
                    race.pilotes.append(current_pilote)
                else : # même pilote, mais tour différent
                    current_pilote.current_tour = td_values[3]
                for j, chrono_CP in enumerate(td_values):
                    if (j > 3):
                        current_pilote.add_chrono(chrono_CP)              
                old_pilote = current_pilote
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
def get_current_rank(current_tour_P, current_CP_P, pilote_P):
    current_position_L = 1
    if (len(pilote_P.chronos_tour_CP[current_tour_P-1]) == 0):
        return 0
    current_chrono_L = pilote_P.chronos_tour_CP[current_tour_P-1][current_CP_P-1]
    if current_chrono_L == time(0, 0): # cas d'un CP non tracké/vide
        return 0
    for k, pilote_to_compare in enumerate(race.pilotes):
        if (len(pilote_to_compare.chronos_tour_CP[current_tour_P-1]) > 0):
            chrono_to_compare = pilote_to_compare.chronos_tour_CP[current_tour_P-1][current_CP_P-1]
            if pilote_to_compare != pilote_P and chrono_to_compare != time(0,0) and current_chrono_L > chrono_to_compare:
                current_position_L +=1
    return current_position_L

    
#############
# Main code
#############

# Vérifier les arguments
if len(sys.argv) > 2:
    url = sys.argv[1]  
    number_arg = sys.argv[2]  
else:
    print("Il manque un ou des argument(s).")

race = Race('MyRace', date(2025, 1, 26))
parse_datas(url, race)
pilote_arg = race.get_pilote_by_number(number_arg)
if (pilote_arg is not None):
    # ajout de tous les chronos de tous les tours pour 1 pilote
    for tour_L in range(race.nb_tours):    
        for cp_L in range(race.nb_CP) :
            pilote_arg.positions_tour_CP[tour_L].append(get_current_rank(tour_L+1, cp_L+1, pilote_arg))
    pilote_arg.print_positions()
else:
    print("Aucun pilote trouvé pour le numéro " + number_arg)

print("")



