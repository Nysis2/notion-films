import requests
import os
from dotenv import load_dotenv
from difflib import SequenceMatcher

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
            print("ERREUR Notion lors de la recuperation :", response.json())
            return []

    return all_movies

# ❌ Supprimer un film de Notion
def delete_movie(movie_id):
    url = f"https://api.notion.com/v1/pages/{movie_id}"
    response = requests.patch(url, headers=HEADERS_NOTION, json={"archived": True})
    
    if response.status_code == 200:
        print(f"SUPPRIME : {movie_id}")
    else:
        print("ERREUR suppression :", response.json())

def are_titles_similar(title1, title2):
    return SequenceMatcher(None, title1.lower(), title2.lower()).ratio() > 0.8

# 🏷 Supprimer les doublons en gardant une seule occurrence
def remove_duplicates():    
    movies = get_movies_from_notion()
    
    seen_titles = []
    duplicates = []

    for title, movie_id in movies:
        normalized_title = title.lower()
        
        if any(are_titles_similar(normalized_title, seen) for seen in seen_titles):
            duplicates.append(movie_id)
        else:
            seen_titles.append(normalized_title)
    
    for movie_id in duplicates:
        delete_movie(movie_id)
    
    print(f"{len(duplicates)} doublon(s) supprimes.")

# 🚀 Exécuter le script
if __name__ == "__main__":
    remove_duplicates()
