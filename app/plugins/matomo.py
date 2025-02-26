import requests
from .abstract import AbstractPlugin

class MatomoPlugin(AbstractPlugin):
    def __init__(self, endpoint, headers):
        super().__init__(endpoint=endpoint, headers=headers)

    MATOMO_LATEST_URL = "https://api.matomo.org/1.0/getLatestVersion/"
    MATOMO_API_ENDPOINT = "/index.php?module=API&method=API.getMatomoVersion&format=json"

    def get_current_version(self):
        auth_param = f"&token_auth={self.headers['token']}" if self.headers['token'] else ""
        try:
            response = requests.get(self.endpoint + self.MATOMO_API_ENDPOINT + auth_param, headers=self.headers, timeout=5)
            response.raise_for_status()
            return self.normalize_version(response.json().get("value", "Pas de value"))
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer la version installée ({e})"

    def get_latest_version(self):
        try:
            response = requests.get(self.MATOMO_LATEST_URL, timeout=5)
            response.raise_for_status()
            return self.normalize_version(response.text.strip())
        except requests.RequestException as e:
            return f"Erreur: Impossible de récupérer la dernière version ({e})"
