import requests
from plugins.abstract import normalize_version

GLPI_LATEST_URL = "https://api.github.com/repos/glpi-project/glpi/releases/latest"
GLPI_API_INIT_ENDPOINT = "/apirest.php/initSession"
GLPI_API_ENDPOINT = "/apirest.php/getGlpiConfig"

def get_versions(endpoint, headers={}):
    try:
        headers["Content-Type"] = "application/json"
        response = requests.get(endpoint + GLPI_API_INIT_ENDPOINT, headers=headers, timeout=5)
        response.raise_for_status()
        session_token = response.json().get("session_token")
        headers["Session-Token"] = session_token

        response = requests.get(endpoint + GLPI_API_ENDPOINT, headers=headers, timeout=5)
        response.raise_for_status()
        current_version = response.json().get("cfg_glpi").get("version", None)
    except requests.RequestException as e:
        current_version = f"Erreur: Impossible de récupérer la version installée ({e})"

    try:
        response = requests.get(GLPI_LATEST_URL, timeout=5)
        response.raise_for_status()
        latest_version = normalize_version(response.json().get("tag_name", "Erreur: Clé 'tag_name' introuvable"))
    except requests.RequestException as e:
        latest_version = f"Erreur: Impossible de récupérer la dernière version ({e})"

    return current_version, latest_version
