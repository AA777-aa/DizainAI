"""
Настройки приложения DizainAI
"""

import os
import json
from pathlib import Path


class Settings:
    """Класс для управления настройками приложения"""

    DEFAULT_SETTINGS = {
        "openai_api_key": "",
        "gpt_model": "gpt-4o",
        "language": "ru",
        "default_wall_height": 2700,  # мм
        "default_wall_thickness": 100,  # мм
        "grid_size": 100,  # мм
        "units": "mm",  # mm или cm
        "theme": "dark",
        "recent_projects": [],
        "max_recent_projects": 10,
    }

    def __init__(self):
        self.config_dir = Path.home() / ".dizainai"
        self.config_file = self.config_dir / "settings.json"
        self.settings = {}
        self._load()

    def _load(self):
        """Загрузка настроек из файла"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            except Exception:
                self.settings = {}

        # Заполняем отсутствующие значения дефолтными
        for key, value in self.DEFAULT_SETTINGS.items():
            if key not in self.settings:
                self.settings[key] = value

    def save(self):
        """Сохранение настроек в файл"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default=None):
        """Получить значение настройки"""
        return self.settings.get(key, default)

    def set(self, key: str, value):
        """Установить значение настройки"""
        self.settings[key] = value
        self.save()

    @property
    def api_key(self) -> str:
        """OpenAI API ключ"""
        # Сначала проверяем переменную окружения
        env_key = os.environ.get("OPENAI_API_KEY")
        if env_key:
            return env_key
        return self.settings.get("openai_api_key", "")

    @api_key.setter
    def api_key(self, value: str):
        self.set("openai_api_key", value)
