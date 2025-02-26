import os
import importlib
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


# def fetch_latest_versions(tools):
#     versions = {}
#     for tool, data in tools.items():
#         if tool in cache:
#             versions[tool] = cache[tool]
#             continue
#
#         try:
#             response = requests.get(data['url'], timeout=5)
#             response.raise_for_status()
#             data_json = response.json()
#
#             if isinstance(data_json, list):  # Cas GitLab
#                 latest_version = data_json[0].get("tag_name", "Unknown")
#             elif isinstance(data_json, dict):  # Cas GitHub
#                 latest_version = data_json.get("tag_name", "Unknown")
#             else:
#                 latest_version = "Unsupported API format"
#
#             versions[tool] = latest_version
#             cache[tool] = latest_version  # Mise en cache de la version
#         except requests.RequestException as e:
#             logging.error(f"Erreur lors de la récupération de {tool}: {e}")
#             versions[tool] = "Erreur: Impossible de récupérer la version"
#     return versions

def load_plugin(plugin_name, endpoint, headers):
    try:
        module = importlib.import_module(f"plugins.{plugin_name}")
        plugin_class = getattr(module, f"{plugin_name.capitalize()}Plugin")
        return plugin_class(endpoint, headers)
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Erreur lors du chargement du plugin {plugin_name}: {e}")
        return None


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
        endpoint = data["endpoint"]
        headers = data.get("headers", {})

        plugin = load_plugin(data["type"], endpoint, headers)

        try:
            current_version, latest_version = plugin.get_versions()
            uptodate = compare_versions(current_version, latest_version)

            status = "À jour" if uptodate else "Mise à jour disponible"
        except Exception as e:
            logging.error(f"Erreur dans {tool}: {e}")
            current_version, latest_version, status, uptodate = "Erreur", "Erreur", "Inconnu", False

        versions[data["name"]] = {
            "endpoint": endpoint,
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
