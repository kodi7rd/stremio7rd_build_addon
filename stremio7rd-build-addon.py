from flask import Flask, jsonify, redirect

app = Flask(__name__)

################################################################
# Constants
LATEST_VERSION = "1.0.1"
STREMIO7RD_URL = "https://i.imgur.com/CRpsxpE.jpeg"
RED_THUMBS_DOWN_URL = "https://i.imgur.com/gY4MWuf.png"
GREEN_THUMBS_UP_URL = "https://i.imgur.com/ntwsGcb.png"
NEW_UPDATE_URL = "https://i.imgur.com/RZcmX2e.png"
BUILD_QR_URL = "https://i.imgur.com/wbnhJUp.png"
################################################################

# Define a base manifest template
def generate_manifest(version):
    return {
        "id": "org.stremio7rd.com",
        "version": version,
        "name": f"Stremio + Real Debrid Israel Build",
        "description": f"Stremio + Real Debrid Israel Build Version Check.",
        "resources": ["catalog"],
        "types": ["other"],
        "logo": STREMIO7RD_URL,
        "catalogs": [
            {
                "type": "other",
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

@app.route("/<current_version>/catalog/other/info_catalog.json")
@app.route("/catalog/other/info_catalog.json")
def catalog(current_version=None):
    """Return the catalog with text fetched from an external URL."""
    print("[DEBUG] /catalog/other/info_catalog.json endpoint was called.")
    
    if current_version is None:
        current_version = LATEST_VERSION
        
    # Set the poster based on whether versions are equal or not
    current_version_poster = GREEN_THUMBS_UP_URL if current_version == LATEST_VERSION else RED_THUMBS_DOWN_URL
    
    catalog_entry = [
        {
            "id": "latest_version",
            "name": f"גרסה אחרונה: {LATEST_VERSION}",
            "type": "other",
            "poster": STREMIO7RD_URL,
            "posterShape": "square"
        },
        {
            "id": "current_version",
            "name": f"גרסה נוכחית: {current_version}",
            "type": "other",
            "poster": current_version_poster,
            "posterShape": "square"
        }
    ]
    
    if current_version != LATEST_VERSION:
        catalog_entry.extend([
        {
            "id": "build_qr",
            "name": "סרוק להתקנה",
            "type": "other",
            "poster": BUILD_QR_URL,
            "posterShape": "square"
        },
        {
            "id": "update_addon",
            "name": "!יש לעדכן את הבילד",
            "type": "other",
            "poster": NEW_UPDATE_URL,
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
