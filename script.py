import os
from bs4 import BeautifulSoup

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
for row in all_rows:
    td_values = [td.text.strip() for td in row.find_all("td")]
    print(td_values)