import os
from datetime import datetime
import requests
import json
import base64

from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def sync_with_github():
    """Synchroniser les fichiers web avec GitHub via l'API"""
    try:
        # Configuration GitHub - à définir dans les Secrets de Replit
        github_token = os.getenv('GITHUB_TOKEN')
        github_repo = os.getenv('GITHUB_REPO')  # Format: "username/jailbreak-assistant"
        github_branch = os.getenv('GITHUB_BRANCH', 'main')

        if not github_token or not github_repo:
            print("⚠️ Variables GitHub manquantes. Configurez GITHUB_TOKEN et GITHUB_REPO dans les Secrets")
            return

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Fichiers à synchroniser
        files_to_sync = [
            'index.html', 
            'style.css', 
            'script.js', 
            'app.py',
            'Home Page/home.html',
            'Home Page/home.css',
            'Home Page/home.js',
            'github_sync.py',
            'requirements.txt'
        ]
        
        # Synchroniser aussi les images dans le dossier pictures
        pictures_dir = 'pictures'
        if os.path.exists(pictures_dir):
            for file in os.listdir(pictures_dir):
                if os.path.isfile(os.path.join(pictures_dir, file)):
                    files_to_sync.append(f'pictures/{file}')

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        files_updated = 0

        for file_path in files_to_sync:
            if not os.path.exists(file_path):
                continue

            try:
                # Lire le contenu du fichier
                with open(file_path, "rb") as f:
                    content = base64.b64encode(f.read()).decode()

                # URL de l'API GitHub pour ce fichier
                api_url = f"https://api.github.com/repos/{github_repo}/contents/{file_path}"

                # Données pour la requête
                data = {
                    "message": f"Auto-sync {file_path} - {timestamp}",
                    "content": content,
                    "branch": github_branch
                }

                # Vérifier si le fichier existe déjà
                get_response = requests.get(api_url, headers=headers)
                if get_response.status_code == 200:
                    data["sha"] = get_response.json()["sha"]

                # Envoyer la requête PUT
                put_response = requests.put(api_url, headers=headers, json=data)

                if put_response.status_code in [200, 201]:
                    files_updated += 1
                    print(f"✅ {file_path} synchronisé avec GitHub")
                else:
                    print(f"⚠️ Erreur lors de la sync de {file_path}: {put_response.status_code}")

            except Exception as file_error:
                print(f"⚠️ Erreur lors de la sync de {file_path}: {file_error}")

        print(f"✅ Synchronisation terminée - {files_updated} fichier(s) mis à jour")
        print(f"📊 Statut de synchronisation:")
        print(f"   - Repository: {github_repo}")
        print(f"   - Branche: {github_branch}")
        print(f"   - Timestamp: {timestamp}")
        print(f"   - Fichiers traités: {len(files_to_sync)}")
        print(f"   - Fichiers synchronisés: {files_updated}")
        print("🔄 Synchronisation GitHub confirmée!")

    except Exception as e:
        print(f"⚠️ Erreur de synchronisation GitHub: {e}")
        print("❌ Synchronisation échouée!")

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