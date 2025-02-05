import os
from bs4 import BeautifulSoup
from chrono import Chrono
from pilote import Pilote 

# print(os.getcwd())
filename = 'pilote1.html'
 
# 1- lecture html
with open(filename, "r", encoding="utf-8") as file:
    html_content = file.read()

# print(html_content)  # Vérifie si le contenu est bien chargé

# 2 - extraction headers
soup = BeautifulSoup(html_content, "html.parser")

first_row = soup.find_all("tr")[0]
first_row_td_values = [td.text.strip() for td in first_row.find_all("td")]
# print(first_row_td_values)

# 3 - extraction 1ère ligne de données
sec_row = soup.find_all("tr")[1]
sec_row_td_values = [td.text.strip() for td in sec_row.find_all("td")]
# print(sec_row_td_values)

# 4 - extraction toutes les lignes
all_rows = soup.find_all("tr")
i = 0
for row in all_rows:
    td_values = [td.text.strip() for td in row.find_all("td")]
    if (i == 0): 
        table_header = Pilote(td_values[0], td_values[1], td_values[2], td_values[3])
    elif (i == 1):
        pilote1 = Pilote(td_values[0], td_values[1], td_values[2], td_values[3])
        pilote1.chronos.ajouter_temps(td_values[4], td_values[5], td_values[6], td_values[7])
    i += 1
    # print(td_values)


# classement au CP1
print(pilote1)
# print(pilote1)