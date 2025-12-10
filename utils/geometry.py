"""
Геометрические утилиты
"""

import math
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float
    rotation: float = 0  # градусы

    @property
    def center(self) -> Point:
        return Point(self.x + self.width / 2, self.y + self.height / 2)

    @property
    def area(self) -> float:
        return self.width * self.height

    def contains_point(self, p: Point) -> bool:
        """Проверка попадания точки в прямоугольник (без учёта поворота)"""
        return (self.x <= p.x <= self.x + self.width and
                self.y <= p.y <= self.y + self.height)

    def intersects(self, other: 'Rectangle') -> bool:
        """Проверка пересечения с другим прямоугольником"""
        return not (self.x + self.width < other.x or
                    other.x + other.width < self.x or
                    self.y + self.height < other.y or
                    other.y + other.height < self.y)


class GeometryUtils:
    """Геометрические утилиты"""

    @staticmethod
    def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Расстояние между двумя точками"""
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    @staticmethod
    def polygon_area(points: List[Tuple[float, float]]) -> float:
        """
        Площадь многоугольника по формуле шнурка (Shoelace)
        Точки должны идти по порядку (по или против часовой)
        """
        n = len(points)
        if n < 3:
            return 0

        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]

        return abs(area) / 2

    @staticmethod
    def polygon_perimeter(points: List[Tuple[float, float]]) -> float:
        """Периметр многоугольника"""
        n = len(points)
        if n < 2:
            return 0

        perimeter = 0
        for i in range(n):
            j = (i + 1) % n
            perimeter += GeometryUtils.distance(points[i], points[j])

        return perimeter

    @staticmethod
    def point_in_polygon(point: Tuple[float, float],
                         polygon: List[Tuple[float, float]]) -> bool:
        """Проверка нахождения точки внутри многоугольника (Ray casting)"""
        x, y = point
        n = len(polygon)
        inside = False

        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]

            if ((yi > y) != (yj > y) and
                    x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside

            j = i

        return inside

    @staticmethod
    def line_intersection(
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        p3: Tuple[float, float],
        p4: Tuple[float, float]
    ) -> Optional[Tuple[float, float]]:
        """Найти точку пересечения двух отрезков"""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if abs(denom) < 1e-10:
            return None  # Параллельны

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

        if 0 <= t <= 1 and 0 <= u <= 1:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)

        return None

    @staticmethod
    def rotate_point(
        point: Tuple[float, float],
        center: Tuple[float, float],
        angle_degrees: float
    ) -> Tuple[float, float]:
        """Повернуть точку вокруг центра"""
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        x, y = point
        cx, cy = center

        # Сдвиг к началу координат
        x -= cx
        y -= cy

        # Поворот
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a

        # Сдвиг обратно
        return (new_x + cx, new_y + cy)

    @staticmethod
    def snap_to_grid(value: float, grid_size: float) -> float:
        """Привязка к сетке"""
        return round(value / grid_size) * grid_size

    @staticmethod
    def mm_to_m(mm: float) -> float:
        """Миллиметры в метры"""
        return mm / 1000

    @staticmethod
    def m_to_mm(m: float) -> float:
        """Метры в миллиметры"""
        return m * 1000

    @staticmethod
    def sqmm_to_sqm(sqmm: float) -> float:
        """Квадратные миллиметры в квадратные метры"""
        return sqmm / 1_000_000