# 🎬 Notion Films

Ce projet permet de synchroniser quotidiennement les **films en salle** depuis **TMDb** avec une base de données **Notion**.  
L'automatisation est gérée via **GitHub Actions**, et l'affichage des films est hébergé sur **Netlify**, avec une intégration dans **Notion**.

---

## 🚀 Fonctionnalités
✅ Récupération des **films actuellement en salle** via l'API **TMDb**.  
✅ Mise à jour de la **base Notion** avec les nouveaux films.  
✅ **Mise à jour automatique** des notes et bandes-annonces si elles changent.  
✅ **Exécution quotidienne** via **GitHub Actions**.  
✅ **Affichage Web** via **Netlify**, intégré à **Notion** via un `embed`.  

---

## 📌 Architecture du projet
<div align="center">
   <img src="https://github.com/user-attachments/assets/d9a0c4d4-2505-42db-b3c0-31ac009c7981" alt="Architecture du projet" width="800">
</div>


### **📌 Explication des interactions**
1. **Récupération des films depuis TMDb API**  
   - `fetch_movies.py` interroge **The Movie Database (TMDb)** pour récupérer **les films en cours de diffusion**.  
   - Ces films sont envoyés à **Notion API** pour être stockés dans **Notion DB**.

2. **Mise à jour automatique via GitHub Actions (CRON)**  
   - `notion_update.yml` s'exécute **tous les jours** via GitHub Actions.  
   - Il lance `fetch_movies.py` pour **mettre à jour la base Notion** avec les nouveaux films.

3. **Export des films en JSON pour le site web**  
   - `fetch_movies.py` génère **`movies.json`**, un fichier contenant tous les films récupérés depuis **Notion DB**.  
   - `index.html` utilise ce fichier **via JavaScript** pour afficher les films sous forme de **cartes interactives**.

4. **Hébergement sur Netlify**  
   - `index.html` est **hébergé sur Netlify** et peut être consulté via une URL (`https://ton-site.netlify.app`).  
   - **Chaque mise à jour du JSON rafraîchit automatiquement les films affichés sur Netlify.**

5. **Affichage du site Netlify dans Notion**  
   - Une **page Notion** utilise un **embed (`/embed`)** pour afficher le site Netlify en **direct** dans Notion.  
   - Les utilisateurs peuvent voir **les films à jour directement dans Notion**, sans quitter l'interface.

---

## 📌 Configuration
### 1️⃣ Cloner le projet
```sh
git clone https://github.com/VOTRE_UTILISATEUR/notion-movie-sync.git
cd notion-movie-sync
```

### 2️⃣ Installer les dépendances
```sh
pip install -r requirements.txt
```

### 3️⃣ Obtenir les clés API
Vous aurez besoin des clés suivantes :
1. **TMDb API Key** → [Créer un compte TMDb](https://www.themoviedb.org/settings/api)
2. **Notion API Key** → [Créer une intégration Notion](https://www.notion.so/my-integrations)
3. **Notion Database ID** → ID de votre base de données Notion

Ajoutez-les dans un fichier `.env` (local) ou dans **GitHub Secrets**.

---

## ⚙️ Configuration de GitHub Actions
Le workflow GitHub Actions **`notion_update.yml`** exécute automatiquement le script **tous les jours à 03:00 UTC**.

Pour voir les logs :
1. Aller dans **GitHub** → **Repo** → **Actions**.
2. Sélectionner le workflow **Notion Daily Update**.
3. Vérifier l’état d’exécution.

---

## 📌 Exécution Manuelle
Si vous souhaitez exécuter manuellement le script :
1. Allez dans **Actions** → **Notion Daily Update**.
2. Cliquez sur **Run Workflow**.

---

## 📜 License
MIT License. Libre d'utilisation et de modification.

🚀 **Bon développement !**
