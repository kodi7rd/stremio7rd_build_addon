from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Constants
LATEST_VERSION_URL = "https://kodi7rd.github.io/stremio7rd_build_addon/version.txt"
# Posters
STREMIO7RD_URL = "https://i.imgur.com/CRpsxpE.jpeg"
RED_THUMBS_UP_URL = "https://i.imgur.com/HwcDn4G.png"
GREEN_THUMBS_UP_URL = "https://i.imgur.com/dJ1E3aj.png"
NEW_UPDATE_URL = "https://i.imgur.com/RZcmX2e.png"

# Define the manifest object
MANIFEST = {
    "id": "org.stremio7rd.com",
    "version": "1.0.0",
    "name": "Stremio + Real Debrid Israel Build",
    "description": "Stremio + Real Debrid Israel Build Version Information.",
    "resources": ["catalog"],
    "types": ["movie"],
    "icon": STREMIO7RD_URL,
    "catalogs": [
        {
            "type": "movie",
            "id": "info_catalog",
            "name": "Stremio + Real Debrid Israel ברוכים הבאים לבילד של"
        }
    ],
}

def get_latest_version():
    """Reads the version from the version.txt file in the same directory."""
    try:
        with open("version.txt", "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"[ERROR] Failed to read version.txt: {e}")
        return "שגיאה"  # Default to 0.0.0 if file read fails

@app.route("/manifest.json")
def manifest():
    """Return the manifest."""
    print("[DEBUG] /manifest.json endpoint was called.")
    return respond_with(MANIFEST)

@app.route("/catalog/movie/info_catalog.json")
def catalog():
    """Return the catalog with text fetched from an external URL."""
    print("[DEBUG] /catalog/movie/info_catalog.json endpoint was called.")
    try:
        current_version = str(MANIFEST['version'])
        latest_version = get_latest_version()

        # Set the poster based on whether versions are equal or not
        current_version_poster = GREEN_THUMBS_UP_URL if current_version == latest_version else RED_THUMBS_UP_URL
        
        catalog_entry = [
            {
                "id": "latest_version",
                "name": f"גרסה אחרונה: {latest_version}",
                "type": "movie",
                "poster": STREMIO7RD_URL
            },
            {
                "id": "current_version",
                "name": f"גרסה נוכחית: {current_version}",
                "type": "movie",
                "poster": current_version_poster
            }
        ]
        
        if current_version != latest_version:
            catalog_entry.append({
                "id": "update_addon",
                "name": "!יש לעדכן את הבילד",
                "type": "movie",
                "poster": NEW_UPDATE_URL
            })
            
        return respond_with({"metas": catalog_entry})
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch external text: {e}")
        return respond_with({"metas": []})

def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

if __name__ == "__main__":
    print("[DEBUG] Starting the Flask application on http://0.0.0.0:7000")
    app.run(host="0.0.0.0", port=5000, debug=True)
