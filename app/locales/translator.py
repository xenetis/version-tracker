import importlib
from flask import request

class Translator:
    def __init__(self, default_lang="en"):
        self.default_lang = default_lang
        self.lang = self.detect_language()
        self.translations = self.load_translations()

    def detect_language(self):
        lang = request.args.get("lang")

        if not lang:
            lang = request.cookies.get("lang")

        if not lang and request.headers.get("Accept-Language"):
            lang = request.headers.get("Accept-Language").split(",")[0].split("-")[0]  # Ex: "fr-FR" -> "fr"

        if lang not in ["en", "fr"]:
            lang = self.default_lang

        return lang

    def load_translations(self):
        try:
            module = importlib.import_module(f"locales.{self.lang}")
            return module.translations
        except ModuleNotFoundError:
            print(f"Warning: Language '{self.lang}' not found, using default language.")
            module = importlib.import_module(f"locales.{self.default_lang}")
            return module.translations

    def t(self, key):
        return self.translations.get(key, key)
