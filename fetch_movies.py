import requests
import os
import json
from datetime import datetime, timedelta
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
    movies = []
    next_cursor = None

    while True:
        body = {"page_size": 100}
        if next_cursor:
            body["start_cursor"] = next_cursor
        response = requests.post(url, headers=HEADERS_NOTION, json=body)

        if response.status_code != 200:
            print("Erreur API Notion :", response.json())
            break

        payload = response.json()
        data = payload["results"]

        for entry in data:
            title = entry["properties"]["Title"]["title"][0]["text"]["content"]
            rating = entry["properties"]["Rating"]["number"]
            genre = entry["properties"]["Genre"]["rich_text"][0]["text"]["content"]

            # 🖼 Vérifier le type du champ Poster
            if "Poster" in entry["properties"] and "rich_text" in entry["properties"]["Poster"]:
                poster_text = entry["properties"]["Poster"]["rich_text"]
                if poster_text:
                    poster = poster_text[0]["text"]["content"]  # ✅ Récupérer l'URL
                else:
                    poster = "https://via.placeholder.com/250x350?text=No+Image"
            else:
                poster = "https://via.placeholder.com/250x350?text=No+Image"

            # 🔗 Vérifier le champ Trailer
            if "Trailer" in entry["properties"] and "url" in entry["properties"]["Trailer"]:
                trailer = entry["properties"]["Trailer"]["url"]
            else:
                trailer = None

            def rich_text(key):
                prop = entry["properties"].get(key, {}).get("rich_text", [])
                return prop[0]["text"]["content"] if prop else ""

            release_date = rich_text("Release Date") or None
            overview = rich_text("Overview")
            tagline = rich_text("Tagline")
            backdrop = rich_text("Backdrop") or None
            runtime = entry["properties"].get("Runtime", {}).get("number")

            movies.append({
                "title": title,
                "rating": rating,
                "genre": genre,
                "poster": poster,
                "trailer": trailer,
                "release_date": release_date,
                "overview": overview,
                "tagline": tagline,
                "runtime": runtime,
                "backdrop": backdrop,
            })

        if payload.get("has_more"):
            next_cursor = payload["next_cursor"]
        else:
            break

    return movies

# 🔹 Filtre : films des 6 dernières semaines uniquement
def is_recent(movie, weeks=6):
    rd = movie.get("release_date")
    if not rd:
        return True  # on garde si pas de date
    try:
        release = datetime.strptime(rd, "%Y-%m-%d")
        return release >= datetime.now() - timedelta(weeks=weeks)
    except ValueError:
        return True

# 🔹 Sauvegarde des données en JSON
all_movies = get_movies_from_notion()
recent = [m for m in all_movies if is_recent(m)]

# Dédoublonnage par titre (on garde le premier)
seen = set()
movies = []
for m in recent:
    if m["title"] not in seen:
        seen.add(m["title"])
        movies.append(m)

print(f"{len(all_movies)} films recus, {len(recent)} recents, {len(movies)} apres dedoublonnage")

with open("movies.json", "w", encoding="utf-8") as file:
    json.dump(movies, file, indent=4, ensure_ascii=False)
