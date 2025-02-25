import os
import sys
from datetime import date, time
from bs4 import BeautifulSoup
from pilote import Pilote 
from race import Race

#############
# Functions
# extrait toutes les données pilotes et chronos depuis le tableau HTML
def extract_datas(filename):
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    all_rows = soup.find_all("tr")
    i = 0
    old_pilote = None 
    current_pilote = None
    for row in all_rows:
        td_values = [td.text.strip() for td in row.find_all("td")]
        if (i == 0): 
            table_header = Pilote(td_values[0], td_values[1], td_values[2], td_values[3])
        else :
            if (i == 1): # init le nombre de tours de la course
                race.nb_tours = int(td_values[3])
                current_line_number = td_values[1]
            elif (td_values[1] != ''):
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
    # init le nombre de CP par tour
    race.nb_CP = len(race.pilotes[0].chronos_tour_CP[0])  


# Donne le classement d'un pilote pour un tour et un CP donné
# ex : get_current_rank(1, 1, ...) : tour 1 et CP 1  
def get_current_rank(current_tour_P, current_CP_P, pilote_P):
    current_position_L = 1
    current_chrono_L = pilote_P.chronos_tour_CP[current_tour_P-1][current_CP_P-1]
    for k, pilote_L in enumerate(race.pilotes):
        if current_chrono_L == time(0, 0):
            current_position_L = 0
            break
        chrono_to_compare = pilote_L.chronos_tour_CP[current_tour_P-1][current_CP_P-1]
        if pilote_L != pilote_P and chrono_to_compare != time(0,0) and current_chrono_L > chrono_to_compare:
            current_position_L +=1
    return current_position_L

    
#############
# Main code

# Vérifier qu'un argument a été passé
if len(sys.argv) > 1:
    number_arg = sys.argv[1]  # Premier argument après le nom du script
else:
    print("Aucun argument fourni.")

race = Race("Alestrem", date(2025, 1, 26))
extract_datas("pilote_3tours.html")
pilote_arg = race.get_pilote_by_number(number_arg)
if (pilote_arg is not None):
    # ajout de tous les chronos de tous les tours pour 1 pilote
    for tour_L in range(race.nb_tours):    
        for cp_L in range(race.nb_CP) :
            pilote_arg.positions_tour_CP[tour_L].append(get_current_rank(tour_L+1, cp_L+1, pilote_arg))
else:
    print("Aucun pilote trouvé pour le numéro " + number_arg)

print("")



