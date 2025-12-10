"""
Панель инструментов для редактирования плана
"""

from PyQt5.QtWidgets import (
    QToolBar, QWidget, QHBoxLayout, QVBoxLayout,
    QButtonGroup, QLabel, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize

from .icons import Icons, ToolButton
from .components import Separator


class EditMode:
    """Режимы редактирования"""
    SELECT = "select"
    MOVE = "move"
    DRAW_WALL = "draw_wall"
    DRAW_ROOM = "draw_room"
    ADD_DOOR = "add_door"
    ADD_WINDOW = "add_window"
    ADD_FURNITURE = "add_furniture"
    MEASURE = "measure"


class DrawingToolbar(QToolBar):
    """Панель инструментов рисования"""

    mode_changed = pyqtSignal(str)
    action_triggered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__("Инструменты", parent)

        self.current_mode = EditMode.SELECT

        self.setMovable(False)
        self.setIconSize(QSize(20, 20))
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self._setup_tools()

    def _setup_tools(self):
        """Настройка инструментов"""

        # === Инструменты выбора ===
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.select_btn = self._add_tool_button(
            Icons.SVG_SELECT, "Выбор (V)", EditMode.SELECT, True
        )
        self.select_btn.setChecked(True)

        self.move_btn = self._add_tool_button(
            Icons.SVG_MOVE, "Перемещение (M)", EditMode.MOVE, True
        )

        self.addSeparator()

        # === Инструменты рисования ===
        self.wall_btn = self._add_tool_button(
            Icons.SVG_DRAW_WALL, "Нарисовать стену (W)", EditMode.DRAW_WALL, True
        )

        self.room_btn = self._add_tool_button(
            Icons.SVG_DRAW_RECT, "Нарисовать комнату (R)", EditMode.DRAW_ROOM, True
        )

        self.addSeparator()

        # === Элементы ===
        self.door_btn = self._add_tool_button(
            Icons.SVG_DOOR, "Добавить дверь (D)", EditMode.ADD_DOOR, True
        )

        self.window_btn = self._add_tool_button(
            Icons.SVG_WINDOW, "Добавить окно (O)", EditMode.ADD_WINDOW, True
        )

        self.furniture_btn = self._add_tool_button(
            Icons.SVG_FURNITURE, "Добавить мебель (F)", EditMode.ADD_FURNITURE, True
        )

        self.addSeparator()

        # === Действия (не checkable) ===
        self.undo_btn = self._add_action_button(
            Icons.SVG_UNDO, "Отменить (Ctrl+Z)", "undo"
        )

        self.redo_btn = self._add_action_button(
            Icons.SVG_REDO, "Повторить (Ctrl+Y)", "redo"
        )

        self.addSeparator()

        self.delete_btn = self._add_action_button(
            Icons.SVG_DELETE, "Удалить (Delete)", "delete"
        )

        self.addSeparator()

        # === Вид ===
        self.zoom_in_btn = self._add_action_button(
            Icons.SVG_ZOOM_IN, "Увеличить (+)", "zoom_in"
        )

        self.zoom_out_btn = self._add_action_button(
            Icons.SVG_ZOOM_OUT, "Уменьшить (-)", "zoom_out"
        )

        self.fit_btn = self._add_action_button(
            Icons.SVG_FIT, "Вписать в экран (Home)", "fit"
        )

        self.addSeparator()

        self.grid_btn = ToolButton(Icons.SVG_GRID, "Показать сетку (G)", checkable=True)
        self.grid_btn.setChecked(True)
        self.grid_btn.toggled.connect(lambda c: self.action_triggered.emit("toggle_grid"))
        self.addWidget(self.grid_btn)

    def _add_tool_button(self, icon_svg: str, tooltip: str,
                         mode: str, checkable: bool = False) -> ToolButton:
        """Добавить кнопку инструмента"""
        btn = ToolButton(icon_svg, tooltip, checkable=checkable)

        if checkable:
            self.btn_group.addButton(btn)
            btn.toggled.connect(lambda checked, m=mode: self._on_mode_toggled(checked, m))

        self.addWidget(btn)
        return btn

    def _add_action_button(self, icon_svg: str, tooltip: str, action: str) -> ToolButton:
        """Добавить кнопку действия"""
        btn = ToolButton(icon_svg, tooltip)
        btn.clicked.connect(lambda: self.action_triggered.emit(action))
        self.addWidget(btn)
        return btn

    def _on_mode_toggled(self, checked: bool, mode: str):
        """Смена режима"""
        if checked:
            self.current_mode = mode
            self.mode_changed.emit(mode)

    def set_mode(self, mode: str):
        """Установить режим программно"""
        mode_buttons = {
            EditMode.SELECT: self.select_btn,
            EditMode.MOVE: self.move_btn,
            EditMode.DRAW_WALL: self.wall_btn,
            EditMode.DRAW_ROOM: self.room_btn,
            EditMode.ADD_DOOR: self.door_btn,
            EditMode.ADD_WINDOW: self.window_btn,
            EditMode.ADD_FURNITURE: self.furniture_btn,
        }

        btn = mode_buttons.get(mode)
        if btn:
            btn.setChecked(True)


class StatusToolbar(QWidget):
    """Панель статуса внизу канваса"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(16)

        # Режим
        self.mode_label = QLabel("Режим: Выбор")
        self.mode_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
        layout.addWidget(self.mode_label)

        layout.addWidget(Separator("vertical"))

        # Координаты
        self.coords_label = QLabel("X: 0  Y: 0")
        self.coords_label.setStyleSheet("color: #64748b; font-size: 12px; font-family: monospace;")
        layout.addWidget(self.coords_label)

        layout.addWidget(Separator("vertical"))

        # Масштаб
        self.scale_label = QLabel("100%")
        self.scale_label.setStyleSheet("color: #64748b; font-size: 12px;")
        layout.addWidget(self.scale_label)

        layout.addStretch()

        # Подсказка
        self.hint_label = QLabel("ЛКМ - выбрать • СКМ - перемещение • Колесо - масштаб")
        self.hint_label.setStyleSheet("color: #475569; font-size: 11px;")
        layout.addWidget(self.hint_label)

    def set_mode(self, mode: str):
        mode_names = {
            EditMode.SELECT: "Выбор",
            EditMode.MOVE: "Перемещение",
            EditMode.DRAW_WALL: "Рисование стены",
            EditMode.DRAW_ROOM: "Рисование комнаты",
            EditMode.ADD_DOOR: "Добавление двери",
            EditMode.ADD_WINDOW: "Добавление окна",
            EditMode.ADD_FURNITURE: "Добавление мебели",
        }
        self.mode_label.setText(f"Режим: {mode_names.get(mode, mode)}")

    def set_coords(self, x: float, y: float):
        self.coords_label.setText(f"X: {x:.0f}  Y: {y:.0f}")

    def set_scale(self, scale: float):
        self.scale_label.setText(f"{scale * 100:.0f}%")

    def set_hint(self, text: str):
        self.hint_label.setText(text)