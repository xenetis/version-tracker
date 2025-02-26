import requests
from .abstract import AbstractPlugin

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
        try:
            data = self.fetch_version(self.PROMETHEUS_LATEST_URL)
            return self.normalize_version(data.get("tag_name", "Inconnu")) if data else "Erreur"
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer la dernière version ({e})"
