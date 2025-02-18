import requests
import os
import json
from dotenv import load_dotenv

# Charger les clés API depuis un fichier .env
load_dotenv()

# 🔹 Config Notion API
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
HEADERS_NOTION = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 🔹 Fonction pour récupérer les films
def get_movies_from_notion():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    response = requests.post(url, headers=HEADERS_NOTION)

    if response.status_code == 200:
        movies = []
        data = response.json()["results"]

        for entry in data:
            title = entry["properties"]["Title"]["title"][0]["text"]["content"]
            rating = entry["properties"]["Rating"]["number"]
            genre = entry["properties"]["Genre"]["rich_text"][0]["text"]["content"]

            # 🖼 Vérifier le type du champ Poster
            if "url" in entry["properties"]["Poster"]:  
                poster = entry["properties"]["Poster"]["url"]  # Format URL direct
            elif "files" in entry["properties"]["Poster"] and entry["properties"]["Poster"]["files"]:
                poster = entry["properties"]["Poster"]["files"][0]["file"]["url"]  # Format fichier Notion
            else:
                poster = "https://via.placeholder.com/250x350?text=No+Image"  # Image par défaut

            # 🔗 Vérifier le champ Trailer
            if "url" in entry["properties"]["Trailer"]:
                trailer = entry["properties"]["Trailer"]["url"]
            else:
                trailer = None

            movies.append({
                "title": title,
                "rating": rating,
                "genre": genre,
                "poster": poster,
                "trailer": trailer
            })

        return movies
    else:
        print("Erreur API Notion :", response.json())
        return []


# 🔹 Sauvegarde des données en JSON
movies = get_movies_from_notion()
with open("movies.json", "w", encoding="utf-8") as file:
    json.dump(movies, file, indent=4, ensure_ascii=False)

print("✅ Données récupérées et sauvegardées !")
