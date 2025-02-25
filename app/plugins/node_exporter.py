import re
import requests
from plugins.abstract import normalize_version, fetch_version

NODE_EXPORTER_LATEST_URL = "https://api.github.com/repos/prometheus/node_exporter/releases/latest"

NODE_EXPORTER_API_ENDPOINT = "/metrics"

def get_versions(endpoint, headers={}):
    try:
        response = requests.get(endpoint + NODE_EXPORTER_API_ENDPOINT, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Erreur: Impossible de récupérer les métriques ({e})", "Erreur"

    if response.text:
        version_match = re.search(r'node_exporter_build_info.*?,version="([^"]+)"', response.text)
        if version_match:
            current_version = normalize_version(version_match.group(1))
        else:
            current_version = "Erreur: Version non trouvée"
    else:
        current_version = "Erreur: Impossible de récupérer les métriques"

    data = fetch_version(NODE_EXPORTER_LATEST_URL)
    if data and isinstance(data, dict):
        latest_version = normalize_version(data.get("tag_name", "Inconnu"))
    else:
        latest_version = "Erreur"

    return current_version, latest_version
