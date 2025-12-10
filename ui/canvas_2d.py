"""
2D Canvas для редактирования плана помещения
Версия 2.0 - с полноценным редактированием
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QMenu, QAction, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QPointF, QRectF
from PyQt5.QtGui import (
    QPainter, QPen, QBrush, QColor, QFont, QPainterPath,
    QMouseEvent, QWheelEvent, QKeyEvent, QCursor
)

from core.project import Project
from core.room import Room, Wall, Point2D, Window, Door
from .toolbar import EditMode, StatusToolbar
from .styles import COLORS


class SelectionHandle:
    """Маркер для изменения размера"""
    SIZE = 8

    TOP_LEFT = 0
    TOP = 1
    TOP_RIGHT = 2
    RIGHT = 3
    BOTTOM_RIGHT = 4
    BOTTOM = 5
    BOTTOM_LEFT = 6
    LEFT = 7

    def __init__(self, position: int, x: float, y: float):
        self.position = position
        self.x = x
        self.y = y

    def contains(self, px: float, py: float) -> bool:
        half = self.SIZE / 2
        return (self.x - half <= px <= self.x + half and
                self.y - half <= py <= self.y + half)


class Canvas2D(QWidget):
    """2D редактор плана помещения"""

    # Сигналы
    room_selected = pyqtSignal(str)
    wall_selected = pyqtSignal(str, str)
    selection_changed = pyqtSignal(object)

    # Константы
    GRID_SIZE = 100  # мм
    SNAP_THRESHOLD = 20  # пикселей

    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project

        # Состояние вида
        self.scale = 0.1
        self.offset_x = 100
        self.offset_y = 100

        # Режим редактирования
        self.edit_mode = EditMode.SELECT
        self.show_grid = True

        # Выбор
        self.selected_room_id = None
        self.selected_wall_id = None
        self.selected_element = None  # door/window
        self.selection_handles = []
        self.hovered_handle = None

        # Состояние взаимодействия
        self.is_dragging = False
        self.is_panning = False
        self.is_resizing = False
        self.is_drawing = False

        self.last_mouse_pos = QPoint()
        self.drag_start_pos = None
        self.draw_start_pos = None
        self.draw_current_pos = None

        # История для undo/redo
        self.history = []
        self.history_index = -1

        self._setup_ui()

    def _setup_ui(self):
        """Настройка виджета"""
        self.setMinimumSize(400, 300)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        # Курсоры для разных режимов
        self.cursors = {
            EditMode.SELECT: Qt.ArrowCursor,
            EditMode.MOVE: Qt.SizeAllCursor,
            EditMode.DRAW_WALL: Qt.CrossCursor,
            EditMode.DRAW_ROOM: Qt.CrossCursor,
            EditMode.ADD_DOOR: Qt.PointingHandCursor,
            EditMode.ADD_WINDOW: Qt.PointingHandCursor,
        }

    def set_mode(self, mode: str):
        """Установить режим редактирования"""
        self.edit_mode = mode
        self.setCursor(self.cursors.get(mode, Qt.ArrowCursor))

        # Сбрасываем состояние рисования
        self.is_drawing = False
        self.draw_start_pos = None
        self.draw_current_pos = None
        self.update()

    def update_project(self, project: Project):
        """Обновить проект"""
        self.project = project
        self.selected_room_id = None
        self.selected_wall_id = None
        self.update()

    # === Преобразование координат ===

    def world_to_screen(self, x: float, y: float) -> QPointF:
        """Мировые координаты → экранные"""
        sx = x * self.scale + self.offset_x
        sy = self.height() - (y * self.scale + self.offset_y)
        return QPointF(sx, sy)

    def screen_to_world(self, sx: float, sy: float) -> tuple:
        """Экранные координаты → мировые"""
        x = (sx - self.offset_x) / self.scale
        y = (self.height() - sy - self.offset_y) / self.scale
        return (x, y)

    def snap_to_grid(self, x: float, y: float) -> tuple:
        """Привязка к сетке"""
        return (
            round(x / self.GRID_SIZE) * self.GRID_SIZE,
            round(y / self.GRID_SIZE) * self.GRID_SIZE
        )

    # === Отрисовка ===

    def paintEvent(self, event):
        """Отрисовка канваса"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Фон
        painter.fillRect(self.rect(), QColor(COLORS['bg_primary']))

        # Сетка
        if self.show_grid:
            self._draw_grid(painter)

        # Комнаты
        for room in self.project.rooms:
            self._draw_room(painter, room)

        # Текущее рисование
        if self.is_drawing and self.draw_start_pos and self.draw_current_pos:
            self._draw_preview(painter)

        # Маркеры выделения
        if self.selected_room_id:
            self._draw_selection_handles(painter)

        painter.end()

    def _draw_grid(self, painter: QPainter):
        """Отрисовка сетки"""
        grid_px = self.GRID_SIZE * self.scale

        if grid_px < 5:
            return

        # Границы видимой области
        x1, y1 = self.screen_to_world(0, self.height())
        x2, y2 = self.screen_to_world(self.width(), 0)

        start_x = int(x1 / self.GRID_SIZE) * self.GRID_SIZE
        start_y = int(y1 / self.GRID_SIZE) * self.GRID_SIZE

        # Мелкая сетка
        painter.setPen(QPen(QColor(COLORS['grid']), 1))

        x = start_x
        while x < x2:
            p1 = self.world_to_screen(x, y1)
            p2 = self.world_to_screen(x, y2)
            painter.drawLine(p1, p2)
            x += self.GRID_SIZE

        y = start_y
        while y < y2:
            p1 = self.world_to_screen(x1, y)
            p2 = self.world_to_screen(x2, y)
            painter.drawLine(p1, p2)
            y += self.GRID_SIZE

        # Крупная сетка (каждый метр)
        painter.setPen(QPen(QColor(COLORS['grid_major']), 1))

        x = int(start_x / 1000) * 1000
        while x < x2:
            p1 = self.world_to_screen(x, y1)
            p2 = self.world_to_screen(x, y2)
            painter.drawLine(p1, p2)
            x += 1000

        y = int(start_y / 1000) * 1000
        while y < y2:
            p1 = self.world_to_screen(x1, y)
            p2 = self.world_to_screen(x2, y)
            painter.drawLine(p1, p2)
            y += 1000

    def _draw_room(self, painter: QPainter, room: Room):
        """Отрисовка комнаты"""
        if not room.walls:
            return

        is_selected = room.id == self.selected_room_id

        # Собираем точки для полигона
        points = []
        for wall in room.walls:
            p = self.world_to_screen(wall.start.x, wall.start.y)
            points.append(p)

        if not points:
            return

        # Заливка
        path = QPainterPath()
        path.moveTo(points[0])
        for p in points[1:]:
            path.lineTo(p)
        path.closeSubpath()

        fill_color = QColor(COLORS['accent'])
        fill_color.setAlpha(30 if is_selected else 15)
        painter.fillPath(path, QBrush(fill_color))

        # Стены
        for wall in room.walls:
            self._draw_wall(painter, wall, room.id, is_selected)

        # Название и площадь
        cx = sum(p.x() for p in points) / len(points)
        cy = sum(p.y() for p in points) / len(points)

        painter.setPen(QColor(COLORS['text_primary']))
        font = painter.font()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QPointF(cx - 40, cy - 5), room.name)

        font.setBold(False)
        font.setPointSize(9)
        painter.setFont(font)
        painter.setPen(QColor(COLORS['text_secondary']))
        painter.drawText(QPointF(cx - 30, cy + 12), f"{room.floor_area:.1f} м²")

    def _draw_wall(self, painter: QPainter, wall: Wall, room_id: str, room_selected: bool):
        """Отрисовка стены"""
        p1 = self.world_to_screen(wall.start.x, wall.start.y)
        p2 = self.world_to_screen(wall.end.x, wall.end.y)

        is_selected = wall.id == self.selected_wall_id

        # Стена
        if is_selected:
            color = QColor(COLORS['wall_selected'])
            width = 4
        elif room_selected:
            color = QColor(COLORS['wall'])
            width = 3
        else:
            color = QColor(COLORS['wall'])
            color.setAlpha(180)
            width = 2

        painter.setPen(QPen(color, width))
        painter.drawLine(p1, p2)

        # Элементы на стене
        if wall.length > 0:
            dx = wall.end.x - wall.start.x
            dy = wall.end.y - wall.start.y
            length = wall.length
            nx, ny = dx / length, dy / length

            # Окна
            painter.setPen(QPen(QColor(COLORS['window']), 5))
            for window in wall.windows:
                wx1 = wall.start.x + nx * window.position
                wy1 = wall.start.y + ny * window.position
                wx2 = wall.start.x + nx * (window.position + window.width)
                wy2 = wall.start.y + ny * (window.position + window.width)
                painter.drawLine(
                    self.world_to_screen(wx1, wy1),
                    self.world_to_screen(wx2, wy2)
                )

            # Двери
            painter.setPen(QPen(QColor(COLORS['door']), 5))
            for door in wall.doors:
                dx1 = wall.start.x + nx * door.position
                dy1 = wall.start.y + ny * door.position
                dx2 = wall.start.x + nx * (door.position + door.width)
                dy2 = wall.start.y + ny * (door.position + door.width)
                painter.drawLine(
                    self.world_to_screen(dx1, dy1),
                    self.world_to_screen(dx2, dy2)
                )

        # Размер стены
        if room_selected or is_selected:
            mid_x = (wall.start.x + wall.end.x) / 2
            mid_y = (wall.start.y + wall.end.y) / 2
            mp = self.world_to_screen(mid_x, mid_y)

            painter.setPen(QColor(COLORS['text_secondary']))
            font = painter.font()
            font.setPointSize(9)
            painter.setFont(font)

            # Фон для текста
            text = f"{wall.length:.0f}"
            metrics = painter.fontMetrics()
            text_rect = metrics.boundingRect(text)

            bg_rect = QRectF(
                mp.x() - text_rect.width()/2 - 4,
                mp.y() - text_rect.height()/2 - 2,
                text_rect.width() + 8,
                text_rect.height() + 4
            )
            painter.fillRect(bg_rect, QColor(COLORS['bg_primary']))
            painter.drawText(mp + QPointF(-text_rect.width()/2, text_rect.height()/4), text)

    def _draw_preview(self, painter: QPainter):
        """Отрисовка превью при рисовании"""
        if self.edit_mode == EditMode.DRAW_ROOM:
            x1, y1 = self.draw_start_pos
            x2, y2 = self.draw_current_pos

            # Привязка к сетке
            x1, y1 = self.snap_to_grid(x1, y1)
            x2, y2 = self.snap_to_grid(x2, y2)

            p1 = self.world_to_screen(x1, y1)
            p2 = self.world_to_screen(x2, y1)
            p3 = self.world_to_screen(x2, y2)
            p4 = self.world_to_screen(x1, y2)

            # Заливка
            path = QPainterPath()
            path.moveTo(p1)
            path.lineTo(p2)
            path.lineTo(p3)
            path.lineTo(p4)
            path.closeSubpath()

            fill = QColor(COLORS['accent'])
            fill.setAlpha(50)
            painter.fillPath(path, fill)

            # Контур
            pen = QPen(QColor(COLORS['accent']), 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawPath(path)

            # Размеры
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            painter.setPen(QColor(COLORS['text_primary']))
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)

            painter.drawText(
                self.world_to_screen((x1+x2)/2, max(y1, y2) + 200),
                f"{width:.0f} мм"
            )
            painter.drawText(
                self.world_to_screen(max(x1, x2) + 200, (y1+y2)/2),
                f"{height:.0f} мм"
            )

        elif self.edit_mode == EditMode.DRAW_WALL:
            x1, y1 = self.snap_to_grid(*self.draw_start_pos)
            x2, y2 = self.snap_to_grid(*self.draw_current_pos)

            p1 = self.world_to_screen(x1, y1)
            p2 = self.world_to_screen(x2, y2)

            pen = QPen(QColor(COLORS['accent']), 3, Qt.DashLine)
            painter.setPen(pen)
            painter.drawLine(p1, p2)

    def _draw_selection_handles(self, painter: QPainter):
        """Отрисовка маркеров выделения"""
        room = self.project.get_room_by_id(self.selected_room_id)
        if not room or not room.walls:
            return

        # Находим границы комнаты
        min_x = min(w.start.x for w in room.walls)
        max_x = max(w.start.x for w in room.walls)
        min_y = min(w.start.y for w in room.walls)
        max_y = max(w.start.y for w in room.walls)

        # Позиции маркеров
        handle_positions = [
            (min_x, max_y),  # TOP_LEFT
            ((min_x + max_x) / 2, max_y),  # TOP
            (max_x, max_y),  # TOP_RIGHT
            (max_x, (min_y + max_y) / 2),  # RIGHT
            (max_x, min_y),  # BOTTOM_RIGHT
            ((min_x + max_x) / 2, min_y),  # BOTTOM
            (min_x, min_y),  # BOTTOM_LEFT
            (min_x, (min_y + max_y) / 2),  # LEFT
        ]

        self.selection_handles = []

        for i, (wx, wy) in enumerate(handle_positions):
            sp = self.world_to_screen(wx, wy)
            self.selection_handles.append(SelectionHandle(i, sp.x(), sp.y()))

            # Рисуем маркер
            is_hovered = self.hovered_handle == i
            size = SelectionHandle.SIZE + (2 if is_hovered else 0)

            rect = QRectF(sp.x() - size/2, sp.y() - size/2, size, size)

            painter.setPen(QPen(QColor(COLORS['accent']), 2))
            painter.setBrush(QBrush(QColor("#ffffff" if is_hovered else COLORS['bg_primary'])))
            painter.drawRect(rect)

    # === Обработка событий мыши ===

    def mousePressEvent(self, event: QMouseEvent):
        """Нажатие мыши"""
        wx, wy = self.screen_to_world(event.x(), event.y())

        if event.button() == Qt.MiddleButton:
            # Панорамирование
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            return

        if event.button() == Qt.LeftButton:
            # Проверяем маркеры выделения
            for handle in self.selection_handles:
                if handle.contains(event.x(), event.y()):
                    self.is_resizing = True
                    self.hovered_handle = handle.position
                    self.drag_start_pos = (wx, wy)
                    return

            if self.edit_mode == EditMode.SELECT:
                # Выбор комнаты
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

            elif self.edit_mode == EditMode.MOVE:
                # Начало перетаскивания
                for room in self.project.rooms:
                    if self._point_in_room(wx, wy, room):
                        self.selected_room_id = room.id
                        self.is_dragging = True
                        self.drag_start_pos = (wx, wy)
                        break

            elif self.edit_mode in (EditMode.DRAW_WALL, EditMode.DRAW_ROOM):
                # Начало рисования
                self.is_drawing = True
                self.draw_start_pos = (wx, wy)
                self.draw_current_pos = (wx, wy)

            elif self.edit_mode == EditMode.ADD_DOOR:
                self._add_door_at(wx, wy)

            elif self.edit_mode == EditMode.ADD_WINDOW:
                self._add_window_at(wx, wy)

    def mouseMoveEvent(self, event: QMouseEvent):
        """Движение мыши"""
        wx, wy = self.screen_to_world(event.x(), event.y())

        # Обновляем координаты для статусбара
        parent = self.parent()
        while parent:
            if hasattr(parent, 'status_toolbar'):
                parent.status_toolbar.set_coords(wx, wy)
                break
            parent = parent.parent()

        if self.is_panning:
            delta = event.pos() - self.last_mouse_pos
            self.offset_x += delta.x()
            self.offset_y -= delta.y()
            self.last_mouse_pos = event.pos()
            self.update()

        elif self.is_dragging and self.selected_room_id:
            # Перемещение комнаты
            room = self.project.get_room_by_id(self.selected_room_id)
            if room and self.drag_start_pos:
                dx = wx - self.drag_start_pos[0]
                dy = wy - self.drag_start_pos[1]

                for wall in room.walls:
                    wall.start.x += dx
                    wall.start.y += dy
                    wall.end.x += dx
                    wall.end.y += dy

                self.drag_start_pos = (wx, wy)
                self.update()

        elif self.is_resizing:
            self._resize_room(wx, wy)
            self.update()

        elif self.is_drawing:
            self.draw_current_pos = (wx, wy)
            self.update()

        else:
            # Проверяем наведение на маркеры
            old_hovered = self.hovered_handle
            self.hovered_handle = None

            for handle in self.selection_handles:
                if handle.contains(event.x(), event.y()):
                    self.hovered_handle = handle.position
                    break

            if old_hovered != self.hovered_handle:
                self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Отпускание мыши"""
        if event.button() == Qt.MiddleButton:
            self.is_panning = False
            self.setCursor(self.cursors.get(self.edit_mode, Qt.ArrowCursor))

        elif event.button() == Qt.LeftButton:
            if self.is_drawing and self.draw_start_pos and self.draw_current_pos:
                self._finish_drawing()

            self.is_dragging = False
            self.is_resizing = False
            self.is_drawing = False
            self.drag_start_pos = None

    def wheelEvent(self, event: QWheelEvent):
        """Масштабирование"""
        # Позиция мыши до масштабирования
        old_world = self.screen_to_world(event.x(), event.y())

        # Изменяем масштаб
        delta = event.angleDelta().y()
        factor = 1.15 if delta > 0 else 0.85

        new_scale = self.scale * factor
        new_scale = max(0.01, min(2.0, new_scale))
        self.scale = new_scale

        # Корректируем смещение
        new_world = self.screen_to_world(event.x(), event.y())
        self.offset_x += (new_world[0] - old_world[0]) * self.scale
        self.offset_y += (new_world[1] - old_world[1]) * self.scale

        # Обновляем статусбар
        parent = self.parent()
        while parent:
            if hasattr(parent, 'status_toolbar'):
                parent.status_toolbar.set_scale(self.scale)
                break
            parent = parent.parent()

        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        """Обработка клавиш"""
        key = event.key()

        # Быстрые клавиши для инструментов
        shortcuts = {
            Qt.Key_V: EditMode.SELECT,
            Qt.Key_M: EditMode.MOVE,
            Qt.Key_W: EditMode.DRAW_WALL,
            Qt.Key_R: EditMode.DRAW_ROOM,
            Qt.Key_D: EditMode.ADD_DOOR,
            Qt.Key_O: EditMode.ADD_WINDOW,
        }

        if key in shortcuts:
            self.set_mode(shortcuts[key])
            # Уведомляем тулбар
            parent = self.parent()
            while parent:
                if hasattr(parent, 'toolbar'):
                    parent.toolbar.set_mode(shortcuts[key])
                    break
                parent = parent.parent()

        elif key == Qt.Key_Delete:
            self._delete_selected()

        elif key == Qt.Key_Escape:
            self.is_drawing = False
            self.draw_start_pos = None
            self.selected_room_id = None
            self.update()

        elif key == Qt.Key_G:
            self.show_grid = not self.show_grid
            self.update()

        elif key == Qt.Key_Home:
            self.fit_to_view()

    # === Вспомогательные методы ===

    def _point_in_room(self, x: float, y: float, room: Room) -> bool:
        """Проверка попадания точки в комнату"""
        if len(room.walls) < 3:
            return False

        points = [(wall.start.x, wall.start.y) for wall in room.walls]
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

    def _finish_drawing(self):
        """Завершить рисование"""
        if self.edit_mode == EditMode.DRAW_ROOM:
            x1, y1 = self.snap_to_grid(*self.draw_start_pos)
            x2, y2 = self.snap_to_grid(*self.draw_current_pos)

            # Минимальный размер
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            if width >= 500 and height >= 500:
                # Создаём комнату
                room = Room.create_rectangular(
                    "Новая комната",
                    width,
                    height,
                    2700
                )

                # Смещаем к позиции рисования
                offset_x = min(x1, x2)
                offset_y = min(y1, y2)

                for wall in room.walls:
                    wall.start.x += offset_x
                    wall.start.y += offset_y
                    wall.end.x += offset_x
                    wall.end.y += offset_y

                self.project.add_room(room)
                self.selected_room_id = room.id
                self.room_selected.emit(room.id)

        self.draw_start_pos = None
        self.draw_current_pos = None
        self.update()

    def _resize_room(self, wx: float, wy: float):
        """Изменение размера комнаты через маркеры"""
        room = self.project.get_room_by_id(self.selected_room_id)
        if not room:
            return

        # Привязка к сетке
        wx, wy = self.snap_to_grid(wx, wy)

        # Находим текущие границы
        min_x = min(w.start.x for w in room.walls)
        max_x = max(w.start.x for w in room.walls)
        min_y = min(w.start.y for w in room.walls)
        max_y = max(w.start.y for w in room.walls)

        # Изменяем в зависимости от маркера
        handle = self.hovered_handle

        if handle in (SelectionHandle.LEFT, SelectionHandle.TOP_LEFT, SelectionHandle.BOTTOM_LEFT):
            new_min_x = min(wx, max_x - 500)
            delta = new_min_x - min_x
            for wall in room.walls:
                if wall.start.x == min_x:
                    wall.start.x = new_min_x
                if wall.end.x == min_x:
                    wall.end.x = new_min_x

        if handle in (SelectionHandle.RIGHT, SelectionHandle.TOP_RIGHT, SelectionHandle.BOTTOM_RIGHT):
            new_max_x = max(wx, min_x + 500)
            for wall in room.walls:
                if wall.start.x == max_x:
                    wall.start.x = new_max_x
                if wall.end.x == max_x:
                    wall.end.x = new_max_x

        if handle in (SelectionHandle.TOP, SelectionHandle.TOP_LEFT, SelectionHandle.TOP_RIGHT):
            new_max_y = max(wy, min_y + 500)
            for wall in room.walls:
                if wall.start.y == max_y:
                    wall.start.y = new_max_y
                if wall.end.y == max_y:
                    wall.end.y = new_max_y

        if handle in (SelectionHandle.BOTTOM, SelectionHandle.BOTTOM_LEFT, SelectionHandle.BOTTOM_RIGHT):
            new_min_y = min(wy, max_y - 500)
            for wall in room.walls:
                if wall.start.y == min_y:
                    wall.start.y = new_min_y
                if wall.end.y == min_y:
                    wall.end.y = new_min_y

    def _add_door_at(self, wx: float, wy: float):
        """Добавить дверь на ближайшую стену"""
        closest_wall = None
        closest_room = None
        min_dist = float('inf')
        closest_pos = 0

        for room in self.project.rooms:
            for wall in room.walls:
                # Находим ближайшую точку на стене
                dist, pos = self._point_to_wall_distance(wx, wy, wall)
                if dist < min_dist and dist < 500:  # в пределах 500мм от стены
                    min_dist = dist
                    closest_wall = wall
                    closest_room = room
                    closest_pos = pos

        if closest_wall:
            # Проверяем что дверь помещается
            door_width = 900
            if closest_pos + door_width <= closest_wall.length:
                door = Door(
                    position=closest_pos,
                    width=door_width,
                    height=2100
                )
                closest_wall.doors.append(door)
                self.update()

    def _add_window_at(self, wx: float, wy: float):
        """Добавить окно на ближайшую стену"""
        closest_wall = None
        min_dist = float('inf')
        closest_pos = 0

        for room in self.project.rooms:
            for wall in room.walls:
                dist, pos = self._point_to_wall_distance(wx, wy, wall)
                if dist < min_dist and dist < 500:
                    min_dist = dist
                    closest_wall = wall
                    closest_pos = pos

        if closest_wall:
            window_width = 1200
            if closest_pos + window_width <= closest_wall.length:
                window = Window(
                    position=closest_pos,
                    width=window_width,
                    height=1400,
                    sill_height=900
                )
                closest_wall.windows.append(window)
                self.update()

    def _point_to_wall_distance(self, px: float, py: float, wall: Wall) -> tuple:
        """Расстояние от точки до стены и позиция на стене"""
        x1, y1 = wall.start.x, wall.start.y
        x2, y2 = wall.end.x, wall.end.y

        # Вектор стены
        dx = x2 - x1
        dy = y2 - y1
        length_sq = dx*dx + dy*dy

        if length_sq == 0:
            return float('inf'), 0

        # Параметр проекции
        t = max(0, min(1, ((px - x1)*dx + (py - y1)*dy) / length_sq))

        # Ближайшая точка
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy

        # Расстояние
        dist = ((px - proj_x)**2 + (py - proj_y)**2)**0.5

        # Позиция вдоль стены
        position = t * wall.length

        return dist, position

    def _delete_selected(self):
        """Удалить выбранный элемент"""
        if self.selected_room_id:
            self.project.remove_room(self.selected_room_id)
            self.selected_room_id = None
            self.update()
            self.selection_changed.emit(None)

    def fit_to_view(self):
        """Вписать все комнаты в экран"""
        if not self.project.rooms:
            return

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

        content_width = max_x - min_x
        content_height = max_y - min_y

        if content_width == 0 or content_height == 0:
            return

        margin = 80
        scale_x = (self.width() - 2 * margin) / content_width
        scale_y = (self.height() - 2 * margin) / content_height
        self.scale = min(scale_x, scale_y, 0.5)

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        self.offset_x = self.width() / 2 - center_x * self.scale
        self.offset_y = self.height() / 2 - center_y * self.scale

        self.update()

    def _show_context_menu(self, pos):
        """Контекстное меню"""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 8px 24px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {COLORS['accent']};
            }}
        """)

        if self.selected_room_id:
            room = self.project.get_room_by_id(self.selected_room_id)
            if room:
                title = menu.addAction(room.name)
                title.setEnabled(False)
                menu.addSeparator()

                rename_action = menu.addAction("Переименовать")
                rename_action.triggered.connect(self._rename_selected_room)

                delete_action = menu.addAction("Удалить")
                delete_action.triggered.connect(self._delete_selected)
        else:
            add_room = menu.addAction("Добавить комнату")
            add_room.triggered.connect(lambda: self.set_mode(EditMode.DRAW_ROOM))

        menu.addSeparator()

        fit_action = menu.addAction("Вписать в экран")
        fit_action.triggered.connect(self.fit_to_view)

        menu.exec_(self.mapToGlobal(pos))

    def _rename_selected_room(self):
        """Переименовать комнату"""
        room = self.project.get_room_by_id(self.selected_room_id)
        if room:
            name, ok = QInputDialog.getText(
                self, "Переименовать",
                "Название комнаты:", text=room.name
            )
            if ok and name:
                room.name = name
                self.update()