import requests
import logging
from .abstract import AbstractPlugin, latest_version_cache


class DolibarrPlugin(AbstractPlugin):
    DOLIBARR_LATEST_URL = "https://api.github.com/repos/Dolibarr/dolibarr/releases/latest"
    DOLIBARR_API_ENDPOINT = "/api/index.php/status"
    DOLIBARR_LOGIN_API_ENDPOINT = "/api/index.php/login"

    def __init__(self, endpoint, headers, translations, **kwargs):
        super().__init__(endpoint=endpoint, headers=headers, translations=translations)

    def get_current_version(self):
        try:
            endpoint = self.endpoint + self.DOLIBARR_LOGIN_API_ENDPOINT + "?login=" + self.headers["login"] + "&password=" + self.headers["password"]
            response = requests.get(endpoint, headers=self.headers, timeout=5)
            response.raise_for_status()

            token = response.json().get("success").get("token")
            headers = {"DOLAPIKEY": token, **self.headers}
            response = requests.get(self.endpoint + self.DOLIBARR_API_ENDPOINT, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()

            current_version = self.normalize_version(data.get("success", self.translations.get("unknown")).get("dolibarr_version", self.translations.get("unknown"))) if data else self.translations.get("error")

        except requests.RequestException as e:
            logging.error(f"Error retrieving data: {e}")
            return f"Error: unable to retrieve current version"

        return current_version

    def get_latest_version(self):
        if "dolibarr" in latest_version_cache:
            return latest_version_cache["dolibarr"]

        data = self.fetch_version(self.DOLIBARR_LATEST_URL)
        if data and isinstance(data, dict):
            latest_version = self.normalize_version(data.get("tag_name", self.translations.get("unknown"))) if data else self.translations.get("error")
            if latest_version not in [self.translations.get("unknown"), self.translations.get("error")]: latest_version_cache["dolibarr"] = latest_version
        else:
            latest_version = "Erreur"

        return latest_version
