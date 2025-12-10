"""
Диалог добавления/редактирования комнаты
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton,
    QLabel, QGroupBox, QComboBox, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt

from core.room import Room, Wall, Point2D, Window, Door


class RoomDialog(QDialog):
    """Диалог создания комнаты"""

    ROOM_PRESETS = {
        "custom": ("Произвольная", 0, 0),
        "small_bedroom": ("Спальня малая", 3000, 3500),
        "bedroom": ("Спальня", 4000, 4500),
        "living": ("Гостиная", 5000, 6000),
        "kitchen": ("Кухня", 3500, 4000),
        "bathroom": ("Ванная", 2000, 2500),
        "toilet": ("Туалет", 1200, 1800),
        "hallway": ("Прихожая", 2000, 4000),
        "office": ("Кабинет", 3000, 3500),
    }

    def __init__(self, parent=None, rectangular=False):
        super().__init__(parent)
        self.rectangular = rectangular
        self.room = None

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("Добавить комнату")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # Название
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название:"))
        self.name_edit = QLineEdit("Новая комната")
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Пресеты
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Шаблон:"))
        self.preset_combo = QComboBox()
        for key, (name, w, h) in self.ROOM_PRESETS.items():
            self.preset_combo.addItem(name, key)
        preset_layout.addWidget(self.preset_combo)
        layout.addLayout(preset_layout)

        # Размеры
        size_group = QGroupBox("Размеры (мм)")
        size_layout = QFormLayout(size_group)

        self.width_spin = QSpinBox()
        self.width_spin.setRange(500, 50000)
        self.width_spin.setValue(4000)
        self.width_spin.setSuffix(" мм")
        self.width_spin.setSingleStep(100)
        size_layout.addRow("Ширина:", self.width_spin)

        self.length_spin = QSpinBox()
        self.length_spin.setRange(500, 50000)
        self.length_spin.setValue(5000)
        self.length_spin.setSuffix(" мм")
        self.length_spin.setSingleStep(100)
        size_layout.addRow("Длина:", self.length_spin)

        self.height_spin = QSpinBox()
        self.height_spin.setRange(2000, 5000)
        self.height_spin.setValue(2700)
        self.height_spin.setSuffix(" мм")
        self.height_spin.setSingleStep(50)
        size_layout.addRow("Высота потолка:", self.height_spin)

        layout.addWidget(size_group)

        # Элементы комнаты
        elements_group = QGroupBox("Элементы")
        elements_layout = QVBoxLayout(elements_group)

        # Окно
        window_layout = QHBoxLayout()
        self.add_window_check = QCheckBox("Добавить окно")
        self.add_window_check.setChecked(True)
        window_layout.addWidget(self.add_window_check)

        window_layout.addWidget(QLabel("на стене:"))
        self.window_wall_combo = QComboBox()
        self.window_wall_combo.addItems(["1 (нижняя)", "2 (правая)", "3 (верхняя)", "4 (левая)"])
        self.window_wall_combo.setCurrentIndex(2)  # Верхняя стена по умолчанию
        window_layout.addWidget(self.window_wall_combo)
        elements_layout.addLayout(window_layout)

        # Дверь
        door_layout = QHBoxLayout()
        self.add_door_check = QCheckBox("Добавить дверь")
        self.add_door_check.setChecked(True)
        door_layout.addWidget(self.add_door_check)

        door_layout.addWidget(QLabel("на стене:"))
        self.door_wall_combo = QComboBox()
        self.door_wall_combo.addItems(["1 (нижняя)", "2 (правая)", "3 (верхняя)", "4 (левая)"])
        self.door_wall_combo.setCurrentIndex(0)  # Нижняя стена по умолчанию
        door_layout.addWidget(self.door_wall_combo)
        elements_layout.addLayout(door_layout)

        layout.addWidget(elements_group)

        # Площадь (информация)
        self.area_label = QLabel()
        self.area_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        layout.addWidget(self.area_label)
        self._update_area()

        # Кнопки
        buttons_layout = QHBoxLayout()

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("Создать")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self._create_room)
        buttons_layout.addWidget(ok_btn)

        layout.addLayout(buttons_layout)

    def _connect_signals(self):
        """Подключение сигналов"""
        self.preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        self.width_spin.valueChanged.connect(self._update_area)
        self.length_spin.valueChanged.connect(self._update_area)

    def _on_preset_changed(self, index):
        """Выбор пресета"""
        key = self.preset_combo.currentData()
        if key and key != "custom":
            name, width, length = self.ROOM_PRESETS[key]
            self.name_edit.setText(name)
            self.width_spin.setValue(width)
            self.length_spin.setValue(length)

    def _update_area(self):
        """Обновить отображение площади"""
        width = self.width_spin.value()
        length = self.length_spin.value()
        area = (width * length) / 1_000_000
        self.area_label.setText(f"📐 Площадь: {area:.2f} м²")

    def _create_room(self):
        """Создать комнату"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название комнаты")
            return

        width = self.width_spin.value()
        length = self.length_spin.value()
        height = self.height_spin.value()

        # Создаём прямоугольную комнату
        self.room = Room.create_rectangular(name, width, length, height)

        # Добавляем окно
        if self.add_window_check.isChecked() and len(self.room.walls) >= 4:
            wall_idx = self.window_wall_combo.currentIndex()
            wall = self.room.walls[wall_idx]

            # Окно по центру стены
            window_width = min(1200, wall.length * 0.6)
            window_pos = (wall.length - window_width) / 2

            window = Window(
                position=window_pos,
                width=window_width,
                height=1400,
                sill_height=900
            )
            wall.windows.append(window)

        # Добавляем дверь
        if self.add_door_check.isChecked() and len(self.room.walls) >= 4:
            wall_idx = self.door_wall_combo.currentIndex()
            wall = self.room.walls[wall_idx]

            # Дверь ближе к углу
            door_pos = 200

            door = Door(
                position=door_pos,
                width=900,
                height=2100
            )
            wall.doors.append(door)

        self.accept()

    def get_room(self) -> Room:
        """Получить созданную комнату"""
        return self.room