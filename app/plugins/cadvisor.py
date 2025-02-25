import re
import requests
from plugins.abstract import normalize_version, fetch_version

NODE_EXPORTER_LATEST_URL = "https://api.github.com/repos/google/cadvisor/releases/latest"

NODE_EXPORTER_API_ENDPOINT = "/metrics"

def get_versions(endpoint, headers={}):
    try:
        response = requests.get(endpoint + NODE_EXPORTER_API_ENDPOINT, headers=headers, timeout=5)
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
    except requests.RequestException as e:
        return f"Erreur: Impossible de récupérer les métriques ({e})", "Erreur"

    if response.text:
        version_match = re.search(r'cadvisor_version_info.*?,cadvisorVersion="([^"]+)"', response.text)
        if version_match:
            current_version = normalize_version(version_match.group(1))
        else:
            current_version = "Erreur: Version non trouvée"
    else:
        current_version = "Erreur: Impossible de récupérer les métriques"

    data = fetch_version(NODE_EXPORTER_LATEST_URL)
    if data and isinstance(data, dict):
        latest_version = normalize_version(data.get("tag_name", "Inconnu"))  # Dernier tag de version
    else:
        latest_version = "Erreur"

    return current_version, latest_version
