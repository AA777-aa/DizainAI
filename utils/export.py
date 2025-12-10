"""
Экспорт проекта в различные форматы
"""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from core.project import Project
from core.materials_calc import MaterialsCalculator


class ProjectExporter:
    """Экспорт проекта"""

    @staticmethod
    def to_json(project: Project, file_path: str) -> bool:
        """Экспорт в JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка экспорта: {e}")
            return False

    @staticmethod
    def to_text_report(project: Project, file_path: str) -> bool:
        """Экспорт в текстовый отчёт"""
        try:
            lines = []
            lines.append("=" * 60)
            lines.append(f"ПРОЕКТ: {project.name}")
            lines.append("=" * 60)
            lines.append(f"Дата создания: {project.created_at}")
            lines.append(f"Автор: {project.author or 'Не указан'}")
            lines.append(f"Описание: {project.description or 'Нет'}")
            lines.append("")
            lines.append(f"Общая площадь: {project.total_area:.2f} м²")
            lines.append(f"Количество комнат: {len(project.rooms)}")
            lines.append("")

            for room in project.rooms:
                lines.append("-" * 40)
                lines.append(f"КОМНАТА: {room.name}")
                lines.append("-" * 40)
                lines.append(f"  Площадь: {room.floor_area:.2f} м²")
                lines.append(f"  Высота потолка: {room.ceiling_height} мм")
                lines.append(f"  Периметр: {room.perimeter:.0f} мм")
                lines.append(f"  Количество стен: {len(room.walls)}")

                for i, wall in enumerate(room.walls, 1):
                    lines.append(f"    Стена {i}: {wall.length:.0f} мм")
                    lines.append(f"      Окна: {len(wall.windows)}, Двери: {len(wall.doors)}")

                lines.append("")

            # Расчёт материалов
            calc = MaterialsCalculator(project)
            lines.append(calc.get_summary_text())

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))

            return True

        except Exception as e:
            print(f"Ошибка экспорта: {e}")
            return False

    @staticmethod
    def to_csv_materials(project: Project, file_path: str) -> bool:
        """Экспорт материалов в CSV"""
        try:
            calc = MaterialsCalculator(project)
            all_materials = calc.calculate_all()

            lines = ["Категория;Материал;Количество;Единица;С запасом;Примечание"]

            category_names = {
                "walls": "Стены",
                "floor": "Пол",
                "ceiling": "Потолок",
                "other": "Прочее"
            }

            for category, materials in all_materials.items():
                cat_name = category_names.get(category, category)
                for mat in materials:
                    lines.append(
                        f"{cat_name};{mat.name};{mat.quantity};{mat.unit};"
                        f"{mat.with_reserve};{mat.notes}"
                    )

            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.write("\n".join(lines))

            return True

        except Exception as e:
            print(f"Ошибка экспорта CSV: {e}")
            return False