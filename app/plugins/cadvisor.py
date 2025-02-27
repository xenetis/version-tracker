import re
import requests
from .abstract import AbstractPlugin, latest_version_cache

class CadvisorPlugin(AbstractPlugin):
    def __init__(self, endpoint, headers, **kwargs):
        super().__init__(endpoint=endpoint, headers=headers)

    NODE_EXPORTER_LATEST_URL = "https://api.github.com/repos/google/cadvisor/releases/latest"
    NODE_EXPORTER_API_ENDPOINT = "/metrics"

    def get_current_version(self):
        try:
            response = requests.get(self.endpoint + self.NODE_EXPORTER_API_ENDPOINT, headers=self.headers, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer les métriques ({e})", "Erreur"

        if response.text:
            version_match = re.search(r'cadvisor_version_info.*?,cadvisorVersion="([^"]+)"', response.text)
            if version_match:
                current_version = self.normalize_version(version_match.group(1))
            else:
                current_version = "Erreur: Version non trouvée"
        else:
            current_version = "Erreur: Impossible de récupérer les métriques"
        return current_version

    def get_latest_version(self):
        if "cadvisor" in latest_version_cache:
            return latest_version_cache["cadvisor"]
        try:
            data = self.fetch_version(self.NODE_EXPORTER_LATEST_URL)
            if data and isinstance(data, dict):
                latest_version = self.normalize_version(data.get("tag_name", "Inconnu"))
            else:
                latest_version = "Erreur"
            if latest_version not in ["Inconnu", "Erreur"]: latest_version_cache["cadvisor"] = latest_version
            return latest_version
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer les métriques ({e})", "Erreur"
