"""
3D Viewport для визуализации помещения
Упрощённая версия без OpenGL (на QPainter с изометрической проекцией)
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPolygonF

from core.project import Project
from core.room import Room
import math


class Viewport3D(QWidget):
    """3D просмотрщик (изометрическая проекция)"""

    # Цвета
    COLOR_BG = QColor(35, 35, 40)
    COLOR_FLOOR = QColor(80, 70, 60)
    COLOR_WALL = QColor(220, 215, 210)
    COLOR_WALL_DARK = QColor(180, 175, 170)
    COLOR_CEILING = QColor(240, 240, 245)
    COLOR_WINDOW = QColor(135, 206, 250, 180)
    COLOR_DOOR = QColor(139, 90, 43)

    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project

        # Параметры проекции
        self.angle_x = 30  # Угол наклона (изометрия)
        self.angle_z = 45  # Угол поворота
        self.scale = 0.08
        self.offset_x = 0
        self.offset_y = 0

        self.selected_room_index = 0

        self._setup_ui()

    def _setup_ui(self):
        """Настройка UI"""
        self.setMinimumSize(400, 300)

        # Панель управления сверху
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        controls = QHBoxLayout()

        controls.addWidget(QLabel("Комната:"))
        self.room_combo = QComboBox()
        self.room_combo.currentIndexChanged.connect(self._on_room_changed)
        controls.addWidget(self.room_combo)

        controls.addStretch()

        controls.addWidget(QLabel("Поворот:"))
        self.rotation_combo = QComboBox()
        self.rotation_combo.addItems(["45°", "135°", "225°", "315°"])
        self.rotation_combo.currentIndexChanged.connect(self._on_rotation_changed)
        controls.addWidget(self.rotation_combo)

        layout.addLayout(controls)
        layout.addStretch()

        self._update_room_combo()

    def update_project(self, project: Project):
        """Обновить проект"""
        self.project = project
        self._update_room_combo()
        self.update()

    def _update_room_combo(self):
        """Обновить список комнат"""
        self.room_combo.clear()
        for room in self.project.rooms:
            self.room_combo.addItem(room.name, room.id)

        if self.project.rooms:
            self.room_combo.setCurrentIndex(0)

    def _on_room_changed(self, index):
        """Смена комнаты"""
        self.selected_room_index = index
        self.update()

    def _on_rotation_changed(self, index):
        """Смена угла поворота"""
        angles = [45, 135, 225, 315]
        self.angle_z = angles[index]
        self.update()

    def _project_3d_to_2d(self, x: float, y: float, z: float) -> QPointF:
        """Изометрическая проекция 3D -> 2D"""
        # Поворот вокруг Z
        rad_z = math.radians(self.angle_z)
        x_rot = x * math.cos(rad_z) - y * math.sin(rad_z)
        y_rot = x * math.sin(rad_z) + y * math.cos(rad_z)

        # Изометрическая проекция
        rad_x = math.radians(self.angle_x)

        screen_x = x_rot * self.scale
        screen_y = (y_rot * math.cos(rad_x) - z) * self.scale

        # Центрирование
        screen_x += self.width() / 2 + self.offset_x
        screen_y += self.height() / 2 + self.offset_y + 100

        return QPointF(screen_x, screen_y)

    def paintEvent(self, event):
        """Отрисовка"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Фон
        painter.fillRect(self.rect(), self.COLOR_BG)

        # Рисуем комнату
        if self.project.rooms and 0 <= self.selected_room_index < len(self.project.rooms):
            room = self.project.rooms[self.selected_room_index]
            self._draw_room_3d(painter, room)
        else:
            # Сообщение если нет комнат
            painter.setPen(QColor(150, 150, 150))
            painter.setFont(QFont("Arial", 14))
            painter.drawText(
                self.rect(), Qt.AlignCenter,
                "Добавьте комнату для 3D просмотра\n\nМеню: Комната → Добавить"
            )

        painter.end()

    def _draw_room_3d(self, painter: QPainter, room: Room):
        """Отрисовка комнаты в 3D"""
        if len(room.walls) < 3:
            return

        height = room.ceiling_height

        # Собираем точки пола
        floor_points = []
        for wall in room.walls:
            floor_points.append((wall.start.x, wall.start.y, 0))

        # Центрируем комнату
        if floor_points:
            cx = sum(p[0] for p in floor_points) / len(floor_points)
            cy = sum(p[1] for p in floor_points) / len(floor_points)
            floor_points = [(x - cx, y - cy, z) for x, y, z in floor_points]

        # 1. Пол
        floor_polygon = QPolygonF()
        for x, y, z in floor_points:
            floor_polygon.append(self._project_3d_to_2d(x, y, z))

        painter.setPen(QPen(self.COLOR_FLOOR.darker(), 2))
        painter.setBrush(QBrush(self.COLOR_FLOOR))
        painter.drawPolygon(floor_polygon)

        # 2. Стены (сортируем по удалённости для правильного перекрытия)
        walls_to_draw = []
        for i, wall in enumerate(room.walls):
            # Средняя точка стены
            mx = (wall.start.x - cx + wall.end.x - cx) / 2
            my = (wall.start.y - cy + wall.end.y - cy) / 2

            # Расстояние от камеры (упрощённо)
            rad_z = math.radians(self.angle_z)
            dist = mx * math.sin(rad_z) + my * math.cos(rad_z)

            walls_to_draw.append((dist, i, wall))

        # Сортируем: дальние стены рисуем первыми
        walls_to_draw.sort(key=lambda x: x[0], reverse=True)

        for _, i, wall in walls_to_draw:
            x1, y1 = wall.start.x - cx, wall.start.y - cy
            x2, y2 = wall.end.x - cx, wall.end.y - cy

            # Определяем освещённость стены
            dx = x2 - x1
            dy = y2 - y1
            angle = math.atan2(dy, dx)
            light = abs(math.cos(angle - math.radians(self.angle_z)))

            wall_color = QColor(
                int(self.COLOR_WALL.red() * (0.6 + 0.4 * light)),
                int(self.COLOR_WALL.green() * (0.6 + 0.4 * light)),
                int(self.COLOR_WALL.blue() * (0.6 + 0.4 * light))
            )

            # Полигон стены
            wall_polygon = QPolygonF([
                self._project_3d_to_2d(x1, y1, 0),
                self._project_3d_to_2d(x2, y2, 0),
                self._project_3d_to_2d(x2, y2, height),
                self._project_3d_to_2d(x1, y1, height)
            ])

            painter.setPen(QPen(wall_color.darker(), 1))
            painter.setBrush(QBrush(wall_color))
            painter.drawPolygon(wall_polygon)

            # Рисуем окна на стене
            wall_len = wall.length
            if wall_len > 0:
                for window in wall.windows:
                    self._draw_window_3d(
                        painter, wall, window,
                        x1, y1, x2, y2, cx, cy
                    )

                # Рисуем двери
                for door in wall.doors:
                    self._draw_door_3d(
                        painter, wall, door,
                        x1, y1, x2, y2, cx, cy
                    )

        # 3. Потолок (опционально, полупрозрачный)
        ceiling_polygon = QPolygonF()
        for x, y, _ in floor_points:
            ceiling_polygon.append(self._project_3d_to_2d(x, y, height))

        painter.setPen(QPen(self.COLOR_CEILING.darker(), 1))
        ceiling_color = QColor(self.COLOR_CEILING)
        ceiling_color.setAlpha(100)
        painter.setBrush(QBrush(ceiling_color))
        painter.drawPolygon(ceiling_polygon)

    def _draw_window_3d(self, painter, wall, window, x1, y1, x2, y2, cx, cy):
        """Отрисовка окна в 3D"""
        wall_len = wall.length
        dx = (x2 - x1) / wall_len
        dy = (y2 - y1) / wall_len

        # Позиции углов окна
        wx1 = x1 + dx * window.position
        wy1 = y1 + dy * window.position
        wx2 = x1 + dx * (window.position + window.width)
        wy2 = y1 + dy * (window.position + window.width)

        z1 = window.sill_height
        z2 = window.sill_height + window.height

        window_polygon = QPolygonF([
            self._project_3d_to_2d(wx1, wy1, z1),
            self._project_3d_to_2d(wx2, wy2, z1),
            self._project_3d_to_2d(wx2, wy2, z2),
            self._project_3d_to_2d(wx1, wy1, z2)
        ])

        painter.setPen(QPen(QColor(100, 150, 200), 2))
        painter.setBrush(QBrush(self.COLOR_WINDOW))
        painter.drawPolygon(window_polygon)

    def _draw_door_3d(self, painter, wall, door, x1, y1, x2, y2, cx, cy):
        """Отрисовка двери в 3D"""
        wall_len = wall.length
        dx = (x2 - x1) / wall_len
        dy = (y2 - y1) / wall_len

        dx1 = x1 + dx * door.position
        dy1 = y1 + dy * door.position
        dx2 = x1 + dx * (door.position + door.width)
        dy2 = y1 + dy * (door.position + door.width)

        door_polygon = QPolygonF([
            self._project_3d_to_2d(dx1, dy1, 0),
            self._project_3d_to_2d(dx2, dy2, 0),
            self._project_3d_to_2d(dx2, dy2, door.height),
            self._project_3d_to_2d(dx1, dy1, door.height)
        ])

        painter.setPen(QPen(self.COLOR_DOOR.darker(), 2))
        painter.setBrush(QBrush(self.COLOR_DOOR))
        painter.drawPolygon(door_polygon)