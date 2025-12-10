"""
Панель свойств - отображение и редактирование свойств комнаты
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QSpinBox, QPushButton,
    QGroupBox, QListWidget, QListWidgetItem,
    QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal

from core.project import Project
from core.room import Room


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
        layout.setContentsMargins(5, 5, 5, 5)

        # Скролл для всей панели
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)

        # === Проект ===
        project_group = QGroupBox("📁 Проект")
        project_layout = QFormLayout(project_group)

        self.project_name_edit = QLineEdit()
        self.project_name_edit.textChanged.connect(self._on_project_name_changed)
        project_layout.addRow("Название:", self.project_name_edit)

        self.total_area_label = QLabel("0 м²")
        self.total_area_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        project_layout.addRow("Общая площадь:", self.total_area_label)

        content_layout.addWidget(project_group)

        # === Список комнат ===
        rooms_group = QGroupBox("🏠 Комнаты")
        rooms_layout = QVBoxLayout(rooms_group)

        self.rooms_list = QListWidget()
        self.rooms_list.currentItemChanged.connect(self._on_room_selected)
        rooms_layout.addWidget(self.rooms_list)

        content_layout.addWidget(rooms_group)

        # === Свойства комнаты ===
        self.room_group = QGroupBox("📐 Свойства комнаты")
        room_layout = QFormLayout(self.room_group)

        self.room_name_edit = QLineEdit()
        self.room_name_edit.textChanged.connect(self._on_room_name_changed)
        room_layout.addRow("Название:", self.room_name_edit)

        self.room_area_label = QLabel()
        room_layout.addRow("Площадь:", self.room_area_label)

        self.room_perimeter_label = QLabel()
        room_layout.addRow("Периметр:", self.room_perimeter_label)

        self.room_height_spin = QSpinBox()
        self.room_height_spin.setRange(2000, 5000)
        self.room_height_spin.setSuffix(" мм")
        self.room_height_spin.valueChanged.connect(self._on_room_height_changed)
        room_layout.addRow("Высота:", self.room_height_spin)

        self.room_walls_label = QLabel()
        room_layout.addRow("Стен:", self.room_walls_label)

        self.room_windows_label = QLabel()
        room_layout.addRow("Окон:", self.room_windows_label)

        self.room_doors_label = QLabel()
        room_layout.addRow("Дверей:", self.room_doors_label)

        content_layout.addWidget(self.room_group)

        # === Стены ===
        self.walls_group = QGroupBox("🧱 Стены")
        walls_layout = QVBoxLayout(self.walls_group)

        self.walls_list = QListWidget()
        self.walls_list.setMaximumHeight(150)
        walls_layout.addWidget(self.walls_list)

        content_layout.addWidget(self.walls_group)

        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

        self._update_display()

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
        self.project_name_edit.blockSignals(True)
        self.project_name_edit.setText(self.project.name)
        self.project_name_edit.blockSignals(False)

        self.total_area_label.setText(f"{self.project.total_area:.2f} м²")

        # Список комнат
        self.rooms_list.clear()
        for room in self.project.rooms:
            item = QListWidgetItem(f"{room.name} ({room.floor_area:.1f} м²)")
            item.setData(Qt.UserRole, room.id)
            self.rooms_list.addItem(item)

        # Свойства комнаты
        if self.current_room:
            self._update_room_display()
        else:
            self.room_group.setEnabled(False)
            self.walls_group.setEnabled(False)

    def _update_room_display(self):
        """Обновить отображение комнаты"""
        room = self.current_room
        if not room:
            return

        self.room_group.setEnabled(True)
        self.walls_group.setEnabled(True)

        self.room_name_edit.blockSignals(True)
        self.room_name_edit.setText(room.name)
        self.room_name_edit.blockSignals(False)

        self.room_area_label.setText(f"{room.floor_area:.2f} м²")
        self.room_perimeter_label.setText(f"{room.perimeter:.0f} мм ({room.perimeter / 1000:.2f} м)")

        self.room_height_spin.blockSignals(True)
        self.room_height_spin.setValue(int(room.ceiling_height))
        self.room_height_spin.blockSignals(False)

        self.room_walls_label.setText(str(len(room.walls)))

        windows = sum(len(w.windows) for w in room.walls)
        doors = sum(len(w.doors) for w in room.walls)

        self.room_windows_label.setText(str(windows))
        self.room_doors_label.setText(str(doors))

        # Список стен
        self.walls_list.clear()
        for i, wall in enumerate(room.walls, 1):
            info = f"Стена {i}: {wall.length:.0f} мм"
            if wall.windows:
                info += f" | {len(wall.windows)} окно"
            if wall.doors:
                info += f" | {len(wall.doors)} дверь"
            self.walls_list.addItem(info)

    def _on_project_name_changed(self, text):
        """Изменено название проекта"""
        self.project.name = text
        self.project_changed.emit()

    def _on_room_selected(self, current, previous):
        """Выбрана комната"""
        if current:
            room_id = current.data(Qt.UserRole)
            self.current_room = self.project.get_room_by_id(room_id)
            self._update_room_display()
        else:
            self.current_room = None

    def _on_room_name_changed(self, text):
        """Изменено название комнаты"""
        if self.current_room:
            self.current_room.name = text
            self._update_display()
            self.project_changed.emit()

    def _on_room_height_changed(self, value):
        """Изменена высота комнаты"""
        if self.current_room:
            self.current_room.ceiling_height = value
            for wall in self.current_room.walls:
                wall.height = value
            self.project_changed.emit()