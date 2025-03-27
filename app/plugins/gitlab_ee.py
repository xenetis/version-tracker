import requests
from .abstract import AbstractPlugin, latest_version_cache

class Gitlab_eePlugin(AbstractPlugin):
    def __init__(self, endpoint, headers, translations, **kwargs):
        super().__init__(endpoint=endpoint, headers=headers, translations=translations)

    GITLAB_LATEST_URL = "https://gitlab.com/api/v4/projects/278964/repository/tags"
    GITLAB_API_ENDPOINT = "/api/v4/version"

    def get_current_version(self):
        try:
            data = self.fetch_version(self.endpoint + self.GITLAB_API_ENDPOINT, self.headers)
            return self.normalize_version(data.get("version", self.translations.get("unknown"))) if data else self.translations.get("error")
        except requests.RequestException as e:
            return f"Error: unable to retrieve current version"

    def get_latest_version(self):
        if "gitlab_ee" in latest_version_cache:
            return latest_version_cache["gitlab_ee"]
        try:
            data = self.fetch_version(self.GITLAB_LATEST_URL)
            latest_version = self.normalize_version(data[0].get("name", self.translations.get("unknown"))) if data else self.translations.get("error")
            if latest_version not in [self.translations.get("unknown"), self.translations.get("error")]: latest_version_cache["gitlab_ee"] = latest_version
            return latest_version
        except requests.RequestException as e:
            return f"Error: unable to retrieve latest version"
