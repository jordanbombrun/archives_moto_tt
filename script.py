import os
from bs4 import BeautifulSoup
from chrono import Chrono
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
                    pilotes[i-1].chronos.ajouter_temps(chrono_CP)
        i += 1


#############
# Main code
pilotes = []
extract_datas(pilotes)


# classement au CP1
print(pilotes[2])
# print(pilote1)