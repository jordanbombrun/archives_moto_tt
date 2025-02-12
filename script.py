import os
from bs4 import BeautifulSoup
from pilote import Pilote 

#############
# Functions
# extrait toutes les données pilotes et chronos depuis le tableau HTML
def extract_datas(pilotes):
    filename = 'pilote1.html'
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    all_rows = soup.find_all("tr")
    i = 0
    for row in all_rows:
        td_values = [td.text.strip() for td in row.find_all("td")]
        if (i == 0): 
            table_header = Pilote(td_values[0], td_values[1], td_values[2], td_values[3])
        else :
            pilotes.append(Pilote(td_values[0], td_values[1], td_values[2], td_values[3]))
            for j, chrono_CP in enumerate(td_values):
                if (j > 3):
                    pilotes[i-1].ajouter_chrono(chrono_CP)
        i += 1

# Donne le classement d'un pilote pour un CP donné
def current_rank(current_CP_P, pilote_P):
    current_position_L = 1
    current_chrono_L = pilote_P.chronos[current_CP_P-1]
    for k, pilote_L in enumerate(pilotes):
        if pilote_L != pilote_P and current_chrono_L > pilote_L.chronos[current_CP_P-1]:
            current_position_L +=1
    return current_position_L

    
#############
# Main code
pilotes = []
extract_datas(pilotes)

# classement pilote 2 au CP2 - ne marche pas ?
print("Position du pilote " + pilotes[2].nom + " au CP 2 : " + str(current_rank(2, pilotes[2])) + " à l'heure : " + pilotes[2].chronos[1])

# print(pilotes[2])
# print(pilote1)