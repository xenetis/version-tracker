from plugins.abstract import normalize_version, fetch_version

GRAFANA_LATEST_URL = "https://api.github.com/repos/grafana/grafana/releases/latest"

GRAFANA_API_ENDPOINT = "/api/health"

def get_versions(endpoint, headers={}):
    data = fetch_version(endpoint + GRAFANA_API_ENDPOINT, headers)
    current_version = normalize_version(data.get("version", "Inconnu")) if data else "Erreur"

    data = fetch_version(GRAFANA_LATEST_URL)
    latest_version = normalize_version(data.get("tag_name", "Inconnu")) if data else "Erreur"

    return current_version, latest_version