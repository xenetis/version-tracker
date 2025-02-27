import requests
from .abstract import AbstractPlugin, latest_version_cache

class PrometheusPlugin(AbstractPlugin):
    def __init__(self, endpoint, headers):
        super().__init__(endpoint=endpoint, headers=headers)

    PROMETHEUS_LATEST_URL = "https://api.github.com/repos/prometheus/prometheus/releases/latest"
    PROMETHEUS_API_ENDPOINT = "/api/v1/status/buildinfo"

    def get_current_version(self):
        try:
            data = self.fetch_version(self.endpoint + self.PROMETHEUS_API_ENDPOINT, self.headers)
            return self.normalize_version(data.get("data", {}).get("version", "Inconnu")) if data else "Erreur"
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer la version installée ({e})"

    def get_latest_version(self):
        if "prometheus" in latest_version_cache:
            return latest_version_cache["prometheus"]
        try:
            data = self.fetch_version(self.PROMETHEUS_LATEST_URL)
            latest_version = self.normalize_version(data.get("tag_name", "Inconnu")) if data else "Erreur"
            if latest_version not in ["Inconnu", "Erreur"]: latest_version_cache["prometheus"] = latest_version
            return latest_version
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer la dernière version ({e})"
