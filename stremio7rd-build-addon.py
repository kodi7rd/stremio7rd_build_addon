from flask import Flask, jsonify, redirect

app = Flask(__name__)

# Constants
LATEST_VERSION = "1.0.0"
STREMIO7RD_URL = "https://i.imgur.com/CRpsxpE.jpeg"
RED_THUMBS_UP_URL = "https://i.imgur.com/HwcDn4G.png"
GREEN_THUMBS_UP_URL = "https://i.imgur.com/aCNdSXk.png"
NEW_UPDATE_URL = "https://i.imgur.com/RZcmX2e.png"
BUILD_QR_URL = "https://i.imgur.com/wbnhJUp.png"

# Define a base manifest template
def generate_manifest(version):
    return {
        "id": "org.stremio7rd.com",
        "version": version,
        "name": f"Stremio + Real Debrid Israel Build",
        "description": f"Stremio + Real Debrid Israel Build Version Check.",
        "resources": ["catalog"],
        "types": ["movie"],
        "logo": STREMIO7RD_URL,
        "catalogs": [
            {
                "type": "movie",
                "id": "info_catalog",
                "name": "Stremio + Real Debrid Israel ברוכים הבאים לבילד של"
            }
        ],
    }

@app.route("/")
@app.route("/manifest.json")
def default_manifest():
    """Redirect root URL to default version manifest."""
    """If the manifest URL is accessed without a version, redirect to the versioned URL."""
    return redirect(f'/{LATEST_VERSION}/manifest.json')

@app.route("/<current_version>/manifest.json")
def manifest(current_version):
    """Return the manifest for a specific version."""
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
        catalog_entry.extend([
        {
            "id": "update_addon",
            "name": "!יש לעדכן את הבילד",
            "type": "movie",
            "poster": NEW_UPDATE_URL
        },
        {
            "id": "build_qr",
            "name": "סרוק להתקנה",
            "type": "movie",
            "poster": BUILD_QR_URL,
            "background": BUILD_QR_URL,
            "logo": BUILD_QR_URL,
            "posterShape": "square"
        }
    ])
        
    return respond_with({"metas": catalog_entry})

def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

if __name__ == "__main__":
    print("[DEBUG] Starting the Flask application on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
