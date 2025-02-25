from plugins.abstract import normalize_version, fetch_version

GITLAB_LATEST_URL = "https://gitlab.com/api/v4/projects/13083/repository/tags"

GITLAB_API_ENDPOINT = "/api/v4/version"

def get_versions(endpoint, headers={}):
    data = fetch_version(endpoint + GITLAB_API_ENDPOINT, headers)
    current_version = normalize_version(data.get("version", "Inconnu")) if data else "Erreur"

    data = fetch_version(GITLAB_LATEST_URL)
    latest_version = normalize_version(data[0].get("name", "Inconnu")) if data else "Erreur"

    return current_version, latest_version
