"""
Модель комнаты - стены, двери, окна
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from enum import Enum
import uuid
import json


class WallType(Enum):
    """Тип стены"""
    EXTERNAL = "external"  # Внешняя несущая
    INTERNAL = "internal"  # Внутренняя
    PARTITION = "partition"  # Перегородка


@dataclass
class Point2D:
    """Точка на 2D плане"""
    x: float  # мм
    y: float  # мм

    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data: dict) -> 'Point2D':
        return cls(x=data["x"], y=data["y"])


@dataclass
class Window:
    """Окно в стене"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    position: float = 0  # Позиция от начала стены (мм)
    width: float = 1200  # мм
    height: float = 1400  # мм
    sill_height: float = 900  # Высота подоконника (мм)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "position": self.position,
            "width": self.width,
            "height": self.height,
            "sill_height": self.sill_height
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Window':
        return cls(**data)


@dataclass
class Door:
    """Дверь в стене"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    position: float = 0  # Позиция от начала стены (мм)
    width: float = 900  # мм
    height: float = 2100  # мм
    opens_inside: bool = True  # Открывается внутрь
    opens_left: bool = True  # Открывается влево

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "position": self.position,
            "width": self.width,
            "height": self.height,
            "opens_inside": self.opens_inside,
            "opens_left": self.opens_left
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Door':
        return cls(**data)


@dataclass
class Wall:
    """Стена комнаты"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start: Point2D = field(default_factory=lambda: Point2D(0, 0))
    end: Point2D = field(default_factory=lambda: Point2D(1000, 0))
    height: float = 2700  # мм
    thickness: float = 100  # мм
    wall_type: WallType = WallType.INTERNAL
    windows: List[Window] = field(default_factory=list)
    doors: List[Door] = field(default_factory=list)

    @property
    def length(self) -> float:
        """Длина стены в мм"""
        import math
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return math.sqrt(dx * dx + dy * dy)

    @property
    def area(self) -> float:
        """Площадь стены в м²"""
        return (self.length * self.height) / 1_000_000

    @property
    def net_area(self) -> float:
        """Площадь стены без окон и дверей в м²"""
        windows_area = sum(w.width * w.height for w in self.windows) / 1_000_000
        doors_area = sum(d.width * d.height for d in self.doors) / 1_000_000
        return self.area - windows_area - doors_area

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "start": self.start.to_dict(),
            "end": self.end.to_dict(),
            "height": self.height,
            "thickness": self.thickness,
            "wall_type": self.wall_type.value,
            "windows": [w.to_dict() for w in self.windows],
            "doors": [d.to_dict() for d in self.doors]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Wall':
        return cls(
            id=data["id"],
            start=Point2D.from_dict(data["start"]),
            end=Point2D.from_dict(data["end"]),
            height=data["height"],
            thickness=data["thickness"],
            wall_type=WallType(data["wall_type"]),
            windows=[Window.from_dict(w) for w in data.get("windows", [])],
            doors=[Door.from_dict(d) for d in data.get("doors", [])]
        )


@dataclass
class Room:
    """Комната"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Новая комната"
    walls: List[Wall] = field(default_factory=list)
    ceiling_height: float = 2700  # мм

    @property
    def floor_area(self) -> float:
        """Площадь пола в м² (по методу шнурка)"""
        if len(self.walls) < 3:
            return 0

        # Собираем все точки по порядку
        points = [wall.start for wall in self.walls]

        # Формула площади многоугольника (shoelace formula)
        n = len(points)
        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += points[i].x * points[j].y
            area -= points[j].x * points[i].y

        return abs(area) / 2 / 1_000_000  # в м²

    @property
    def perimeter(self) -> float:
        """Периметр комнаты в мм"""
        return sum(wall.length for wall in self.walls)

    @property
    def total_wall_area(self) -> float:
        """Общая площадь стен в м²"""
        return sum(wall.area for wall in self.walls)

    @property
    def net_wall_area(self) -> float:
        """Площадь стен без окон и дверей в м²"""
        return sum(wall.net_area for wall in self.walls)

    @property
    def ceiling_area(self) -> float:
        """Площадь потолка = площадь пола"""
        return self.floor_area

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "walls": [w.to_dict() for w in self.walls],
            "ceiling_height": self.ceiling_height
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Room':
        return cls(
            id=data["id"],
            name=data["name"],
            walls=[Wall.from_dict(w) for w in data["walls"]],
            ceiling_height=data["ceiling_height"]
        )

    @classmethod
    def create_rectangular(cls, name: str, width: float, length: float,
                           height: float = 2700) -> 'Room':
        """Создать прямоугольную комнату"""
        room = cls(name=name, ceiling_height=height)

        # Создаём 4 стены по часовой стрелке
        points = [
            Point2D(0, 0),
            Point2D(width, 0),
            Point2D(width, length),
            Point2D(0, length)
        ]

        for i in range(4):
            wall = Wall(
                start=points[i],
                end=points[(i + 1) % 4],
                height=height
            )
            room.walls.append(wall)

        return room
