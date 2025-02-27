import requests
from .abstract import AbstractPlugin, latest_version_cache

class Gitlab_cePlugin(AbstractPlugin):
    def __init__(self, endpoint, headers, **kwargs):
        super().__init__(endpoint=endpoint, headers=headers)

    GITLAB_LATEST_URL = "https://gitlab.com/api/v4/projects/13083/repository/tags"
    GITLAB_API_ENDPOINT = "/api/v4/version"

    def get_current_version(self):
        try:
            data = self.fetch_version(self.endpoint + self.GITLAB_API_ENDPOINT, self.headers)
            return self.normalize_version(data.get("version", "Inconnu")) if data else "Erreur"
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer les métriques ({e})", "Erreur"

    def get_latest_version(self):
        if "gitlab_ce" in latest_version_cache:
            return latest_version_cache["gitlab_ce"]
        try:
            data = self.fetch_version(self.GITLAB_LATEST_URL)
            latest_version = self.normalize_version(data[0].get("name", "Inconnu")) if data else "Erreur"
            if latest_version not in ["Inconnu", "Erreur"]: latest_version_cache["gitlab_ce"] = latest_version
            return latest_version
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer les métriques ({e})", "Erreur"
