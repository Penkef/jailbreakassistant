
#!/usr/bin/env python3
"""
Jailbreak Assistant - Backend Python
"""

import os
from datetime import datetime
from github_sync import sync_with_github, verify_sync_status

def log_access():
    """Log website access"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("access.log", "a") as f:
        f.write(f"Site accessed at: {timestamp}\n")

def get_site_info():
    """Get basic site information"""
    return {
        "name": "Jailbreak Assistant",
        "url": "www.jailbreakassistant.xyz",
        "status": "Coming Soon",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--sync":
        sync_with_github()
    else:
        log_access()
        info = get_site_info()
        print(f"=== {info['name']} ===")
        print(f"URL: {info['url']}")
        print(f"Status: {info['status']}")
        print(f"Version: {info['version']}")
        print("\nPour synchroniser avec GitHub: python app.py --sync")
        print()
        verify_sync_status()