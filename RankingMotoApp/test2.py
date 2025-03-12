import requests
from bs4 import BeautifulSoup, Comment

url = "http://www.motott.fr/live/HARD_GENTOR_2025/MANCHE1_PASSAGES_CH.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_html(html):
    """
    Corrige automatiquement les erreurs HTML avec BeautifulSoup.
    Supprime également les balises inutiles (commentaires, balises vides, etc.).
    """
    soup = BeautifulSoup(html, "html.parser")

    # Supprimer les commentaires HTML
    # for comment in soup(text=lambda text: isinstance(text, Comment)):
    #     comment.extract()

    # Supprimer les balises vides
    for tag in soup.find_all():
        if tag.name not in ["td", "tr", "th"] and not tag.text.strip():
            tag.extract()

    return soup

def get_table_rows(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Correction automatique du HTML
        # soup = clean_html(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        table_data = []

        # Parcourir toutes les lignes <tr> sans fusionner plusieurs lignes
        rows = soup.find_all("tr")
        for row in rows:
            # Trouver uniquement les cellules enfants directs de la ligne actuelle
            cells = [td.text.strip() for td in row.find_all("td", recursive=False)]
            if cells:  # N'ajoute que les lignes non vides
                table_data.append(cells)

        return table_data
    else:
        print(f"Erreur {response.status_code}")
        return []

# Exemple d'utilisation
rows = get_table_rows(url)
for row in rows:
    print(row)
