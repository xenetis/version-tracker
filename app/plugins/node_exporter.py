import re
import requests
import requests
from .abstract import AbstractPlugin

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
        data = self.fetch_version(self.NODE_EXPORTER_LATEST_URL)
        if data and isinstance(data, dict):
            return self.normalize_version(data.get("tag_name", "Inconnu"))
        else:
            return "Erreur"

    # def get_versions(endpoint, headers={}):
    #     try:
    #         response = requests.get(endpoint + NODE_EXPORTER_API_ENDPOINT, headers=headers, timeout=5)
    #         response.raise_for_status()
    #     except requests.RequestException as e:
    #         return f"Erreur: Impossible de récupérer les métriques ({e})", "Erreur"
    #
    #     if response.text:
    #         version_match = re.search(r'node_exporter_build_info.*?,version="([^"]+)"', response.text)
    #         if version_match:
    #             current_version = normalize_version(version_match.group(1))
    #         else:
    #             current_version = "Erreur: Version non trouvée"
    #     else:
    #         current_version = "Erreur: Impossible de récupérer les métriques"
    #
    #     data = fetch_version(NODE_EXPORTER_LATEST_URL)
    #     if data and isinstance(data, dict):
    #         latest_version = normalize_version(data.get("tag_name", "Inconnu"))
    #     else:
    #         latest_version = "Erreur"
    #
    #     return current_version, latest_version
