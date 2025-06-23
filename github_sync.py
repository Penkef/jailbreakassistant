
import os
from datetime import datetime
import json
import base64
from dotenv import load_dotenv
import requests
import hashlib
import shutil

# Charger les variables d'environnement
load_dotenv()

def get_file_hash(file_path):
    """Calculer le hash SHA-256 d'un fichier"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def get_all_local_files():
    """Obtenir tous les fichiers locaux à synchroniser (exclut les fichiers temporaires et caches)"""
    excluded_patterns = [
        '__pycache__',
        '.git',
        'node_modules',
        '.env',
        'access.log',
        'backup_*',
        '.DS_Store',
        '*.pyc',
        '*.pyo',
        '*.tmp',
        'attached_assets'
    ]

    all_files = []

    for root, dirs, files in os.walk('.'):
        # Filtrer les dossiers à exclure
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in excluded_patterns)]

        for file in files:
            file_path = os.path.join(root, file)[2:]  # Retirer le './' du début

            # Exclure les fichiers selon les patterns
            if not any(pattern.replace('*', '') in file_path for pattern in excluded_patterns):
                all_files.append(file_path)

    return sorted(all_files)

def get_all_github_files(repo, branch, headers):
    """Obtenir tous les fichiers du repository GitHub de manière récursive"""
    all_files = []

    def get_tree_recursive(tree_sha):
        """Récupérer l'arbre des fichiers de manière récursive"""
        tree_url = f"https://api.github.com/repos/{repo}/git/trees/{tree_sha}?recursive=1"

        try:
            response = requests.get(tree_url, headers=headers, timeout=15)
            if response.status_code == 200:
                tree_data = response.json()
                for item in tree_data.get('tree', []):
                    if item['type'] == 'blob':  # C'est un fichier
                        all_files.append(item['path'])
        except Exception as e:
            print(f"Erreur lors de la récupération de l'arbre: {e}")

    try:
        # Obtenir le SHA du commit le plus récent
        commits_url = f"https://api.github.com/repos/{repo}/commits/{branch}"
        response = requests.get(commits_url, headers=headers, timeout=10)

        if response.status_code == 200:
            commit_data = response.json()
            tree_sha = commit_data['commit']['tree']['sha']
            get_tree_recursive(tree_sha)
        else:
            print(f"Erreur lors de la récupération des commits: {response.status_code}")

    except Exception as e:
        print(f"Erreur lors de la récupération des fichiers GitHub: {e}")

    return sorted(all_files)

def backup_local_files():
    """Créer une sauvegarde des fichiers locaux avant extraction"""
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Utiliser tous les fichiers locaux pour la sauvegarde
    files_to_backup = get_all_local_files()

    backup_created = False

    for file_path in files_to_backup:
        if os.path.exists(file_path):
            if not backup_created:
                os.makedirs(backup_dir, exist_ok=True)
                backup_created = True

            # Créer les dossiers de sauvegarde si nécessaire
            backup_file_path = os.path.join(backup_dir, file_path)
            os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)

            # Copier le fichier
            shutil.copy2(file_path, backup_file_path)

    if backup_created:
        print(f"💾 Sauvegarde créée dans: {backup_dir}")
        return backup_dir
    else:
        print("ℹ️ Aucun fichier local à sauvegarder")
        return None

def compare_files(local_path, github_content_b64):
    """Comparer un fichier local avec le contenu GitHub"""
    if not os.path.exists(local_path):
        return "local_missing"

    try:
        with open(local_path, 'rb') as f:
            local_content = f.read()
            local_b64 = base64.b64encode(local_content).decode()

        github_content_clean = github_content_b64.replace('\n', '')

        if local_b64 == github_content_clean:
            return "identical"
        else:
            return "different"
    except:
        return "error"

def pull_from_github(force=False):
    """Extraire les fichiers depuis GitHub avec comparaison intelligente"""
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

        # Créer une sauvegarde avant extraction
        backup_dir = backup_local_files() if not force else None

        # Obtenir tous les fichiers du repository GitHub
        files_to_pull = get_all_github_files(github_repo, github_branch, headers)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        files_downloaded = 0
        files_created = 0
        files_skipped = 0
        conflicts = []

        print(f"⬇️ Début d'extraction depuis GitHub - {timestamp}")
        print(f"Repository: {github_repo}")
        print(f"Branche: {github_branch}")
        if backup_dir:
            print(f"💾 Sauvegarde: {backup_dir}")
        print("-" * 50)

        for file_path in files_to_pull:
            try:
                api_url = f"https://api.github.com/repos/{github_repo}/contents/{file_path}"

                response = requests.get(api_url, headers=headers, timeout=15)

                if response.status_code == 200:
                    file_data = response.json()
                    content_b64 = file_data.get('content', '')

                    if content_b64:
                        try:
                            # Comparer avec le fichier local
                            comparison = compare_files(file_path, content_b64)

                            if comparison == "identical" and not force:
                                print(f"📋 {file_path} - Identique (ignoré)")
                                files_skipped += 1
                                continue
                            elif comparison == "different" and not force:
                                print(f"⚠️ {file_path} - CONFLIT DÉTECTÉ!")
                                print(f"   Local différent de GitHub. Utilisez --force pour écraser.")
                                conflicts.append(file_path)
                                continue

                            # Décoder et écrire le fichier
                            file_content = base64.b64decode(content_b64)

                            # Créer les dossiers si nécessaire
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)

                            file_exists = os.path.exists(file_path)

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
                    print(f"❌ {file_path} - Erreur {response.status_code}")

            except Exception as e:
                print(f"❌ Erreur pour {file_path}: {str(e)}")

        print(f"\n📊 Résumé d'extraction:")
        print(f"   • Fichiers mis à jour: {files_downloaded}")
        print(f"   • Fichiers créés: {files_created}")
        print(f"   • Fichiers ignorés: {files_skipped}")
        print(f"   • Conflits détectés: {len(conflicts)}")
        print(f"   • Total traité: {files_downloaded + files_created + files_skipped + len(conflicts)}/{len(files_to_pull)}")

        if conflicts:
            print(f"\n⚠️ Fichiers en conflit:")
            for conflict in conflicts:
                print(f"   • {conflict}")
            print(f"Utilisez: python github_sync.py pull --force pour écraser")

        if backup_dir:
            print(f"\n💾 Sauvegarde disponible dans: {backup_dir}")

        print("=" * 50)
        return True

    except Exception as e:
        print(f"⚠️ Erreur générale d'extraction: {str(e)}")
        return False

def sync_with_github():
    """Synchroniser les fichiers locaux vers GitHub (PUSH)"""
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

        # Test de connexion
        test_url = f"https://api.github.com/repos/{github_repo}"
        try:
            test_response = requests.get(test_url, headers=headers, timeout=10)
            if test_response.status_code == 404:
                print(f"❌ Repository '{github_repo}' non trouvé")
                return False
            elif test_response.status_code != 200:
                print(f"❌ Erreur d'accès: {test_response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Connexion GitHub impossible: {str(e)}")
            return False

        # Obtenir tous les fichiers locaux à synchroniser
        files_to_sync = get_all_local_files()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        files_updated = 0
        files_created = 0
        files_skipped = 0

        print(f"⬆️ Synchronisation vers GitHub - {timestamp}")
        print(f"Repository: {github_repo}")
        print(f"Branche: {github_branch}")
        print("-" * 50)

        for file_path in files_to_sync:
            if not os.path.exists(file_path):
                print(f"⚠️ Fichier non trouvé: {file_path}")
                continue

            try:
                with open(file_path, "rb") as f:
                    file_content = f.read()
                    content_b64 = base64.b64encode(file_content).decode()

                api_url = f"https://api.github.com/repos/{github_repo}/contents/{file_path}"

                # Vérifier le fichier existant sur GitHub
                sha = None
                file_exists = False

                try:
                    get_response = requests.get(api_url, headers=headers, timeout=10)

                    if get_response.status_code == 200:
                        remote_file = get_response.json()
                        sha = remote_file.get("sha")
                        file_exists = True

                        # Comparer les contenus
                        remote_content_b64 = remote_file.get("content", "").replace('\n', '')
                        if remote_content_b64 == content_b64:
                            print(f"📋 {file_path} - Déjà à jour")
                            files_skipped += 1
                            continue

                    elif get_response.status_code == 404:
                        file_exists = False

                except requests.exceptions.RequestException:
                    continue

                # Préparer et envoyer la mise à jour
                data = {
                    "message": f"Auto-sync {file_path} - {timestamp}",
                    "content": content_b64,
                    "branch": github_branch
                }

                if sha:
                    data["sha"] = sha

                try:
                    put_response = requests.put(api_url, headers=headers, json=data, timeout=20)

                    if put_response.status_code in [200, 201]:
                        if file_exists:
                            print(f"✅ {file_path} - Mis à jour")
                            files_updated += 1
                        else:
                            print(f"🆕 {file_path} - Créé")
                            files_created += 1
                    else:
                        print(f"❌ {file_path} - Échec: {put_response.status_code}")

                except requests.exceptions.RequestException as e:
                    print(f"❌ Erreur envoi {file_path}: {str(e)}")

            except Exception as e:
                print(f"❌ Erreur traitement {file_path}: {str(e)}")

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
    """Afficher le statut de configuration"""
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
    print("  • Tous les fichiers du projet (détection automatique)")
    print("  • Exclusions: __pycache__, .git, node_modules, .env, logs, backups")

    # Afficher quelques exemples de fichiers détectés
    local_files = get_all_local_files()
    if local_files:
        print(f"  • {len(local_files)} fichiers détectés localement")
        print("  • Exemples:", ", ".join(local_files[:5]) + ("..." if len(local_files) > 5 else ""))

    if github_repo and github_token:
        print("Status: ✅ Configuration complète")
    else:
        print("Status: ❌ Configuration incomplète")

    print("=" * 60)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "pull":
            force = "--force" in sys.argv
            if force:
                print("🔄 Mode: Extraction FORCÉE depuis GitHub")
            else:
                print("🔄 Mode: Extraction SÉCURISÉE depuis GitHub")
            pull_from_github(force=force)
        elif command == "push":
            print("🔄 Mode: Synchronisation vers GitHub")
            sync_with_github()
        elif command == "status":
            verify_sync_status()
        else:
            print("Usage:")
            print("  python github_sync.py pull         - Extraction sécurisée")
            print("  python github_sync.py pull --force - Extraction forcée")
            print("  python github_sync.py push         - Synchroniser vers GitHub")
            print("  python github_sync.py status       - Vérifier la configuration")
    else:
        print("🔄 Mode par défaut: Synchronisation vers GitHub")
        sync_with_github()
