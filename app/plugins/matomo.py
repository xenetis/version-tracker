import requests
from plugins.abstract import normalize_version

MATOMO_LATEST_URL = "https://api.matomo.org/1.0/getLatestVersion/"

MATOMO_API_ENDPOINT = "/index.php?module=API&method=API.getMatomoVersion&format=json"
# MATOMO_API_ENDPOINT = "/index.php"

def get_versions(endpoint, headers={}, token=None):
    auth_param = f"&token_auth={token}" if token else ""

    try:
        response = requests.get(endpoint + MATOMO_API_ENDPOINT + auth_param, headers=headers, timeout=5)
        response.raise_for_status()
        current_version = normalize_version(response.json().get("value", "Pas de value"))
    except requests.RequestException as e:
        current_version = f"Erreur: Impossible de récupérer la version installée ({e})"

    try:
        response = requests.get(MATOMO_LATEST_URL, timeout=5)
        response.raise_for_status()
        latest_version = normalize_version(response.text.strip())
    except requests.RequestException as e:
        latest_version = f"Erreur: Impossible de récupérer la dernière version ({e})"

    return current_version, latest_version