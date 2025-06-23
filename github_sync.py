
import os
from datetime import datetime
import json
import base64
from dotenv import load_dotenv
import requests
import hashlib

# Charger les variables d'environnement
load_dotenv()

def get_file_hash(file_path):
    """Calculer le hash SHA-256 d'un fichier"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def pull_from_github():
    """Extraire TOUS les fichiers depuis GitHub vers le projet local"""
    try:
        github_token = os.getenv('GITHUB_TOKEN')
        github_repo = os.getenv('GITHUB_REPO')
        github_branch = os.getenv('GITHUB_BRANCH', 'main')

        if not github_token or not github_repo:
            print("⚠️ Variables GitHub manquantes (GITHUB_TOKEN, GITHUB_REPO)")
            print("Vérifiez votre fichier .env")
            return False

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Fichiers à extraire depuis GitHub
        files_to_pull = [
            'Home Page/home.html',
            'Home Page/home.css', 
            'Home Page/home.js',
            'Values Page/values.html',
            'Values Page/values.css',
            'Values Page/values.js',
            'app.py',
            'github_sync.py',
            '.replit',
            'requirements.txt',
            'pictures/README.md'
        ]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        files_downloaded = 0
        files_created = 0

        print(f"⬇️ Début d'extraction depuis GitHub - {timestamp}")
        print(f"Repository: {github_repo}")
        print(f"Branche: {github_branch}")
        print("-" * 50)

        for file_path in files_to_pull:
            try:
                api_url = f"https://api.github.com/repos/{github_repo}/contents/{file_path}"
                
                # Faire la requête GET vers GitHub
                response = requests.get(api_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    file_data = response.json()
                    
                    # Décoder le contenu base64
                    content_b64 = file_data.get('content', '')
                    if content_b64:
                        try:
                            file_content = base64.b64decode(content_b64)
                            
                            # Créer les dossiers si nécessaire
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            
                            # Vérifier si le fichier existe déjà localement
                            file_exists = os.path.exists(file_path)
                            
                            # Écrire le fichier
                            with open(file_path, 'wb') as f:
                                f.write(file_content)
                            
                            if file_exists:
                                print(f"✅ {file_path} - Mis à jour")
                                files_downloaded += 1
                            else:
                                print(f"🆕 {file_path} - Créé")
                                files_created += 1
                                
                        except Exception as decode_error:
                            print(f"❌ Erreur décodage {file_path}: {str(decode_error)}")
                    else:
                        print(f"⚠️ {file_path} - Contenu vide")
                        
                elif response.status_code == 404:
                    print(f"⚠️ {file_path} - Non trouvé sur GitHub")
                else:
                    print(f"❌ {file_path} - Erreur {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Erreur réseau pour {file_path}: {str(e)}")
            except Exception as e:
                print(f"❌ Erreur générale pour {file_path}: {str(e)}")

        print(f"\n📊 Résumé d'extraction:")
        print(f"   • Fichiers mis à jour: {files_downloaded}")
        print(f"   • Fichiers créés: {files_created}")
        print(f"   • Total traité: {files_downloaded + files_created}/{len(files_to_pull)}")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"⚠️ Erreur générale d'extraction: {str(e)}")
        return False

def sync_with_github():
    """Synchroniser TOUS les fichiers web avec GitHub via l'API (PUSH)"""
    try:
        github_token = os.getenv('GITHUB_TOKEN')
        github_repo = os.getenv('GITHUB_REPO')
        github_branch = os.getenv('GITHUB_BRANCH', 'main')

        if not github_token or not github_repo:
            print("⚠️ Variables GitHub manquantes (GITHUB_TOKEN, GITHUB_REPO)")
            print("Vérifiez votre fichier .env")
            return False

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Test de connexion à l'API GitHub
        test_url = f"https://api.github.com/repos/{github_repo}"
        try:
            test_response = requests.get(test_url, headers=headers, timeout=10)
            if test_response.status_code == 404:
                print(f"❌ Repository '{github_repo}' non trouvé ou accès refusé")
                return False
            elif test_response.status_code != 200:
                print(f"❌ Erreur d'accès au repository: {test_response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Impossible de se connecter à GitHub: {str(e)}")
            return False

        # Tous les fichiers à synchroniser
        files_to_sync = [
            'Home Page/home.html',
            'Home Page/home.css', 
            'Home Page/home.js',
            'Values Page/values.html',
            'Values Page/values.css',
            'Values Page/values.js',
            'app.py',
            'github_sync.py',
            '.replit',
            'requirements.txt'
        ]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        files_updated = 0
        files_created = 0
        files_skipped = 0

        print(f"⬆️ Début de synchronisation vers GitHub - {timestamp}")
        print(f"Repository: {github_repo}")
        print(f"Branche: {github_branch}")
        print("-" * 50)

        for file_path in files_to_sync:
            if not os.path.exists(file_path):
                print(f"⚠️ Fichier non trouvé localement: {file_path}")
                continue

            try:
                # Lire le contenu du fichier local
                with open(file_path, "rb") as f:
                    file_content = f.read()
                    content_b64 = base64.b64encode(file_content).decode()

                api_url = f"https://api.github.com/repos/{github_repo}/contents/{file_path}"

                # Vérifier si le fichier existe sur GitHub
                sha = None
                file_exists_on_github = False
                
                try:
                    get_response = requests.get(api_url, headers=headers, timeout=10)
                    
                    if get_response.status_code == 200:
                        remote_file = get_response.json()
                        sha = remote_file.get("sha")
                        file_exists_on_github = True
                        
                        # Comparer les contenus
                        try:
                            remote_content_b64 = remote_file.get("content", "").replace('\n', '')
                            if remote_content_b64 == content_b64:
                                print(f"📋 {file_path} - Déjà à jour")
                                files_skipped += 1
                                continue
                        except:
                            pass  # En cas d'erreur de comparaison, on procède à la mise à jour
                            
                    elif get_response.status_code == 404:
                        file_exists_on_github = False
                    else:
                        print(f"❌ Erreur lors de la vérification de {file_path}: {get_response.status_code}")
                        continue
                        
                except requests.exceptions.RequestException as e:
                    print(f"❌ Erreur réseau pour la vérification de {file_path}: {str(e)}")
                    continue

                # Préparer les données pour la mise à jour
                data = {
                    "message": f"Auto-sync {file_path} - {timestamp}",
                    "content": content_b64,
                    "branch": github_branch
                }

                if sha:
                    data["sha"] = sha

                # Envoyer la mise à jour
                try:
                    put_response = requests.put(api_url, headers=headers, json=data, timeout=20)

                    if put_response.status_code in [200, 201]:
                        if file_exists_on_github:
                            print(f"✅ {file_path} - Mis à jour")
                            files_updated += 1
                        else:
                            print(f"🆕 {file_path} - Créé")
                            files_created += 1
                    else:
                        error_data = put_response.json() if put_response.content else {}
                        error_msg = error_data.get('message', f'HTTP {put_response.status_code}')
                        print(f"❌ {file_path} - Échec: {error_msg}")

                except requests.exceptions.RequestException as e:
                    print(f"❌ Erreur lors de l'envoi de {file_path}: {str(e)}")

            except Exception as e:
                print(f"❌ Erreur lors du traitement de {file_path}: {str(e)}")

        print(f"\n📊 Résumé de synchronisation:")
        print(f"   • Fichiers mis à jour: {files_updated}")
        print(f"   • Fichiers créés: {files_created}")
        print(f"   • Fichiers inchangés: {files_skipped}")
        print(f"   • Total traité: {files_updated + files_created + files_skipped}/{len(files_to_sync)}")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"⚠️ Erreur de synchronisation: {str(e)}")
        return False

def verify_sync_status():
    """Afficher le statut de synchronisation dans la console"""
    github_repo = os.getenv('GITHUB_REPO')
    github_branch = os.getenv('GITHUB_BRANCH', 'main')
    github_token = os.getenv('GITHUB_TOKEN')

    print("=" * 60)
    print("🔍 VÉRIFICATION DE CONFIGURATION")
    print("=" * 60)
    print(f"Repository: {github_repo if github_repo else '❌ Non configuré'}")
    print(f"Branche: {github_branch}")
    print(f"Token GitHub: {'✅ Configuré' if github_token else '❌ Non configuré'}")
    print("Fichiers surveillés:")
    print("  • Home Page (HTML, CSS, JS)")
    print("  • Values Page (HTML, CSS, JS)")
    print("  • Backend (app.py, github_sync.py)")
    print("  • Configuration (.replit, requirements.txt)")
    
    if github_repo and github_token:
        print("Status: ✅ Configuration complète")
    else:
        print("Status: ❌ Configuration incomplète")
        print("\nVeuillez configurer dans .env:")
        print("GITHUB_TOKEN=votre_token_github")
        print("GITHUB_REPO=utilisateur/nom-du-repo")
        print("GITHUB_BRANCH=main")
    
    print("=" * 60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "pull":
            print("🔄 Mode: Extraction depuis GitHub")
            pull_from_github()
        elif command == "push":
            print("🔄 Mode: Synchronisation vers GitHub")
            sync_with_github()
        elif command == "status":
            verify_sync_status()
        else:
            print("Usage:")
            print("  python github_sync.py pull   - Extraire depuis GitHub")
            print("  python github_sync.py push   - Synchroniser vers GitHub")
            print("  python github_sync.py status - Vérifier la configuration")
    else:
        # Mode par défaut: synchronisation vers GitHub
        print("🔄 Mode par défaut: Synchronisation vers GitHub")
        sync_with_github()
