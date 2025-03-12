import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
url = "http://www.motott.fr/live/HARD_GENTOR_2025/MANCHE1_PASSAGES_CH.html"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")  # Le parser "html.parser" corrige les erreurs
    # html_corrige = soup.prettify() 
    for tag in soup.find_all(True):
        if not tag.find_next_sibling() and tag.name in ["table", "tr", "td"]:
            print(f"Balise non fermée : <{tag.name}>")

    # print(response.text)  # Affiche le contenu HTML
else:
    print(f"Erreur {response.status_code}")

# soup = BeautifulSoup(response.text, "html.parser")

# print(soup.title.text)  # Titre de la page
