"""
Панель свойств проекта v2.0
Чистый дизайн без эмодзи
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QLineEdit, QSpinBox, QListWidget, QListWidgetItem,
    QFrame, QSizePolicy, QStackedWidget
)
from PyQt5.QtCore import Qt, pyqtSignal

from core.project import Project
from core.room import Room
from ..icons import Icons
from ..components import (
    Card, SectionHeader, PropertyRow, StatCard,
    ActionButton, Separator, EmptyState
)


class PropertiesPanel(QWidget):
    """Панель свойств проекта"""

    project_changed = pyqtSignal()

    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project
        self.current_room = None

        self._setup_ui()

    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # === Скролл ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 0, 8, 0)
        self.content_layout.setSpacing(16)

        # === Секция проекта ===
        self._create_project_section()

        # === Секция статистики ===
        self._create_stats_section()

        # === Секция комнат ===
        self._create_rooms_section()

        # === Секция свойств комнаты ===
        self._create_room_properties_section()

        # === Секция стен ===
        self._create_walls_section()

        self.content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

        self._update_display()

    def _create_project_section(self):
        """Секция информации о проекте"""
        section = Card()
        layout = QVBoxLayout(section)
        layout.setSpacing(12)

        # Заголовок
        header = SectionHeader("Проект", Icons.SVG_HOME)
        layout.addWidget(header)

        # Название
        self.project_name_row = PropertyRow("Название", "text")
        self.project_name_row.value_changed.connect(self._on_project_name_changed)
        layout.addWidget(self.project_name_row)

        self.content_layout.addWidget(section)

    def _create_stats_section(self):
        """Секция статистики"""
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        self.area_stat = StatCard(
            "Общая площадь",
            "0 м²",
            Icons.SVG_LAYERS,
            "#10b981"
        )
        stats_layout.addWidget(self.area_stat)

        self.rooms_stat = StatCard(
            "Комнат",
            "0",
            Icons.SVG_HOME,
            "#6366f1"
        )
        stats_layout.addWidget(self.rooms_stat)

        self.content_layout.addLayout(stats_layout)

    def _create_rooms_section(self):
        """Секция списка комнат"""
        section = Card()
        layout = QVBoxLayout(section)
        layout.setSpacing(12)

        header = SectionHeader("Комнаты", Icons.SVG_GRID)
        layout.addWidget(header)

        # Список комнат
        self.rooms_list = QListWidget()
        self.rooms_list.setMinimumHeight(120)
        self.rooms_list.setMaximumHeight(200)
        self.rooms_list.currentItemChanged.connect(self._on_room_selected)
        layout.addWidget(self.rooms_list)

        # Кнопки
        buttons = QHBoxLayout()
        buttons.setSpacing(8)

        add_btn = ActionButton("Добавить", Icons.SVG_PLUS, "primary")
        add_btn.clicked.connect(self._add_room_clicked)
        buttons.addWidget(add_btn)

        del_btn = ActionButton("Удалить", Icons.SVG_DELETE, "danger")
        del_btn.clicked.connect(self._delete_room_clicked)
        buttons.addWidget(del_btn)

        layout.addLayout(buttons)

        self.content_layout.addWidget(section)

    def _create_room_properties_section(self):
        """Секция свойств выбранной комнаты"""
        self.room_section = Card()
        layout = QVBoxLayout(self.room_section)
        layout.setSpacing(12)

        header = SectionHeader("Свойства комнаты", Icons.SVG_SETTINGS)
        layout.addWidget(header)

        # Название
        self.room_name_row = PropertyRow("Название", "text")
        self.room_name_row.value_changed.connect(self._on_room_name_changed)
        layout.addWidget(self.room_name_row)

        layout.addWidget(Separator())

        # Метрики в сетке
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(16)

        # Площадь
        area_col = QVBoxLayout()
        area_col.setSpacing(4)
        self.room_area_value = QLabel("0 м²")
        self.room_area_value.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981;")
        area_col.addWidget(self.room_area_value)
        area_label = QLabel("Площадь")
        area_label.setStyleSheet("color: #64748b; font-size: 11px;")
        area_col.addWidget(area_label)
        metrics_layout.addLayout(area_col)

        # Периметр
        perim_col = QVBoxLayout()
        perim_col.setSpacing(4)
        self.room_perimeter_value = QLabel("0 м")
        self.room_perimeter_value.setStyleSheet("font-size: 18px; font-weight: bold; color: #f8fafc;")
        perim_col.addWidget(self.room_perimeter_value)
        perim_label = QLabel("Периметр")
        perim_label.setStyleSheet("color: #64748b; font-size: 11px;")
        perim_col.addWidget(perim_label)
        metrics_layout.addLayout(perim_col)

        metrics_layout.addStretch()
        layout.addLayout(metrics_layout)

        layout.addWidget(Separator())

        # Высота
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Высота потолка:"))
        self.room_height_spin = QSpinBox()
        self.room_height_spin.setRange(2000, 5000)
        self.room_height_spin.setSuffix(" мм")
        self.room_height_spin.setSingleStep(50)
        self.room_height_spin.valueChanged.connect(self._on_room_height_changed)
        height_layout.addWidget(self.room_height_spin)
        layout.addLayout(height_layout)

        # Элементы
        elements_layout = QHBoxLayout()
        elements_layout.setSpacing(24)

        self.walls_count = self._create_counter("Стен", "0")
        elements_layout.addLayout(self.walls_count)

        self.windows_count = self._create_counter("Окон", "0", "#38bdf8")
        elements_layout.addLayout(self.windows_count)

        self.doors_count = self._create_counter("Дверей", "0", "#a3e635")
        elements_layout.addLayout(self.doors_count)

        elements_layout.addStretch()
        layout.addLayout(elements_layout)

        self.content_layout.addWidget(self.room_section)

    def _create_counter(self, label: str, value: str, color: str = "#f8fafc"):
        """Создать счётчик элементов"""
        col = QVBoxLayout()
        col.setSpacing(2)

        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        value_label.setObjectName(f"counter_{label}")
        col.addWidget(value_label, alignment=Qt.AlignCenter)

        text_label = QLabel(label)
        text_label.setStyleSheet("color: #64748b; font-size: 11px;")
        col.addWidget(text_label, alignment=Qt.AlignCenter)

        return col

    def _create_walls_section(self):
        """Секция списка стен"""
        self.walls_section = Card()
        layout = QVBoxLayout(self.walls_section)
        layout.setSpacing(12)

        header = SectionHeader("Стены", Icons.SVG_DRAW_WALL)
        layout.addWidget(header)

        self.walls_list = QListWidget()
        self.walls_list.setMaximumHeight(150)
        layout.addWidget(self.walls_list)

        self.content_layout.addWidget(self.walls_section)

    def update_project(self, project: Project):
        """Обновить проект"""
        self.project = project
        self._update_display()

    def select_room(self, room_id: str):
        """Выбрать комнату по ID"""
        for i in range(self.rooms_list.count()):
            item = self.rooms_list.item(i)
            if item.data(Qt.UserRole) == room_id:
                self.rooms_list.setCurrentItem(item)
                break

    def _update_display(self):
        """Обновить отображение"""
        # Проект
        self.project_name_row.set_value(self.project.name)

        # Статистика
        self.area_stat.set_value(f"{self.project.total_area:.1f} м²")
        self.rooms_stat.set_value(str(len(self.project.rooms)))

        # Список комнат
        self.rooms_list.clear()
        for room in self.project.rooms:
            item = QListWidgetItem(f"{room.name}  •  {room.floor_area:.1f} м²")
            item.setData(Qt.UserRole, room.id)
            self.rooms_list.addItem(item)

        # Свойства комнаты
        if self.current_room:
            self._update_room_display()
            self.room_section.setVisible(True)
            self.walls_section.setVisible(True)
        else:
            self.room_section.setVisible(False)
            self.walls_section.setVisible(False)

    def _update_room_display(self):
        """Обновить отображение свойств комнаты"""
        room = self.current_room
        if not room:
            return

        self.room_name_row.set_value(room.name)
        self.room_area_value.setText(f"{room.floor_area:.2f} м²")
        self.room_perimeter_value.setText(f"{room.perimeter / 1000:.2f} м")

        self.room_height_spin.blockSignals(True)
        self.room_height_spin.setValue(int(room.ceiling_height))
        self.room_height_spin.blockSignals(False)

        # Счётчики
        walls_label = self.findChild(QLabel, "counter_Стен")
        if walls_label:
            walls_label.setText(str(len(room.walls)))

        windows = sum(len(w.windows) for w in room.walls)
        windows_label = self.findChild(QLabel, "counter_Окон")
        if windows_label:
            windows_label.setText(str(windows))

        doors = sum(len(w.doors) for w in room.walls)
        doors_label = self.findChild(QLabel, "counter_Дверей")
        if doors_label:
            doors_label.setText(str(doors))

        # Список стен
        self.walls_list.clear()
        for i, wall in enumerate(room.walls, 1):
            info = f"Стена {i}:  {wall.length:.0f} мм"
            if wall.windows:
                info += f"  •  {len(wall.windows)} окон"
            if wall.doors:
                info += f"  •  {len(wall.doors)} дверей"
            self.walls_list.addItem(info)

    def _on_project_name_changed(self, name):
        """Изменено название проекта"""
        self.project.name = name
        self.project_changed.emit()

    def _on_room_selected(self, current, previous):
        """Выбрана комната"""
        if current:
            room_id = current.data(Qt.UserRole)
            self.current_room = self.project.get_room_by_id(room_id)
        else:
            self.current_room = None

        self._update_display()

    def _on_room_name_changed(self, name):
        """Изменено название комнаты"""
        if self.current_room:
            self.current_room.name = name
            self._update_display()
            self.project_changed.emit()

    def _on_room_height_changed(self, value):
        """Изменена высота комнаты"""
        if self.current_room:
            self.current_room.ceiling_height = value
            for wall in self.current_room.walls:
                wall.height = value
            self.project_changed.emit()

    def _add_room_clicked(self):
        """Клик по кнопке добавления комнаты"""
        from ..dialogs.room_dialog import RoomDialog
        dialog = RoomDialog(self)
        if dialog.exec_():
            room = dialog.get_room()
            if room:
                self.project.add_room(room)
                self._update_display()
                self.project_changed.emit()

    def _delete_room_clicked(self):
        """Удаление выбранной комнаты"""
        if self.current_room:
            from PyQt5.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self, "Удаление",
                f"Удалить комнату «{self.current_room.name}»?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.project.remove_room(self.current_room.id)
                self.current_room = None
                self._update_display()
                self.project_changed.emit()