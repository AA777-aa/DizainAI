"""
2D Canvas для отрисовки и редактирования плана помещения
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QMenu, QAction, QInputDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect, QPointF
from PyQt5.QtGui import (
    QPainter, QPen, QBrush, QColor, QFont,
    QMouseEvent, QWheelEvent, QPainterPath
)

from core.project import Project
from core.room import Room, Wall, Point2D


class Canvas2D(QWidget):
    """2D редактор плана помещения"""

    # Сигналы
    room_selected = pyqtSignal(str)  # room_id
    wall_selected = pyqtSignal(str, str)  # room_id, wall_id

    # Константы
    GRID_SIZE = 100  # мм
    SCALE_MIN = 0.1
    SCALE_MAX = 5.0

    # Цвета
    COLOR_BACKGROUND = QColor(45, 45, 48)
    COLOR_GRID = QColor(60, 60, 65)
    COLOR_GRID_MAJOR = QColor(80, 80, 85)
    COLOR_WALL = QColor(200, 200, 200)
    COLOR_WALL_SELECTED = QColor(100, 150, 255)
    COLOR_WINDOW = QColor(135, 206, 250)
    COLOR_DOOR = QColor(139, 90, 43)
    COLOR_ROOM_FILL = QColor(80, 80, 90, 100)
    COLOR_TEXT = QColor(220, 220, 220)

    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project

        # Состояние вида
        self.scale = 0.15  # пикселей на мм
        self.offset_x = 50
        self.offset_y = 50

        # Состояние взаимодействия
        self.dragging = False
        self.last_mouse_pos = QPoint()
        self.selected_room_id = None
        self.selected_wall_id = None

        # Режим редактирования
        self.edit_mode = "select"  # select, draw_wall, add_door, add_window

        self._setup_ui()

    def _setup_ui(self):
        """Настройка виджета"""
        self.setMinimumSize(400, 300)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

        # Контекстное меню
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def update_project(self, project: Project):
        """Обновить проект"""
        self.project = project
        self.update()

    def _world_to_screen(self, x: float, y: float) -> QPointF:
        """Конвертация мировых координат в экранные"""
        sx = x * self.scale + self.offset_x
        sy = self.height() - (y * self.scale + self.offset_y)
        return QPointF(sx, sy)

    def _screen_to_world(self, sx: float, sy: float) -> tuple:
        """Конвертация экранных координат в мировые"""
        x = (sx - self.offset_x) / self.scale
        y = (self.height() - sy - self.offset_y) / self.scale
        return (x, y)

    def paintEvent(self, event):
        """Отрисовка канваса"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Фон
        painter.fillRect(self.rect(), self.COLOR_BACKGROUND)

        # Сетка
        self._draw_grid(painter)

        # Комнаты
        for room in self.project.rooms:
            self._draw_room(painter, room)

        # Информация
        self._draw_info(painter)

        painter.end()

    def _draw_grid(self, painter: QPainter):
        """Отрисовка сетки"""
        pen = QPen(self.COLOR_GRID)
        pen.setWidth(1)
        painter.setPen(pen)

        # Размер сетки в пикселях
        grid_px = self.GRID_SIZE * self.scale

        if grid_px < 5:
            return  # Слишком мелкая сетка

        # Определяем границы видимой области в мировых координатах
        x1, y1 = self._screen_to_world(0, self.height())
        x2, y2 = self._screen_to_world(self.width(), 0)

        # Округляем до сетки
        start_x = int(x1 / self.GRID_SIZE) * self.GRID_SIZE
        start_y = int(y1 / self.GRID_SIZE) * self.GRID_SIZE

        # Вертикальные линии
        x = start_x
        while x < x2:
            if x % 1000 == 0:  # Каждый метр - жирная линия
                painter.setPen(QPen(self.COLOR_GRID_MAJOR, 1))
            else:
                painter.setPen(QPen(self.COLOR_GRID, 1))

            p1 = self._world_to_screen(x, y1)
            p2 = self._world_to_screen(x, y2)
            painter.drawLine(p1, p2)
            x += self.GRID_SIZE

        # Горизонтальные линии
        y = start_y
        while y < y2:
            if y % 1000 == 0:
                painter.setPen(QPen(self.COLOR_GRID_MAJOR, 1))
            else:
                painter.setPen(QPen(self.COLOR_GRID, 1))

            p1 = self._world_to_screen(x1, y)
            p2 = self._world_to_screen(x2, y)
            painter.drawLine(p1, p2)
            y += self.GRID_SIZE

    def _draw_room(self, painter: QPainter, room: Room):
        """Отрисовка комнаты"""
        if not room.walls:
            return

        is_selected = room.id == self.selected_room_id

        # Собираем точки для полигона
        points = []
        for wall in room.walls:
            p = self._world_to_screen(wall.start.x, wall.start.y)
            points.append(p)

        # Заливка комнаты
        if points:
            path = QPainterPath()
            path.moveTo(points[0])
            for p in points[1:]:
                path.lineTo(p)
            path.closeSubpath()

            fill_color = QColor(100, 150, 255, 50) if is_selected else self.COLOR_ROOM_FILL
            painter.fillPath(path, QBrush(fill_color))

        # Рисуем стены
        for wall in room.walls:
            self._draw_wall(painter, wall, is_selected)

        # Название комнаты
        if points:
            # Центр комнаты
            cx = sum(p.x() for p in points) / len(points)
            cy = sum(p.y() for p in points) / len(points)

            painter.setPen(self.COLOR_TEXT)
            font = QFont("Arial", 10)
            font.setBold(True)
            painter.setFont(font)

            text = f"{room.name}\n{room.floor_area:.1f} м²"
            painter.drawText(QPointF(cx - 40, cy), room.name)

            font.setBold(False)
            font.setPointSize(9)
            painter.setFont(font)
            painter.drawText(QPointF(cx - 30, cy + 15), f"{room.floor_area:.1f} м²")

    def _draw_wall(self, painter: QPainter, wall: Wall, room_selected: bool):
        """Отрисовка стены с окнами и дверями"""
        p1 = self._world_to_screen(wall.start.x, wall.start.y)
        p2 = self._world_to_screen(wall.end.x, wall.end.y)

        is_selected = wall.id == self.selected_wall_id

        # Стена
        color = self.COLOR_WALL_SELECTED if is_selected else self.COLOR_WALL
        pen = QPen(color, 3 if is_selected else 2)
        painter.setPen(pen)
        painter.drawLine(p1, p2)

        # Направление стены
        dx = wall.end.x - wall.start.x
        dy = wall.end.y - wall.start.y
        length = wall.length

        if length == 0:
            return

        # Нормализованный вектор
        nx = dx / length
        ny = dy / length

        # Рисуем окна
        painter.setPen(QPen(self.COLOR_WINDOW, 4))
        for window in wall.windows:
            # Позиция окна вдоль стены
            wx1 = wall.start.x + nx * window.position
            wy1 = wall.start.y + ny * window.position
            wx2 = wall.start.x + nx * (window.position + window.width)
            wy2 = wall.start.y + ny * (window.position + window.width)

            wp1 = self._world_to_screen(wx1, wy1)
            wp2 = self._world_to_screen(wx2, wy2)
            painter.drawLine(wp1, wp2)

        # Рисуем двери
        painter.setPen(QPen(self.COLOR_DOOR, 4))
        for door in wall.doors:
            dx1 = wall.start.x + nx * door.position
            dy1 = wall.start.y + ny * door.position
            dx2 = wall.start.x + nx * (door.position + door.width)
            dy2 = wall.start.y + ny * (door.position + door.width)

            dp1 = self._world_to_screen(dx1, dy1)
            dp2 = self._world_to_screen(dx2, dy2)
            painter.drawLine(dp1, dp2)

        # Размер стены
        if room_selected or is_selected:
            mid_x = (wall.start.x + wall.end.x) / 2
            mid_y = (wall.start.y + wall.end.y) / 2
            mp = self._world_to_screen(mid_x, mid_y)

            painter.setPen(self.COLOR_TEXT)
            font = QFont("Arial", 8)
            painter.setFont(font)
            painter.drawText(mp + QPointF(5, -5), f"{wall.length:.0f}")

    def _draw_info(self, painter: QPainter):
        """Информация в углу"""
        painter.setPen(self.COLOR_TEXT)
        font = QFont("Arial", 9)
        painter.setFont(font)

        info = f"Масштаб: {self.scale * 1000:.0f}% | Сетка: {self.GRID_SIZE}мм"
        painter.drawText(10, 20, info)

        if self.selected_room_id:
            room = self.project.get_room_by_id(self.selected_room_id)
            if room:
                painter.drawText(10, 40, f"Выбрано: {room.name}")

    def mousePressEvent(self, event: QMouseEvent):
        """Нажатие мыши"""
        if event.button() == Qt.LeftButton:
            # Проверяем клик по комнате
            wx, wy = self._screen_to_world(event.x(), event.y())

            clicked_room = None
            for room in self.project.rooms:
                if self._point_in_room(wx, wy, room):
                    clicked_room = room
                    break

            if clicked_room:
                self.selected_room_id = clicked_room.id
                self.room_selected.emit(clicked_room.id)
            else:
                self.selected_room_id = None

            self.update()

        elif event.button() == Qt.MiddleButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Отпускание мыши"""
        if event.button() == Qt.MiddleButton:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        """Движение мыши"""
        if self.dragging:
            delta = event.pos() - self.last_mouse_pos
            self.offset_x += delta.x()
            self.offset_y -= delta.y()
            self.last_mouse_pos = event.pos()
            self.update()

    def wheelEvent(self, event: QWheelEvent):
        """Масштабирование колёсиком"""
        # Позиция мыши в мировых координатах до масштабирования
        mouse_world_before = self._screen_to_world(event.x(), event.y())

        # Изменяем масштаб
        delta = event.angleDelta().y()
        factor = 1.1 if delta > 0 else 0.9

        new_scale = self.scale * factor
        new_scale = max(self.SCALE_MIN, min(self.SCALE_MAX, new_scale))
        self.scale = new_scale

        # Корректируем смещение, чтобы точка под курсором осталась на месте
        mouse_world_after = self._screen_to_world(event.x(), event.y())

        self.offset_x += (mouse_world_after[0] - mouse_world_before[0]) * self.scale
        self.offset_y += (mouse_world_after[1] - mouse_world_before[1]) * self.scale

        self.update()

    def _point_in_room(self, x: float, y: float, room: Room) -> bool:
        """Проверка попадания точки в комнату"""
        if len(room.walls) < 3:
            return False

        # Собираем точки полигона
        points = [(wall.start.x, wall.start.y) for wall in room.walls]

        # Ray casting алгоритм
        n = len(points)
        inside = False

        j = n - 1
        for i in range(n):
            xi, yi = points[i]
            xj, yj = points[j]

            if ((yi > y) != (yj > y) and
                    x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i

        return inside

    def _show_context_menu(self, pos):
        """Контекстное меню"""
        menu = QMenu(self)

        if self.selected_room_id:
            room = self.project.get_room_by_id(self.selected_room_id)
            if room:
                menu.addAction(f"📐 {room.name}").setEnabled(False)
                menu.addSeparator()

                rename_action = menu.addAction("✏️ Переименовать")
                rename_action.triggered.connect(self._rename_selected_room)

                delete_action = menu.addAction("🗑️ Удалить комнату")
                delete_action.triggered.connect(self._delete_selected_room)
        else:
            menu.addAction("Нет выбранной комнаты").setEnabled(False)

        menu.addSeparator()

        fit_action = menu.addAction("🔍 Вписать в экран")
        fit_action.triggered.connect(self.fit_to_view)

        menu.exec_(self.mapToGlobal(pos))

    def _rename_selected_room(self):
        """Переименовать комнату"""
        room = self.project.get_room_by_id(self.selected_room_id)
        if room:
            name, ok = QInputDialog.getText(
                self, "Переименовать комнату",
                "Новое название:", text=room.name
            )
            if ok and name:
                room.name = name
                self.update()

    def _delete_selected_room(self):
        """Удалить комнату"""
        if self.selected_room_id:
            self.project.remove_room(self.selected_room_id)
            self.selected_room_id = None
            self.update()

    def fit_to_view(self):
        """Вписать все комнаты в экран"""
        if not self.project.rooms:
            return

        # Находим границы всех комнат
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for room in self.project.rooms:
            for wall in room.walls:
                min_x = min(min_x, wall.start.x, wall.end.x)
                max_x = max(max_x, wall.start.x, wall.end.x)
                min_y = min(min_y, wall.start.y, wall.end.y)
                max_y = max(max_y, wall.start.y, wall.end.y)

        if min_x == float('inf'):
            return

        # Размеры содержимого
        content_width = max_x - min_x
        content_height = max_y - min_y

        if content_width == 0 or content_height == 0:
            return

        # Вычисляем масштаб
        margin = 50
        scale_x = (self.width() - 2 * margin) / content_width
        scale_y = (self.height() - 2 * margin) / content_height
        self.scale = min(scale_x, scale_y, self.SCALE_MAX)

        # Центрируем
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        self.offset_x = self.width() / 2 - center_x * self.scale
        self.offset_y = self.height() / 2 - center_y * self.scale

        self.update()