import os
import importlib.util
from flask import Flask, render_template, send_from_directory
import requests
import inspect
import yaml
import logging
from cachetools import TTLCache
from packaging.version import parse


app = Flask(__name__)

cache = TTLCache(maxsize=100, ttl=3600)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    with open("config.yml", "r") as file:
        return yaml.safe_load(file)

def fetch_latest_versions(tools):
    versions = {}
    for tool, data in tools.items():
        if tool in cache:
            versions[tool] = cache[tool]
            continue

        try:
            response = requests.get(data['url'], timeout=5)
            response.raise_for_status()
            data_json = response.json()

            if isinstance(data_json, list):  # Cas GitLab
                latest_version = data_json[0].get("tag_name", "Unknown")
            elif isinstance(data_json, dict):  # Cas GitHub
                latest_version = data_json.get("tag_name", "Unknown")
            else:
                latest_version = "Unsupported API format"

            versions[tool] = latest_version
            cache[tool] = latest_version  # Mise en cache de la version
        except requests.RequestException as e:
            logging.error(f"Erreur lors de la récupération de {tool}: {e}")
            versions[tool] = "Erreur: Impossible de récupérer la version"
    return versions

def load_plugin(plugin_name):
    plugin_path = os.path.join(app.root_path, "plugins", f"{plugin_name}.py")
    if not os.path.exists(plugin_path):
        logging.error(f"Plugin introuvable: {plugin_name}")
        return None

    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def compare_versions(current_version, latest_version):
    current_version_clean = current_version.split('-')[0]
    latest_version_clean = latest_version.split('-')[0]

    current_version_parsed = parse(current_version_clean)
    latest_version_parsed = parse(latest_version_clean)

    if current_version_parsed > latest_version_parsed:
        return True
    elif current_version_parsed < latest_version_parsed:
        return False
    else:
        return True

def fetch_versions(tools):
    versions = {}
    for tool, data in tools.items():
        plugin = load_plugin(data["type"])

        if plugin and hasattr(plugin, "get_versions"):
            try:
                headers = data.get("headers", {})
                token = data.get("token", None)
                # current_version, latest_version = plugin.get_versions(data["endpoint"], headers, token)
                signature = inspect.signature(plugin.get_versions)
                if "token" in signature.parameters:
                    current_version, latest_version = plugin.get_versions(data["endpoint"], headers, token)
                else:
                    current_version, latest_version = plugin.get_versions(data["endpoint"], headers)

                uptodate = compare_versions(current_version, latest_version)

                status = "À jour" if uptodate else "Mise à jour disponible"
                # uptodate = True if current_version == latest_version else False
            except Exception as e:
                logging.error(f"Erreur dans {tool}: {e}")
                current_version, latest_version, status, uptodate = "Erreur", "Erreur", "Inconnu", False
        else:
            current_version, latest_version, status, uptodate = "Plugin non valide", "Plugin non valide", "Inconnu", False

        versions[data["name"]] = {
            "endpoint": data["endpoint"],
            "current": current_version,
            "latest": latest_version,
            "status": status,
            "uptodate": uptodate
        }

    return versions


@app.route('/')
def index():
    config = load_config()
    tools = config.get("tools", {})
    versions = fetch_versions(tools)
    return render_template("index.html", versions=versions)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
