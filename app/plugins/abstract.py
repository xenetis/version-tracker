from abc import ABC, abstractmethod
from cachetools import TTLCache
import requests
import re
import logging

latest_version_cache = TTLCache(maxsize=100, ttl=3600)

class AbstractPlugin(ABC):

    def __init__(self, endpoint, headers={}):
        self.endpoint = endpoint
        self.headers = headers

    @abstractmethod
    def get_current_version(self):
        pass

    @abstractmethod
    def get_latest_version(self):
        pass

    def fetch_json(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des données depuis {url}: {e}")
            return None

    def normalize_version(self, version):
        if version:
            return re.sub(r'^[vV]', '', version).strip()
        return version

    @staticmethod
    def fetch_version(url, headers={}):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Erreur lors de la récupération depuis {url}: {e}")
            return None

    def get_versions(self):
        return self.get_current_version(), self.get_latest_version()
