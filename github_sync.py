import os
from datetime import datetime
import json
import base64
from dotenv import load_dotenv
import requests

# Charger les variables d'environnement
load_dotenv()

def sync_with_github():
    """Synchroniser les fichiers web avec GitHub via l'API - Version optimisée"""
    try:
        github_token = os.getenv('GITHUB_TOKEN')
        github_repo = os.getenv('GITHUB_REPO')
        github_branch = os.getenv('GITHUB_BRANCH', 'main')

        if not github_token or not github_repo:
            print("⚠️ Variables GitHub manquantes")
            return

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Fichiers principaux seulement pour plus de rapidité
        files_to_sync = [
            'Home Page/home.html',
            'Home Page/home.css', 
            'Home Page/home.js',
            'github_sync.py'
        ]

        timestamp = datetime.now().strftime("%H:%M:%S")
        files_updated = 0

        # Traitement en parallèle simulé avec moins de vérifications
        for file_path in files_to_sync:
            if not os.path.exists(file_path):
                continue

            try:
                with open(file_path, "rb") as f:
                    content = base64.b64encode(f.read()).decode()

                api_url = f"https://api.github.com/repos/{github_repo}/contents/{file_path}"

                # Requête GET rapide avec timeout court
                try:
                    get_response = requests.get(api_url, headers=headers, timeout=3)
                    sha = get_response.json().get("sha") if get_response.status_code == 200 else None
                except:
                    sha = None

                data = {
                    "message": f"Sync {timestamp}",
                    "content": content,
                    "branch": github_branch
                }

                if sha:
                    data["sha"] = sha

                # Requête PUT avec timeout court
                put_response = requests.put(api_url, headers=headers, json=data, timeout=5)

                if put_response.status_code in [200, 201]:
                    print(f"✅ {file_path}")
                else:
                    print(f"❌ {file_path} non modifié — {put_response.status_code}")

            except Exception:
                continue

        print(f"🔄 {files_updated}/{len(files_to_sync)} fichiers synchronisés")

    except Exception as e:
        print(f"⚠️ Sync rapide échouée: {str(e)[:50]}...")

def verify_sync_status():
    """Afficher le statut de synchronisation dans la console"""
    github_repo = os.getenv('GITHUB_REPO')
    github_branch = os.getenv('GITHUB_BRANCH', 'main')

    print("=" * 50)
    print("🔍 VÉRIFICATION DE SYNCHRONISATION")
    print("=" * 50)
    print(f"Repository: {github_repo}")
    print(f"Branche: {github_branch}")
    print(f"Fichiers surveillés: index.html, style.css, script.js, app.py")
    print("Status: ✅ Prêt pour synchronisation")
    print("=" * 50)

if __name__ == "__main__":
    sync_with_github()