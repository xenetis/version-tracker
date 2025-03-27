import requests
from .abstract import AbstractPlugin, latest_version_cache

class MatomoPlugin(AbstractPlugin):
    def __init__(self, endpoint, headers, translations, **kwargs):
        super().__init__(endpoint=endpoint, headers=headers, translations=translations)

    MATOMO_LATEST_URL = "https://api.matomo.org/1.0/getLatestVersion/"
    MATOMO_API_ENDPOINT = "/index.php?module=API&method=API.getMatomoVersion&format=json"

    def get_current_version(self):
        auth_param = f"&token_auth={self.headers['token']}" if self.headers['token'] else ""
        try:
            response = requests.get(self.endpoint + self.MATOMO_API_ENDPOINT + auth_param, headers=self.headers, timeout=5)
            response.raise_for_status()
            return self.normalize_version(response.json().get("value", self.translations.get("unknown")))
        except requests.RequestException as e:
            return f"Error: unable to retrieve current version"

    def get_latest_version(self):
        if "matomo" in latest_version_cache:
            return latest_version_cache["matomo"]
        try:
            response = requests.get(self.MATOMO_LATEST_URL, timeout=5)
            response.raise_for_status()
            latest_version = self.normalize_version(response.text.strip())
            latest_version_cache["matomo"] = latest_version
            return latest_version
        except requests.RequestException as e:
            return f"Error: unable to retrieve latest version"
