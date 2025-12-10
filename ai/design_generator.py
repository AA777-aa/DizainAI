"""
Генератор дизайна с использованием GPT
"""

import json
import re
from typing import Optional, Dict, List, Callable
from dataclasses import dataclass

from .gpt_client import GPTClient, GPTResponse
from .prompts import PromptBuilder
from core.room import Room
from core.project import Project
from core.furniture import FurnitureItem, FurnitureCategory


@dataclass
class DesignSuggestion:
    """Предложение по дизайну"""
    description: str
    furniture_placements: List[Dict]
    color_scheme: Dict
    materials: Dict
    raw_response: str


class DesignGenerator:
    """Генератор дизайн-предложений"""

    STYLES = {
        "scandinavian": "Скандинавский",
        "minimalist": "Минимализм",
        "modern": "Современный",
        "classic": "Классический",
        "loft": "Лофт",
        "japandi": "Джапанди",
        "mid_century": "Mid-Century Modern",
        "industrial": "Индустриальный",
        "provence": "Прованс",
        "contemporary": "Контемпорари"
    }

    ROOM_TYPES = {
        "living": "Гостиная",
        "bedroom": "Спальня",
        "kitchen": "Кухня",
        "bathroom": "Ванная",
        "office": "Кабинет",
        "kids": "Детская",
        "hallway": "Прихожая"
    }

    def __init__(self, gpt_client: GPTClient):
        self.gpt = gpt_client
        self.prompt_builder = PromptBuilder()

    def generate_design(
        self,
        room: Room,
        style: str,
        preferences: str = "",
        callback: Optional[Callable[[str], None]] = None
    ) -> Optional[DesignSuggestion]:
        """
        Сгенерировать дизайн для комнаты

        Args:
            room: Комната для дизайна
            style: Стиль дизайна
            preferences: Дополнительные пожелания
            callback: Функция для отображения прогресса

        Returns:
            DesignSuggestion или None при ошибке
        """
        if callback:
            callback("Генерация дизайн-концепции...")

        prompt = PromptBuilder.design_style_prompt(room, style, preferences)

        response = self.gpt.send_message([
            {"role": "system", "content": PromptBuilder.SYSTEM_INTERIOR_DESIGNER},
            {"role": "user", "content": prompt}
        ])

        if not response.success:
            if callback:
                callback(f"Ошибка: {response.error}")
            return None

        if callback:
            callback("Анализ ответа...")

        # Парсим ответ
        return DesignSuggestion(
            description=response.content,
            furniture_placements=[],  # TODO: парсинг JSON из ответа
            color_scheme={},
            materials={},
            raw_response=response.content
        )

    def suggest_furniture_layout(
        self,
        room: Room,
        furniture_names: List[str]
    ) -> Optional[List[Dict]]:
        """Получить рекомендации по расстановке мебели"""
        prompt = PromptBuilder.furniture_arrangement_prompt(room, furniture_names)

        response = self.gpt.send_message([
            {"role": "system", "content": PromptBuilder.SYSTEM_INTERIOR_DESIGNER},
            {"role": "user", "content": prompt}
        ])

        if not response.success:
            return None

        # Пытаемся извлечь JSON из ответа
        try:
            json_match = re.search(r'\{[\s\S]*\}', response.content)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("furniture", [])
        except json.JSONDecodeError:
            pass

        return None

    def get_color_scheme(self, style: str, room_type: str) -> Optional[Dict]:
        """Получить цветовую схему"""
        prompt = PromptBuilder.color_scheme_prompt(
            self.STYLES.get(style, style),
            self.ROOM_TYPES.get(room_type, room_type)
        )

        response = self.gpt.send_simple(
            prompt,
            PromptBuilder.SYSTEM_INTERIOR_DESIGNER
        )

        if not response.success:
            return None

        try:
            json_match = re.search(r'\{[\s\S]*\}', response.content)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

        return None

    def get_materials_advice(
        self,
        room: Room,
        budget: str = "средний"
    ) -> Optional[str]:
        """Получить рекомендации по материалам"""
        prompt = PromptBuilder.materials_advice_prompt(room, budget)

        response = self.gpt.send_message([
            {"role": "system", "content": PromptBuilder.SYSTEM_MATERIALS_EXPERT},
            {"role": "user", "content": prompt}
        ])

        if response.success:
            return response.content
        return None

    def chat(self, message: str, context: Optional[Project] = None) -> str:
        """Чат с AI-ассистентом"""
        messages = [
            {"role": "system", "content": PromptBuilder.SYSTEM_INTERIOR_DESIGNER}
        ]

        if context:
            project_desc = PromptBuilder.project_description(context)
            messages.append({
                "role": "system",
                "content": f"Контекст проекта:\n{project_desc}"
            })

        messages.append({"role": "user", "content": message})

        response = self.gpt.send_message(messages)

        if response.success:
            return response.content
        return f"Ошибка: {response.error}"