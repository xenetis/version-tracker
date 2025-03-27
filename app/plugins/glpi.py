import requests
from .abstract import AbstractPlugin, latest_version_cache

class GlpiPlugin(AbstractPlugin):
    def __init__(self, endpoint, headers, translations, **kwargs):
        super().__init__(endpoint=endpoint, headers=headers, translations=translations)

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
            return response.json().get("cfg_glpi").get("version", self.translations.get("unknown"))
        except requests.RequestException as e:
            return f"Error: unable to retrieve current version"

    def get_latest_version(self):
        if "glpi" in latest_version_cache:
            return latest_version_cache["glpi"]
        try:
            response = requests.get(self.GLPI_LATEST_URL, timeout=5)
            response.raise_for_status()
            latest_version = self.normalize_version(response.json().get("tag_name", self.translations.get("unknown")))
            if latest_version != self.translations.get("unknown"): latest_version_cache["glpi"] = latest_version
            return latest_version
        except requests.RequestException as e:
            return f"Error: unable to retrieve latest version"
