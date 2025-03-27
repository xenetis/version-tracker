import os
import importlib
from flask import Flask, request, make_response, render_template, send_from_directory
import yaml
import logging
from cachetools import TTLCache
from packaging.version import parse

from locales.translator import Translator

app = Flask(__name__)

cache = TTLCache(maxsize=100, ttl=3600)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_config():
    with open("config.yml", "r") as file:
        return yaml.safe_load(file)


def load_plugin(plugin_name, endpoint, headers, translations):
    try:
        module = importlib.import_module(f"plugins.{plugin_name}")
        plugin_class = getattr(module, f"{plugin_name.capitalize()}Plugin")
        return plugin_class(endpoint, headers, translations)
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error loading plugin {plugin_name}: {e}")
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


def fetch_versions(tools, translations):
    versions = {}
    for tool, data in tools.items():
        endpoint = data["endpoint"]
        headers = data.get("headers", {})

        plugin = load_plugin(data["type"], endpoint, headers, translations)

        try:
            # current_version, latest_version = plugin.get_versions()
            current_version = plugin.get_current_version()
            latest_version = plugin.get_latest_version()
            uptodate = compare_versions(current_version, latest_version)

            status = translations.get("uptodate") if uptodate else translations.get("update_available")
        except Exception as e:
            logging.error(f"Error in {tool}: {e}")
            status = translations.get("unknown")
            uptodate = False
            # current_version, latest_version, status, uptodate = translations.get("error"), translations.get("error"), translations.get("unknown"), False

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

    translator = Translator()
    lang = translator.detect_language()
    translations = translator.load_translations()

    versions = fetch_versions(tools, translations)

    response = make_response(render_template("index.html", versions=versions, translations=translations, lang=lang))

    if request.args.get("lang"):
        response.set_cookie("lang", request.args.get("lang"), max_age=30*24*60*60)

    return response


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
