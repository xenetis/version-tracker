from plugins.abstract import normalize_version, fetch_version

PROMETHEUS_LATEST_URL = "https://api.github.com/repos/prometheus/prometheus/releases/latest"
PROMETHEUS_API_ENDPOINT = "/api/v1/status/buildinfo"

def get_versions(endpoint, headers={}):

    data = fetch_version(endpoint + PROMETHEUS_API_ENDPOINT, headers)
    current_version = normalize_version(data.get("data", {}).get("version", "Inconnu")) if data else "Erreur"

    data = fetch_version(PROMETHEUS_LATEST_URL)
    latest_version = normalize_version(data.get("tag_name", "Inconnu")) if data else "Erreur"

    return current_version, latest_version