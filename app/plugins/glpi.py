import requests
from .abstract import AbstractPlugin

class GlpiPlugin(AbstractPlugin):
    def __init__(self, endpoint, headers, **kwargs):
        super().__init__(endpoint=endpoint, headers=headers)

    GLPI_LATEST_URL = "https://api.github.com/repos/glpi-project/glpi/releases/latest"
    GLPI_API_INIT_ENDPOINT = "/apirest.php/initSession"
    GLPI_API_ENDPOINT = "/apirest.php/getGlpiConfig"

    def get_current_version(self):
        try:
            self.headers["Content-Type"] = "application/json"
            response = requests.get(self.endpoint + self.GLPI_API_INIT_ENDPOINT, headers=self.headers, timeout=5)
            response.raise_for_status()
            session_token = response.json().get("session_token")
            self.headers["Session-Token"] = session_token

            response = requests.get(self.endpoint + self.GLPI_API_ENDPOINT, headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json().get("cfg_glpi").get("version", None)
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer la version installée ({e})"

    def get_latest_version(self):
        try:
            response = requests.get(self.GLPI_LATEST_URL, timeout=5)
            response.raise_for_status()
            return self.normalize_version(response.json().get("tag_name", "Erreur: Clé 'tag_name' introuvable"))
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer la dernière version ({e})"
