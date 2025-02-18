name: Notion Daily Update

on:
  schedule:
    - cron: "0 3 * * *"  # Exécution tous les jours à 03:00 UTC
  workflow_dispatch:  # Permet de lancer manuellement

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
        run: python notion_update.py
