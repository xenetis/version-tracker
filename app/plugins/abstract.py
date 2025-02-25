import requests
import re
import logging

def normalize_version(version):
    if version:
        return re.sub(r'^[vV]', '', version).strip()
    return version

def fetch_version(url, headers={}):
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la récupération depuis {url}: {e}")
        return None