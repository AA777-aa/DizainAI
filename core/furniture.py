"""
Мебель и объекты интерьера
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import uuid


class FurnitureCategory(Enum):
    """Категории мебели"""
    SEATING = "seating"  # Диваны, кресла, стулья
    TABLES = "tables"  # Столы
    STORAGE = "storage"  # Шкафы, комоды
    BEDS = "beds"  # Кровати
    LIGHTING = "lighting"  # Освещение
    DECOR = "decor"  # Декор
    APPLIANCES = "appliances"  # Техника
    BATHROOM = "bathroom"  # Сантехника
    KITCHEN = "kitchen"  # Кухонная мебель


@dataclass
class FurnitureItem:
    """Предмет мебели"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Предмет"
    category: FurnitureCategory = FurnitureCategory.DECOR

    # Размеры в мм
    width: float = 500
    depth: float = 500
    height: float = 500

    # Позиция в комнате (мм)
    x: float = 0
    y: float = 0
    z: float = 0  # Высота от пола

    # Поворот в градусах
    rotation: float = 0

    # Цвет для отображения (RGB)
    color: tuple = (150, 150, 150)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "width": self.width,
            "depth": self.depth,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "rotation": self.rotation,
            "color": self.color
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'FurnitureItem':
        data_copy = data.copy()
        data_copy["category"] = FurnitureCategory(data["category"])
        data_copy["color"] = tuple(data["color"])
        return cls(**data_copy)


@dataclass
class Furniture:
    """Коллекция мебели в комнате"""
    items: List[FurnitureItem] = field(default_factory=list)

    def add(self, item: FurnitureItem):
        self.items.append(item)

    def remove(self, item_id: str):
        self.items = [i for i in self.items if i.id != item_id]

    def get_by_id(self, item_id: str) -> Optional[FurnitureItem]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def to_dict(self) -> dict:
        return {"items": [i.to_dict() for i in self.items]}

    @classmethod
    def from_dict(cls, data: dict) -> 'Furniture':
        return cls(items=[FurnitureItem.from_dict(i) for i in data["items"]])


# Библиотека стандартной мебели
FURNITURE_LIBRARY: Dict[str, dict] = {
    "sofa_3seat": {
        "name": "Диван 3-местный",
        "category": FurnitureCategory.SEATING,
        "width": 2200, "depth": 900, "height": 850,
        "color": (100, 100, 180)
    },
    "sofa_2seat": {
        "name": "Диван 2-местный",
        "category": FurnitureCategory.SEATING,
        "width": 1600, "depth": 900, "height": 850,
        "color": (100, 100, 180)
    },
    "armchair": {
        "name": "Кресло",
        "category": FurnitureCategory.SEATING,
        "width": 800, "depth": 850, "height": 900,
        "color": (120, 100, 160)
    },
    "dining_table": {
        "name": "Обеденный стол",
        "category": FurnitureCategory.TABLES,
        "width": 1400, "depth": 900, "height": 750,
        "color": (139, 90, 43)
    },
    "coffee_table": {
        "name": "Журнальный столик",
        "category": FurnitureCategory.TABLES,
        "width": 1000, "depth": 600, "height": 450,
        "color": (139, 90, 43)
    },
    "wardrobe": {
        "name": "Шкаф-купе",
        "category": FurnitureCategory.STORAGE,
        "width": 2000, "depth": 600, "height": 2400,
        "color": (210, 180, 140)
    },
    "bed_double": {
        "name": "Кровать двуспальная",
        "category": FurnitureCategory.BEDS,
        "width": 1800, "depth": 2100, "height": 500,
        "color": (180, 180, 200)
    },
    "bed_single": {
        "name": "Кровать односпальная",
        "category": FurnitureCategory.BEDS,
        "width": 900, "depth": 2000, "height": 500,
        "color": (180, 180, 200)
    },
    "tv_stand": {
        "name": "ТВ-тумба",
        "category": FurnitureCategory.STORAGE,
        "width": 1500, "depth": 450, "height": 500,
        "color": (80, 80, 80)
    },
    "desk": {
        "name": "Письменный стол",
        "category": FurnitureCategory.TABLES,
        "width": 1200, "depth": 600, "height": 750,
        "color": (139, 90, 43)
    },
    "chair": {
        "name": "Стул",
        "category": FurnitureCategory.SEATING,
        "width": 450, "depth": 500, "height": 900,
        "color": (139, 90, 43)
    },
    "toilet": {
        "name": "Унитаз",
        "category": FurnitureCategory.BATHROOM,
        "width": 400, "depth": 650, "height": 400,
        "color": (255, 255, 255)
    },
    "bathtub": {
        "name": "Ванна",
        "category": FurnitureCategory.BATHROOM,
        "width": 700, "depth": 1700, "height": 600,
        "color": (255, 255, 255)
    },
    "sink": {
        "name": "Раковина",
        "category": FurnitureCategory.BATHROOM,
        "width": 600, "depth": 450, "height": 850,
        "color": (255, 255, 255)
    },
    "fridge": {
        "name": "Холодильник",
        "category": FurnitureCategory.APPLIANCES,
        "width": 600, "depth": 650, "height": 1850,
        "color": (200, 200, 200)
    },
    "washing_machine": {
        "name": "Стиральная машина",
        "category": FurnitureCategory.APPLIANCES,
        "width": 600, "depth": 600, "height": 850,
        "color": (200, 200, 200)
    },
}


def create_furniture_from_library(key: str, x: float = 0, y: float = 0) -> FurnitureItem:
    """Создать мебель из библиотеки"""
    if key not in FURNITURE_LIBRARY:
        raise ValueError(f"Мебель '{key}' не найдена в библиотеке")

    data = FURNITURE_LIBRARY[key].copy()
    return FurnitureItem(
        name=data["name"],
        category=data["category"],
        width=data["width"],
        depth=data["depth"],
        height=data["height"],
        x=x,
        y=y,
        color=data["color"]
    )
