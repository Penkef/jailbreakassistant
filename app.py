
#!/usr/bin/env python3
"""
Jailbreak Assistant - Backend Python avec serveur Flask
"""
import os
from datetime import datetime
from flask import Flask, send_from_directory, redirect, request
from github_sync import sync_with_github, verify_sync_status

app = Flask(__name__)

def log_access():
    """Log website access"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("access.log","a") as f:
        f.write(f"Site accessed at: {timestamp}\n")

def get_site_info():
    """Get basic site information"""
    return {
        "name": "Jailbreak Assistant",
        "url": "www.jailbreakassistant.xyz",
        "status": "Coming Soon",
        "version": "1.0.0"
    }

@app.before_request
def force_https():
    """Force HTTPS in production"""
    if not request.is_secure and request.headers.get('X-Forwarded-Proto') != 'https':
        if 'replit.dev' in request.host or 'jailbreakassistant.xyz' in request.host:
            return redirect(request.url.replace('http://', 'https://'), code=301)

@app.after_request
def after_request(response):
    """Add security headers"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/')
def home():
    """Redirect to home_page"""
    log_access()
    return redirect('/home')

@app.route('/home')
def home_page():
    """Serve home_page"""
    log_access()
    return send_from_directory('home_page', 'home.html')

@app.route('/values')
def values_page():
    """Serve value_page"""
    log_access()
    return send_from_directory('value_page', 'values.html')

# Routes pour servir les fichiers statiques spécifiques
@app.route('/home_page/<path:filename>')
def serve_home_files(filename):
    """Serve home_page static files"""
    return send_from_directory('home_page', filename)

@app.route('/pictures/<path:filename>')
def serve_pictures(filename):
    """Serve pictures"""
    return send_from_directory('pictures', filename)

@app.route('/<path:filename>')
def serve_files(filename):
    """Serve static files and redirect old URLs"""
    try:
        # Rediriger les accès directs vers les URLs propres
        if filename == 'home_page/home.html':
            return redirect('/home', code=301)
        elif filename == 'value_page/values.html':
            return redirect('/values', code=301)
        elif filename.startswith('home_page'):
            return redirect('/home', code=301)
        elif filename.startswith('values_page/'):
            return redirect('/values', code=301)
        else:
            return send_from_directory('.', filename)
    except:
        return redirect('/home')

if __name__ == "__main__":
    # Synchronisation automatique à chaque lancement
    print("🔄 Synchronisation automatique avec GitHub...")
    sync_with_github()
    print()
    
    # Lancement du serveur web
    info = get_site_info()
    print(f"=== {info['name']} ===")
    print(f"URL: {info['url']}")
    print(f"Status: {info['status']}")
    print(f"Version: {info['version']}")
    print("\nSynchronisation automatique activée ✅")
    print("🌐 Serveur web démarré sur http://0.0.0.0:5000")
    print()
    verify_sync_status()
    
    # Démarrer le serveur Flask
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True, use_reloader=False)
