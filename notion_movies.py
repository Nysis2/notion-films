import requests
import os
from dotenv import load_dotenv
import datetime

# Charger les clés API depuis un fichier .env
load_dotenv()

# Clés API
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Headers pour Notion API
HEADERS_NOTION = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# URL API TMDb pour les films en salle en France
TMDB_URL = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=fr-FR&region=FR"

# 🔍 Récupérer les films enregistrés dans Notion
def get_existing_movies():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    all_movies = {}
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
                
                # Correction : extraire la valeur réelle du rating
                movie_rating = entry["properties"]["Rating"]["number"] if entry["properties"]["Rating"]["number"] is not None else 0.0
                
                # Correction : s'assurer que la bande-annonce est bien récupérée
                movie_trailer = entry["properties"]["Trailer"]["url"] if "url" in entry["properties"]["Trailer"] else None

                all_movies[movie_title] = {
                    "id": movie_id,
                    "rating": float(movie_rating),  # S'assurer que c'est un float
                    "trailer": movie_trailer
                }

            has_more = data.get("has_more", False)
            payload = {"start_cursor": data["next_cursor"]} if has_more else {}

        else:
            print("❌ Erreur Notion lors de la récupération :", response.json())
            return {}

    return all_movies


# 🔹 Récupérer la bande-annonce d'un film (YouTube)
def get_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        videos = response.json().get("results", [])
        for video in videos:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"

    return None  # Pas de bande-annonce disponible

# 📽 Récupérer les films en salle depuis TMDb
def get_movies():
    response = requests.get(TMDB_URL)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("Erreur TMDb:", response.json())
        return []

# 🔄 Mettre à jour un film si les données ont changé
def update_movie_in_notion(movie_id, new_rating, new_trailer):
    update_data = {"properties": {}}

    if new_rating is not None:
        update_data["properties"]["Rating"] = {"number": new_rating}

    if new_trailer is not None:
        update_data["properties"]["Trailer"] = {"url": new_trailer}

    response = requests.patch(f"https://api.notion.com/v1/pages/{movie_id}", headers=HEADERS_NOTION, json=update_data)

    if response.status_code == 200:
        print(f"🔄 Mis à jour : {movie_id}")
    else:
        print("❌ Erreur mise à jour :", response.json())

# ➕ Ajouter un film dans la base Notion
def add_movie_to_notion(movie):
    trailer_url = get_trailer(movie["id"])

    # Obtenir la date et l'heure actuelles
    updated_date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": movie["title"]}}]},
            "Release Date": {"rich_text": [{"text": {"content": movie["release_date"]}}]},
            "Rating": {"number": movie["vote_average"]},
            "Genre": {"rich_text": [{"text": {"content": " / ".join(get_genres(movie["genre_ids"]))}}]},
            "Poster": {"rich_text": [{"text": {"content": f'https://image.tmdb.org/t/p/w500{movie["poster_path"]}'}}]},
            "Trailer": {"url": trailer_url if trailer_url else None}
            "Updated Date": {"rich_text": [{"text": {"content": updated_date}}]}
        }
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS_NOTION, json=data)

    if response.status_code == 200:
        print(f"✅ Ajouté : {movie['title']}")
    else:
        print("❌ Erreur Notion:", response.json())

# 🔄 Convertir les IDs des genres en noms
def get_genres(genre_ids):
    genres = {
        28: "Action", 12: "Aventure", 16: "Animation", 35: "Comédie",
        80: "Crime", 99: "Documentaire", 18: "Drame", 10751: "Famille",
        14: "Fantastique", 36: "Histoire", 27: "Horreur", 10402: "Musique",
        9648: "Mystère", 10749: "Romance", 878: "Science-fiction", 10770: "Téléfilm",
        53: "Thriller", 10752: "Guerre", 37: "Western"
    }
    return [genres.get(id, "Inconnu") for id in genre_ids]

# 🚀 Exécuter le script
if __name__ == "__main__":
    existing_movies = get_existing_movies()  # Films déjà enregistrés
    movies = get_movies()  # Films en salle

    for movie in movies:
        trailer_url = get_trailer(movie["id"])
        if movie["title"] in existing_movies:
            movie_id = existing_movies[movie["title"]]["id"]
            old_rating = existing_movies[movie["title"]]["rating"]
            old_trailer = existing_movies[movie["title"]]["trailer"]

            # Vérification des changements
            if movie["vote_average"] != old_rating or trailer_url != old_trailer:
                print(f"📝 Mise à jour requise pour {movie['title']}")
                update_movie_in_notion(movie_id, movie["vote_average"], trailer_url)
            else:
                print(f"✅ Pas de changement pour {movie['title']}")
        else:
            add_movie_to_notion(movie)
