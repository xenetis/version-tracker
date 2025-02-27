import re
import requests
from .abstract import AbstractPlugin, latest_version_cache

class Node_exporterPlugin(AbstractPlugin):
    def __init__(self, endpoint, headers):
        super().__init__(endpoint=endpoint, headers=headers)

    NODE_EXPORTER_LATEST_URL = "https://api.github.com/repos/prometheus/node_exporter/releases/latest"
    NODE_EXPORTER_API_ENDPOINT = "/metrics"

    def get_current_version(self):
        try:
            response = requests.get(self.endpoint + self.NODE_EXPORTER_API_ENDPOINT, headers=self.headers, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer les métriques ({e})", "Erreur"

        if response.text:
            version_match = re.search(r'node_exporter_build_info.*?,version="([^"]+)"', response.text)
            if version_match:
                return self.normalize_version(version_match.group(1))
            else:
                return "Erreur: Version non trouvée"
        else:
            return "Erreur: Impossible de récupérer les métriques"

    def get_latest_version(self):
        if "node_exporter" in latest_version_cache:
            return latest_version_cache["node_exporter"]
        try:
            data = self.fetch_version(self.NODE_EXPORTER_LATEST_URL)
            latest_version = self.normalize_version(data.get("tag_name", "Inconnu")) if data else "Erreur"
            if latest_version not in ["Inconnu", "Erreur"]: latest_version_cache["node_exporter"] = latest_version
            return latest_version
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer les métriques ({e})", "Erreur"
