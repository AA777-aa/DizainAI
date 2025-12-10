"""
Шаблоны промптов для GPT
"""

from typing import Dict, List
from core.room import Room
from core.project import Project


class PromptBuilder:
    """Построитель промптов для GPT"""

    # Системные промпты
    SYSTEM_INTERIOR_DESIGNER = """Ты — профессиональный дизайнер интерьера с 15-летним опытом.
Ты создаёшь практичные, стильные и функциональные дизайны.
Учитывай реальные размеры помещения, расположение окон и дверей.
Отвечай на русском языке.
Давай конкретные рекомендации с указанием размеров мебели."""

    SYSTEM_MATERIALS_EXPERT = """Ты — эксперт по строительным и отделочным материалам.
Даёшь практичные советы по выбору материалов с учётом бюджета и качества.
Знаешь актуальные цены и производителей на российском рынке.
Отвечай на русском языке."""

    @staticmethod
    def room_description(room: Room) -> str:
        """Создать описание комнаты для промпта"""
        lines = [
            f"Комната: {room.name}",
            f"Площадь пола: {room.floor_area:.1f} м²",
            f"Высота потолка: {room.ceiling_height} мм",
            f"Периметр: {room.perimeter / 1000:.1f} м",
            ""
        ]

        for i, wall in enumerate(room.walls, 1):
            lines.append(f"Стена {i}: длина {wall.length:.0f} мм")

            for win in wall.windows:
                lines.append(f"  - Окно: {win.width}x{win.height} мм, высота подоконника {win.sill_height} мм")

            for door in wall.doors:
                lines.append(f"  - Дверь: {door.width}x{door.height} мм")

        return "\n".join(lines)

    @staticmethod
    def project_description(project: Project) -> str:
        """Создать описание всего проекта"""
        lines = [
            f"Проект: {project.name}",
            f"Общая площадь: {project.total_area:.1f} м²",
            f"Количество комнат: {len(project.rooms)}",
            ""
        ]

        for room in project.rooms:
            lines.append(PromptBuilder.room_description(room))
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def design_style_prompt(room: Room, style: str, preferences: str = "") -> str:
        """Промпт для генерации дизайна в определённом стиле"""
        room_desc = PromptBuilder.room_description(room)

        prompt = f"""Создай дизайн-проект для следующей комнаты:

{room_desc}

Стиль: {style}

Требования:
1. Предложи расстановку мебели с точными размерами (ширина x глубина x высота в мм)
2. Укажи координаты размещения каждого предмета от угла комнаты
3. Опиши цветовую гамму стен, пола, потолка
4. Предложи освещение (основное и дополнительное)
5. Дай рекомендации по декору

{f'Дополнительные пожелания: {preferences}' if preferences else ''}

Ответ структурируй по разделам."""

        return prompt

    @staticmethod
    def furniture_arrangement_prompt(room: Room, furniture_list: List[str]) -> str:
        """Промпт для оптимальной расстановки мебели"""
        room_desc = PromptBuilder.room_description(room)

        furniture_text = "\n".join(f"- {f}" for f in furniture_list)

        return f"""Помоги оптимально расставить мебель в комнате.

{room_desc}

Мебель для размещения:
{furniture_text}

Требования:
1. Укажи координаты X, Y (в мм от левого нижнего угла) для каждого предмета
2. Укажи угол поворота (0, 90, 180 или 270 градусов)
3. Учти проходы минимум 600 мм
4. Учти расположение окон и дверей
5. Обеспечь эргономику и удобство использования

Ответ в формате JSON:
{{"furniture": [{{"name": "...", "x": 0, "y": 0, "rotation": 0}}]}}"""

    @staticmethod
    def color_scheme_prompt(style: str, room_type: str) -> str:
        """Промпт для подбора цветовой схемы"""
        return f"""Предложи цветовую схему для {room_type} в стиле "{style}".

Укажи:
1. Основной цвет стен (HEX код и название)
2. Цвет акцентной стены (если нужна)
3. Цвет пола
4. Цвет потолка
5. 2-3 акцентных цвета для мебели и декора

Ответ в формате JSON:
{{
    "walls_main": {{"hex": "#XXXXXX", "name": "..."}},
    "walls_accent": {{"hex": "#XXXXXX", "name": "..."}},
    "floor": {{"hex": "#XXXXXX", "name": "..."}},
    "ceiling": {{"hex": "#XXXXXX", "name": "..."}},
    "accents": [{{"hex": "#XXXXXX", "name": "..."}}]
}}"""

    @staticmethod
    def materials_advice_prompt(room: Room, budget: str = "средний") -> str:
        """Промпт для рекомендаций по материалам"""
        room_desc = PromptBuilder.room_description(room)

        return f"""Порекомендуй отделочные материалы для комнаты.

{room_desc}

Бюджет: {budget}

Для каждой поверхности укажи:
1. Рекомендуемый материал
2. Примерную стоимость за м² или единицу
3. Производителя/бренд
4. Плюсы и минусы выбора

Поверхности: пол, стены, потолок."""