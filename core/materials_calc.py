"""
Калькулятор строительных материалов
"""

from dataclasses import dataclass
from typing import Dict, List
from .room import Room
from .project import Project


@dataclass
class MaterialResult:
    """Результат расчёта материала"""
    name: str
    unit: str  # м², м³, шт, кг и т.д.
    quantity: float
    with_reserve: float  # с запасом 10-15%
    notes: str = ""


class MaterialsCalculator:
    """Калькулятор материалов для ремонта"""

    # Нормы расхода материалов
    NORMS = {
        # Штукатурка (кг на м² при слое 10мм)
        "plaster_gypsum": 8.5,  # Гипсовая
        "plaster_cement": 16,  # Цементная

        # Шпаклёвка (кг на м² при слое 1мм)
        "putty_start": 1.2,  # Стартовая
        "putty_finish": 0.5,  # Финишная

        # Грунтовка (л на м²)
        "primer": 0.15,

        # Краска (л на м²)
        "paint": 0.15,

        # Обои (рулоны 10м x 0.53м = 5.3 м²)
        "wallpaper_roll_area": 5.3,

        # Ламинат/кварцвинил - стандартная упаковка ~2 м²
        "flooring_pack_area": 2.0,

        # Плинтус (палки по 2.5м)
        "baseboard_length": 2500,  # мм

        # Натяжной потолок - по площади

        # Плитка - стандартный размер 30x30 = 0.09 м²
        "tile_area": 0.09,
    }

    def __init__(self, project: Project):
        self.project = project

    def calculate_all(self) -> Dict[str, List[MaterialResult]]:
        """Рассчитать все материалы"""
        results = {
            "walls": self._calc_walls(),
            "floor": self._calc_floor(),
            "ceiling": self._calc_ceiling(),
            "other": self._calc_other()
        }
        return results

    def _calc_walls(self) -> List[MaterialResult]:
        """Расчёт материалов для стен"""
        results = []

        total_wall_area = sum(r.net_wall_area for r in self.project.rooms)

        # Штукатурка гипсовая (слой 20мм)
        plaster_kg = total_wall_area * self.NORMS["plaster_gypsum"] * 2
        results.append(MaterialResult(
            name="Штукатурка гипсовая (слой 20мм)",
            unit="кг",
            quantity=round(plaster_kg, 1),
            with_reserve=round(plaster_kg * 1.1, 1),
            notes="Мешки по 30 кг"
        ))

        # Шпаклёвка стартовая (слой 3мм)
        putty_start_kg = total_wall_area * self.NORMS["putty_start"] * 3
        results.append(MaterialResult(
            name="Шпаклёвка стартовая (слой 3мм)",
            unit="кг",
            quantity=round(putty_start_kg, 1),
            with_reserve=round(putty_start_kg * 1.1, 1),
            notes="Мешки по 25 кг"
        ))

        # Шпаклёвка финишная (слой 1мм)
        putty_finish_kg = total_wall_area * self.NORMS["putty_finish"]
        results.append(MaterialResult(
            name="Шпаклёвка финишная",
            unit="кг",
            quantity=round(putty_finish_kg, 1),
            with_reserve=round(putty_finish_kg * 1.15, 1),
            notes="Вёдра по 5-20 кг"
        ))

        # Грунтовка (2 слоя)
        primer_l = total_wall_area * self.NORMS["primer"] * 2
        results.append(MaterialResult(
            name="Грунтовка глубокого проникновения",
            unit="л",
            quantity=round(primer_l, 1),
            with_reserve=round(primer_l * 1.1, 1),
            notes="2 слоя"
        ))

        # Обои
        wallpaper_rolls = total_wall_area / self.NORMS["wallpaper_roll_area"]
        results.append(MaterialResult(
            name="Обои (рулоны 10м x 0.53м)",
            unit="рулон",
            quantity=round(wallpaper_rolls),
            with_reserve=round(wallpaper_rolls * 1.15),
            notes="ИЛИ краска - выбрать одно"
        ))

        # Краска для стен (2 слоя)
        paint_l = total_wall_area * self.NORMS["paint"] * 2
        results.append(MaterialResult(
            name="Краска для стен (2 слоя)",
            unit="л",
            quantity=round(paint_l, 1),
            with_reserve=round(paint_l * 1.1, 1),
            notes="ИЛИ обои - выбрать одно"
        ))

        return results

    def _calc_floor(self) -> List[MaterialResult]:
        """Расчёт материалов для пола"""
        results = []

        total_floor_area = sum(r.floor_area for r in self.project.rooms)
        total_perimeter = sum(r.perimeter for r in self.project.rooms) / 1000  # в метрах

        # Ламинат/кварцвинил
        flooring_packs = total_floor_area / self.NORMS["flooring_pack_area"]
        results.append(MaterialResult(
            name="Ламинат/Кварцвинил (упаковка ~2м²)",
            unit="упак",
            quantity=round(flooring_packs),
            with_reserve=round(flooring_packs * 1.1),
            notes="Запас на подрезку"
        ))

        # Подложка
        results.append(MaterialResult(
            name="Подложка под ламинат",
            unit="м²",
            quantity=round(total_floor_area, 1),
            with_reserve=round(total_floor_area * 1.05, 1),
            notes=""
        ))

        # Плинтус
        baseboard_pcs = (total_perimeter * 1000) / self.NORMS["baseboard_length"]
        results.append(MaterialResult(
            name="Плинтус (палки 2.5м)",
            unit="шт",
            quantity=round(baseboard_pcs),
            with_reserve=round(baseboard_pcs * 1.1),
            notes="+ уголки и заглушки"
        ))

        return results

    def _calc_ceiling(self) -> List[MaterialResult]:
        """Расчёт материалов для потолка"""
        results = []

        total_ceiling_area = sum(r.ceiling_area for r in self.project.rooms)

        # Натяжной потолок
        results.append(MaterialResult(
            name="Натяжной потолок",
            unit="м²",
            quantity=round(total_ceiling_area, 1),
            with_reserve=round(total_ceiling_area, 1),
            notes="Цена за работу + материал"
        ))

        # ИЛИ покраска потолка
        paint_ceiling = total_ceiling_area * self.NORMS["paint"] * 2
        results.append(MaterialResult(
            name="Краска для потолка (2 слоя)",
            unit="л",
            quantity=round(paint_ceiling, 1),
            with_reserve=round(paint_ceiling * 1.1, 1),
            notes="Если не натяжной"
        ))

        return results

    def _calc_other(self) -> List[MaterialResult]:
        """Прочие материалы"""
        results = []

        # Подсчёт дверей и окон
        total_doors = sum(len(w.doors) for r in self.project.rooms for w in r.walls)
        total_windows = sum(len(w.windows) for r in self.project.rooms for w in r.walls)

        if total_doors > 0:
            results.append(MaterialResult(
                name="Межкомнатные двери",
                unit="шт",
                quantity=total_doors,
                with_reserve=total_doors,
                notes="+ дверные коробки и наличники"
            ))

        if total_windows > 0:
            results.append(MaterialResult(
                name="Подоконники",
                unit="шт",
                quantity=total_windows,
                with_reserve=total_windows,
                notes="По размеру оконных проёмов"
            ))

        return results

    def get_summary_text(self) -> str:
        """Получить текстовую сводку"""
        all_materials = self.calculate_all()

        lines = ["=" * 50]
        lines.append("РАСЧЁТ МАТЕРИАЛОВ ДЛЯ РЕМОНТА")
        lines.append("=" * 50)
        lines.append(f"Проект: {self.project.name}")
        lines.append(f"Общая площадь: {self.project.total_area:.1f} м²")
        lines.append("")

        for category, results in all_materials.items():
            category_names = {
                "walls": "СТЕНЫ",
                "floor": "ПОЛ",
                "ceiling": "ПОТОЛОК",
                "other": "ПРОЧЕЕ"
            }
            lines.append(f"\n--- {category_names[category]} ---")

            for mat in results:
                lines.append(f"\n{mat.name}:")
                lines.append(f"  Количество: {mat.quantity} {mat.unit}")
                lines.append(f"  С запасом: {mat.with_reserve} {mat.unit}")
                if mat.notes:
                    lines.append(f"  Примечание: {mat.notes}")

        return "\n".join(lines)
