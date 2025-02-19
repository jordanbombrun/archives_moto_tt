import os
from datetime import date, time
from bs4 import BeautifulSoup
from pilote import Pilote 
from course import Course

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
                course.nb_tours = td_values[3]
                current_line_number = td_values[1]
            elif (td_values[1] != ''):
                current_line_number = td_values[1]
            if (old_pilote is None or current_line_number != old_pilote.numero): # nouveau pilote
                current_pilote = Pilote(td_values[0], td_values[1], td_values[2], td_values[3])
                current_pilote.chronos = [[] for _ in range(int(course.nb_tours))]
                current_pilote.positions = [[] for _ in range(int(course.nb_tours))]
                course.pilotes.append(current_pilote)
            else : # même pilote, mais tour différent
                current_pilote.tour_courant = td_values[3]
            for j, chrono_CP in enumerate(td_values):
                if (j > 3):
                    current_pilote.ajouter_chrono(chrono_CP)
            old_pilote = current_pilote
        i += 1

# Donne le classement d'un pilote pour un CP donné
def get_current_rank(current_CP_P, pilote_P):
    current_position_L = 1
    current_chrono_L = pilote_P.chronos[current_CP_P]
    for k, pilote_L in enumerate(course.pilotes):
        if current_chrono_L == time(0, 0):
            current_position_L = 0
            break
        chrono_to_compare = pilote_L.chronos[current_CP_P]
        if pilote_L != pilote_P and chrono_to_compare != time(0,0) and current_chrono_L > chrono_to_compare:
            current_position_L +=1
    return current_position_L

    
#############
# Main code
course = Course("Alestrem", date(2025, 1, 26))
extract_datas("pilote_3tours.html")
course.nb_CP = len(course.pilotes[0].chronos)

# for current_CP in range(course.nb_CP):
#     course.pilotes[2].positions.append(get_current_rank(current_CP, course.pilotes[2]))

# positions
# print("### positions Young :")
# for current_CP in range(course.nb_CP):
#     print("CP " + str(current_CP+1) + " / pos " + str(course.pilotes[2].positions[current_CP]))


# pilote[2] : for each CP get_current_position > positions[]
# print("Young :")
# for current_CP in range(course.nb_CP):
#     print("CP " + str(current_CP+1) + " : " + str(get_current_rank(current_CP, course.pilotes[2])))

# print("Roman :")
# for current_CP in range(course.nb_CP):
#     print("CP " + str(current_CP+1) + " : " + str(get_current_rank(current_CP, course.pilotes[1])))

# print("Kabach :")
# for current_CP in range(course.nb_CP):
#     print("CP " + str(current_CP+1) + " : " + str(get_current_rank(current_CP, course.pilotes[0])))

# print("Position du pilote " + course.pilotes[2].nom + " au CP 2 : " + str(get_current_rank(2, course.pilotes[2])) + " à l'heure : " + str(course.pilotes[2].chronos[1]))
