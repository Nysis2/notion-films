# Notion Movie Sync

Ce projet permet de synchroniser quotidiennement les films en salle depuis **TMDb** avec une base de données **Notion**. L'automatisation est gérée via **GitHub Actions**.

## 🚀 Fonctionnalités
- Récupération des **films actuellement en salle** via l'API **TMDb**.
- Mise à jour de la **base Notion** avec les nouveaux films.
- **Mise à jour automatique** des notes et bandes-annonces si elles changent.
- **Exécution quotidienne** via GitHub Actions.

---

## 📌 Configuration
### 1️⃣ Cloner le projet
```sh
git clone https://github.com/VOTRE_UTILISATEUR/notion-movie-sync.git
cd notion-movie-sync
```

### 2️⃣ Installer les dépendances
Assurez-vous d'avoir **Python 3.x** installé, puis :
```sh
pip install -r requirements.txt
```

### 3️⃣ Obtenir les clés API
Vous aurez besoin des clés suivantes :
1. **TMDb API Key** → [Créer un compte TMDb](https://www.themoviedb.org/settings/api)
2. **Notion API Key** → [Créer une intégration Notion](https://www.notion.so/my-integrations)
3. **Notion Database ID** → ID de votre base de données Notion

Ajoutez-les dans les **secrets GitHub** (voir section suivante).

---

## 🔑 Configuration des Secrets GitHub
1. Allez dans votre **repo GitHub**.
2. Accédez à **Settings** → **Secrets and variables** → **Actions**.
3. Ajoutez les secrets suivants :
   - `NOTION_API_KEY`
   - `TMDB_API_KEY`
   - `NOTION_DATABASE_ID`

---

## ⚙️ Configuration de GitHub Actions
Le workflow GitHub Actions exécute le script tous les jours à **03:00 UTC**.

### 📄 Fichier `.github/workflows/notion_update.yml`
```yaml
name: Notion Daily Update

on:
  schedule:
    - cron: "0 3 * * *"  # Exécution quotidienne à 03:00 UTC
  workflow_dispatch:  # Permet de l'exécuter manuellement

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
      - name: Cloner le repo
        uses: actions/checkout@v3

      - name: Configurer Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.x"

      - name: Installer les dépendances
        run: pip install requests python-dotenv

      - name: Exécuter le script
        env:
          NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
          TMDB_API_KEY: ${{ secrets.TMDB_API_KEY }}
          NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
        run: python notion_update.py
```

---

## 📌 Exécution Manuelle
Si vous souhaitez exécuter manuellement le script :
1. Allez dans **Actions** → **Notion Daily Update**.
2. Cliquez sur **Run Workflow**.

---

## 🛠 Développement et Tests
Pour exécuter le script localement :
```sh
export NOTION_API_KEY="votre_api_key"
export TMDB_API_KEY="votre_tmdb_api_key"
export NOTION_DATABASE_ID="votre_database_id"
python notion_update.py
```

---

## 📜 License
MIT License. Libre d'utilisation et de modification.

🚀 Bon développement !

