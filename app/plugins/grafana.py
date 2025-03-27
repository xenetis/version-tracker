import requests
from .abstract import AbstractPlugin, latest_version_cache

class GrafanaPlugin(AbstractPlugin):
    def __init__(self, endpoint, headers, translations, **kwargs):
        super().__init__(endpoint=endpoint, headers=headers, translations=translations)

    GRAFANA_LATEST_URL = "https://api.github.com/repos/grafana/grafana/releases/latest"
    GRAFANA_API_ENDPOINT = "/api/health"

    def get_current_version(self):
        try:
            data = self.fetch_version(self.endpoint + self.GRAFANA_API_ENDPOINT, self.headers)
            return self.normalize_version(data.get("version", self.translations.get("unknown"))) if data else self.translations.get("error")
        except requests.RequestException as e:
            return f"Error: unable to retrieve current version"

    def get_latest_version(self):
        if "grafana" in latest_version_cache:
            return latest_version_cache["grafana"]
        try:
            data = self.fetch_version(self.GRAFANA_LATEST_URL)
            latest_version = self.normalize_version(data.get("tag_name", self.translations.get("unknown"))) if data else self.translations.get("error")
            if latest_version not in [self.translations.get("unknown"), self.translations.get("error")]: latest_version_cache["grafana"] = latest_version
            return latest_version
        except requests.RequestException as e:
            return "Error: unable to retrieve latest version"
