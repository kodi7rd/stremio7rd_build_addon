from flask import Flask, jsonify, redirect

app = Flask(__name__)

# Constants
LATEST_VERSION = "1.0.0"
STREMIO7RD_URL = "https://i.imgur.com/CRpsxpE.jpeg"
RED_THUMBS_UP_URL = "https://i.imgur.com/HwcDn4G.png"
GREEN_THUMBS_UP_URL = "https://i.imgur.com/dJ1E3aj.png"
NEW_UPDATE_URL = "https://i.imgur.com/RZcmX2e.png"

# Define a base manifest template
def generate_manifest(version):
    return {
        "id": "org.stremio7rd.com",
        "version": version,
        "name": f"Stremio + Real Debrid Israel Build",
        "description": f"Stremio + Real Debrid Israel Build Version.",
        "resources": ["catalog"],
        "types": ["movie"],
        "icon": STREMIO7RD_URL,
        "catalogs": [
            {
                "type": "movie",
                "id": "info_catalog",
                "name": f"Stremio + Real Debrid Israel Build"
            }
        ],
    }

@app.route("/manifest.json")
@app.route("/<current_version>/manifest.json")
def manifest(current_version=None):
    """Return the manifest with dynamic version based on URL parameter or redirect to latest version."""
    if current_version is None:  # No version in the URL, redirect to latest version
        current_version = LATEST_VERSION
        return redirect(f"/{current_version}/manifest.json")

    # Generate the manifest for the specific version
    manifest_data = generate_manifest(current_version)
    return respond_with(manifest_data)

@app.route("/<current_version>/catalog/movie/info_catalog.json")
@app.route("/catalog/movie/info_catalog.json")
def catalog(current_version=None):
    """Return the catalog with text fetched from an external URL."""
    print("[DEBUG] /catalog/movie/info_catalog.json endpoint was called.")
    
    if current_version is None:
        current_version = LATEST_VERSION
        
    # Set the poster based on whether versions are equal or not
    current_version_poster = GREEN_THUMBS_UP_URL if current_version == LATEST_VERSION else RED_THUMBS_UP_URL
    
    catalog_entry = [
        {
            "id": "latest_version",
            "name": f"גרסה אחרונה: {LATEST_VERSION}",
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
    
    if current_version != LATEST_VERSION:
        catalog_entry.append({
            "id": "update_addon",
            "name": "!יש לעדכן את הבילד",
            "type": "movie",
            "poster": NEW_UPDATE_URL
        })
        
    return respond_with({"metas": catalog_entry})

def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

if __name__ == "__main__":
    print("[DEBUG] Starting the Flask application on http://0.0.0.0:7000")
    app.run(host="0.0.0.0", port=5000, debug=True)
