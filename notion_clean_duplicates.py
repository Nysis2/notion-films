import requests
import os
from dotenv import load_dotenv

# Charger les clés API depuis un fichier .env
load_dotenv()

# Clés API Notion
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Headers pour Notion API
HEADERS_NOTION = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 🔍 Récupérer les films enregistrés dans Notion
def get_movies_from_notion():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    all_movies = []
    has_more = True
    payload = {}

    while has_more:
        response = requests.post(url, headers=HEADERS_NOTION, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            for entry in results:
                movie_title = entry["properties"]["Title"]["title"][0]["text"]["content"]
                movie_id = entry["id"]
                all_movies.append((movie_title, movie_id))
            
            has_more = data.get("has_more", False)
            payload = {"start_cursor": data["next_cursor"]} if has_more else {}
        else:
            print("❌ Erreur Notion lors de la récupération :", response.json())
            return []

    return all_movies

# ❌ Supprimer un film de Notion
def delete_movie(movie_id):
    url = f"https://api.notion.com/v1/pages/{movie_id}"
    response = requests.patch(url, headers=HEADERS_NOTION, json={"archived": True})
    
    if response.status_code == 200:
        print(f"🗑 Supprimé : {movie_id}")
    else:
        print("❌ Erreur suppression :", response.json())

# 🏷 Supprimer les doublons en gardant une seule occurrence
def remove_duplicates():
    movies = get_movies_from_notion()
    
    seen_titles = set()
    duplicates = []

    for title, movie_id in movies:
        if title in seen_titles:
            duplicates.append(movie_id)
        else:
            seen_titles.add(title)

    # Supprimer les doublons
    for movie_id in duplicates:
        delete_movie(movie_id)

    print(f"✅ {len(duplicates)} doublon(s) supprimé(s).")

# 🚀 Exécuter le script
if __name__ == "__main__":
    remove_duplicates()
