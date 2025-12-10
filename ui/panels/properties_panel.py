"""
Панель свойств - современный дизайн
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QSpinBox, QPushButton,
    QGroupBox, QListWidget, QListWidgetItem,
    QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

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
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # === ПРОЕКТ ===
        project_group = QGroupBox("Проект")
        project_layout = QVBoxLayout(project_group)
        project_layout.setSpacing(12)

        # Название проекта
        name_layout = QHBoxLayout()
        name_label = QLabel("Название:")
        name_label.setMinimumWidth(80)
        self.project_name_edit = QLineEdit()
        self.project_name_edit.setPlaceholderText("Введите название проекта...")
        self.project_name_edit.textChanged.connect(self._on_project_name_changed)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.project_name_edit)
        project_layout.addLayout(name_layout)

        # Статистика
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(20)

        self.total_area_label = QLabel("0 м²")
        self.total_area_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #10b981;
        """)

        area_desc = QLabel("Общая\nплощадь")
        area_desc.setStyleSheet("color: #94a3b8; font-size: 11px;")

        stats_layout.addWidget(self.total_area_label)
        stats_layout.addWidget(area_desc)
        stats_layout.addStretch()

        project_layout.addWidget(stats_frame)
        layout.addWidget(project_group)

        # === КОМНАТЫ ===
        rooms_group = QGroupBox("Комнаты")
        rooms_layout = QVBoxLayout(rooms_group)
        rooms_layout.setSpacing(10)

        self.rooms_list = QListWidget()
        self.rooms_list.setMinimumHeight(120)
        self.rooms_list.setMaximumHeight(180)
        self.rooms_list.currentItemChanged.connect(self._on_room_selected)
        rooms_layout.addWidget(self.rooms_list)

        # Кнопки управления комнатами
        room_buttons = QHBoxLayout()

        add_room_btn = QPushButton("➕ Добавить")
        add_room_btn.clicked.connect(self._add_room_clicked)
        room_buttons.addWidget(add_room_btn)

        del_room_btn = QPushButton("🗑️ Удалить")
        del_room_btn.clicked.connect(self._delete_room_clicked)
        room_buttons.addWidget(del_room_btn)

        rooms_layout.addLayout(room_buttons)
        layout.addWidget(rooms_group)

        # === СВОЙСТВА КОМНАТЫ ===
        self.room_group = QGroupBox("Свойства комнаты")
        room_layout = QVBoxLayout(self.room_group)
        room_layout.setSpacing(12)

        # Название
        room_name_layout = QHBoxLayout()
        room_name_layout.addWidget(QLabel("Название:"))
        self.room_name_edit = QLineEdit()
        self.room_name_edit.textChanged.connect(self._on_room_name_changed)
        room_name_layout.addWidget(self.room_name_edit)
        room_layout.addLayout(room_name_layout)

        # Метрики комнаты
        metrics_frame = QFrame()
        metrics_frame.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        metrics_layout = QVBoxLayout(metrics_frame)
        metrics_layout.setSpacing(8)

        # Площадь
        area_row = QHBoxLayout()
        area_row.addWidget(QLabel("📐 Площадь:"))
        self.room_area_label = QLabel("—")
        self.room_area_label.setStyleSheet("font-weight: bold; color: #10b981;")
        area_row.addWidget(self.room_area_label)
        area_row.addStretch()
        metrics_layout.addLayout(area_row)

        # Периметр
        perim_row = QHBoxLayout()
        perim_row.addWidget(QLabel("📏 Периметр:"))
        self.room_perimeter_label = QLabel("—")
        self.room_perimeter_label.setStyleSheet("font-weight: bold;")
        perim_row.addWidget(self.room_perimeter_label)
        perim_row.addStretch()
        metrics_layout.addLayout(perim_row)

        # Высота
        height_row = QHBoxLayout()
        height_row.addWidget(QLabel("📐 Высота:"))
        self.room_height_spin = QSpinBox()
        self.room_height_spin.setRange(2000, 5000)
        self.room_height_spin.setSuffix(" мм")
        self.room_height_spin.setSingleStep(50)
        self.room_height_spin.valueChanged.connect(self._on_room_height_changed)
        height_row.addWidget(self.room_height_spin)
        height_row.addStretch()
        metrics_layout.addLayout(height_row)

        room_layout.addWidget(metrics_frame)

        # Элементы комнаты
        elements_frame = QFrame()
        elements_frame.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        elements_layout = QHBoxLayout(elements_frame)
        elements_layout.setSpacing(20)

        # Стены
        walls_col = QVBoxLayout()
        self.room_walls_label = QLabel("0")
        self.room_walls_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #f8fafc;")
        walls_col.addWidget(self.room_walls_label, alignment=Qt.AlignCenter)
        walls_col.addWidget(QLabel("Стен"), alignment=Qt.AlignCenter)
        elements_layout.addLayout(walls_col)

        # Окна
        windows_col = QVBoxLayout()
        self.room_windows_label = QLabel("0")
        self.room_windows_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #87ceeb;")
        windows_col.addWidget(self.room_windows_label, alignment=Qt.AlignCenter)
        windows_col.addWidget(QLabel("Окон"), alignment=Qt.AlignCenter)
        elements_layout.addLayout(windows_col)

        # Двери
        doors_col = QVBoxLayout()
        self.room_doors_label = QLabel("0")
        self.room_doors_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #cd853f;")
        doors_col.addWidget(self.room_doors_label, alignment=Qt.AlignCenter)
        doors_col.addWidget(QLabel("Дверей"), alignment=Qt.AlignCenter)
        elements_layout.addLayout(doors_col)

        room_layout.addWidget(elements_frame)

        layout.addWidget(self.room_group)

        # === СТЕНЫ ===
        walls_group = QGroupBox("Детали стен")
        walls_layout = QVBoxLayout(walls_group)

        self.walls_list = QListWidget()
        self.walls_list.setMaximumHeight(120)
        walls_layout.addWidget(self.walls_list)

        layout.addWidget(walls_group)

        # Растяжка внизу
        layout.addStretch()

        # Начальное состояние
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

        self.total_area_label.setText(f"{self.project.total_area:.1f} м²")

        # Список комнат
        self.rooms_list.clear()
        for room in self.project.rooms:
            item = QListWidgetItem(f"🏠  {room.name}  —  {room.floor_area:.1f} м²")
            item.setData(Qt.UserRole, room.id)
            self.rooms_list.addItem(item)

        # Свойства комнаты
        if self.current_room:
            self._update_room_display()
            self.room_group.setEnabled(True)
        else:
            self.room_group.setEnabled(False)
            self._clear_room_display()

    def _clear_room_display(self):
        """Очистить отображение комнаты"""
        self.room_name_edit.clear()
        self.room_area_label.setText("—")
        self.room_perimeter_label.setText("—")
        self.room_walls_label.setText("0")
        self.room_windows_label.setText("0")
        self.room_doors_label.setText("0")
        self.walls_list.clear()

    def _update_room_display(self):
        """Обновить отображение комнаты"""
        room = self.current_room
        if not room:
            return

        self.room_name_edit.blockSignals(True)
        self.room_name_edit.setText(room.name)
        self.room_name_edit.blockSignals(False)

        self.room_area_label.setText(f"{room.floor_area:.2f} м²")
        self.room_perimeter_label.setText(f"{room.perimeter / 1000:.2f} м")

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
            info = f"Стена {i}:  {wall.length:.0f} мм"
            if wall.windows:
                info += f"  🪟 {len(wall.windows)}"
            if wall.doors:
                info += f"  🚪 {len(wall.doors)}"
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
            self.room_group.setEnabled(True)
        else:
            self.current_room = None
            self.room_group.setEnabled(False)

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

    def _add_room_clicked(self):
        """Клик по кнопке добавления комнаты"""
        from ui.dialogs.room_dialog import RoomDialog
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
                self, "Удаление комнаты",
                f"Удалить комнату '{self.current_room.name}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.project.remove_room(self.current_room.id)
                self.current_room = None
                self._update_display()
                self.project_changed.emit()